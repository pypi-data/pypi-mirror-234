#!/usr/bin/env python3

"""
This script simply wraps terragrunt (which is a wrapper around terraform...)
and its main function is to allow you to execute a `run-all` command but
broken up in individual steps.

This makes debugging a complex project easier, such as spotting where the
exact problem is.
"""

# idea: parse output
# - https://github.com/bcochofel/terraplanfeed/tree/main/terraplanfeed

import os
import sys
import subprocess
import shlex
import shutil
import glob
import re
import tempfile
import json
import yaml
import threading
import queue
import multiprocessing
import click
import networkx as nx
import hcl2
import fnmatch

from datetime import datetime, timezone
from .printer import Printer
from .analyze import run_analyze

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class TgWrap():
    """
    A wrapper around terragrunt with the sole purpose to make it a bit
    (in an opiionated way) easier to use
    """
    SEPARATOR=':|:'
    TERRAGRUNT_FILE='terragrunt.hcl'
    VERSION_FILE="version.hcl"
    LATEST_VERSION='latest'
    LOCATE_VERSION_FILE_MAX_LEVELS=3
    PLANFILE_NAME="planfile"
    TG_SOURCE_VAR="TERRAGRUNT_SOURCE"
    TG_SOURCE_MAP_VAR="TERRAGRUNT_SOURCE_MAP"


    def __init__(self, verbose, check_tg_source=False):
        self.printer = Printer(verbose)

        if check_tg_source:
            # Check if the "TERRAGRUNT_SOURCE" or "TERRAGRUNT_SOURCE_MAP" environment variable is set
            # TERRAGRUNT_SOURCE takes precedence
            if self.TG_SOURCE_MAP_VAR in os.environ:
                self.printer.warning(
                    f"'{self.TG_SOURCE_MAP_VAR}' environment variable is set with addresses: '{os.environ[self.TG_SOURCE_MAP_VAR]}'!"
                    )
                self.tg_source_indicator = self.TG_SOURCE_MAP_VAR

                # if also TG_SOURCE_VAR is set, delete it to avoid it overriding the source map
                if self.TG_SOURCE_VAR in os.environ:
                    del os.environ[self.TG_SOURCE_VAR]
            elif self.TG_SOURCE_VAR in os.environ:
                self.printer.warning(
                    f"'{self.TG_SOURCE_VAR}' environment variable is set with address: '{os.environ[self.TG_SOURCE_VAR]}'!"
                    )
                self.tg_source_indicator = self.TG_SOURCE_VAR
            else:
                self.printer.success(
                    f"No 'TERRAGRUNT_SOURCE[_MAP]' variable is set, so the sources as defined in terragrunt.hcl files will be used as is!"
                    )
                self.tg_source_indicator = None

    def _is_installed(self, program):
        """ Checks if a program is installed on the system """
        return shutil.which(program) is not None

    def load_yaml_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except yaml.parser.ParserError as e:
            self.printer.error(f'Cannot parse YAML file {filepath}, check syntax please!')
            sys.exit(1)

    def _construct_command(self, command, allow_no_run_all, debug, exclude_external_dependencies,
        non_interactive=True, no_auto_approve=True, no_lock=True, update=False, upgrade=False,
        planfile=None, working_dir=None, limit_parallelism=None, 
        include_dirs=[], exclude_dirs=[], terragrunt_args=(), source_module=None):
        """ Constructs the command """

        commands = {
            'generic': '{base_command} {command} --terragrunt-non-interactive {no_auto_approve} {update} {upgrade} {parallelism} {common}',
            'info': '{base_command} terragrunt-info --terragrunt-non-interactive {update} {upgrade} {common}',
            'plan': '{base_command} {command} --terragrunt-non-interactive  -out={planfile_name} {lock_level} {update} {parallelism} {common}',
            'apply': '{base_command} {command} {non_interactive} {no_auto_approve} {update} {parallelism} {common} {planfile}',
            'show': '{base_command} {command} --terragrunt-non-interactive {ignore_deps} {update} -json {planfile_name}', # no working dir allowed here!!!
            'destroy': '{base_command} {command} {non_interactive} {no_auto_approve} {parallelism} {common} {planfile}',
        }

        lock_stmt = ''
        if no_lock and command in ['init', 'validate', 'validate-inputs', 'plan', 'info', 'output', 'show', 'state']:
            lock_stmt = '-lock=false'
            self.printer.warning('Terraform state will NOT be locked')
        elif no_lock:
            self.printer.normal("Request for no-lock cannot be granted")
        else:
            self.printer.normal('Terraform state will be locked')

        update_stmt       = '--terragrunt-source-update' if update else ''
        upgrade_stmt      = '-upgrade' if upgrade else ''
        ignore_deps_stmt  = '--terragrunt-ignore-external-dependencies' if exclude_external_dependencies else '--terragrunt-include-external-dependencies'
        debug_stmt        = '--terragrunt-log-level debug --terragrunt-debug' if debug else ''
        working_dir_stmt  = f'--terragrunt-working-dir {working_dir}' if working_dir else ''
        planfile_stmt     = f'{self.PLANFILE_NAME}' if planfile else ''

        # if we have a source_module passed, we can assign it to TERRAGRUNT_SOURCE
        use_run_all = False
        if self.tg_source_indicator and allow_no_run_all and source_module:
            # we can update the terragrunt source map to fully refer to the module, and then no need for a run-all
            if self.tg_source_indicator == self.TG_SOURCE_MAP_VAR:
                self.printer.verbose(
                    f'{self.TG_SOURCE_MAP_VAR} environment variable is set, no need for further manipulation in order to enhance performance.'
                    )
            elif self.tg_source_indicator == self.TG_SOURCE_VAR:
                terragrunt_source = f'{os.environ.get(self.TG_SOURCE_VAR).rstrip("//.")}//{source_module}'
                os.environ[self.TG_SOURCE_VAR] = terragrunt_source
                self.printer.verbose(
                    f'{self.TG_SOURCE_VAR} environment variable manipulated for extra performance (no run-all): {terragrunt_source}'
                    )
            else:
                self.printer.verbose('Performance enhancements allowed but was not able to configure it.')

        elif self.tg_source_indicator or not allow_no_run_all:
            use_run_all = True

        # if TERRAGRUNT_SOURCE environment variable is set, run-all is needed to avoid re-initialisation (at best)
        if use_run_all:
            base_command      = 'terragrunt run-all'
            ignore_deps_stmt  = '--terragrunt-ignore-external-dependencies' if exclude_external_dependencies else '--terragrunt-include-external-dependencies'
            auto_approve_stmt = '--terragrunt-no-auto-approve' if no_auto_approve else ''
            interactive_stmt  = '--terragrunt-non-interactive' if non_interactive else ''
            parallelism_stmt  = f'--terragrunt-parallelism {limit_parallelism}' if limit_parallelism else ''
            include_dir_stmt  = f'--terragrunt-strict-include  --terragrunt-include-dir {" --terragrunt-include-dir ".join(include_dirs)}' if len(include_dirs) > 0 else ""
            exclude_dir_stmt  = f'--terragrunt-exclude-dir {" --terragrunt-exclude-dir ".join(exclude_dirs)}' if len(exclude_dirs) > 0 else ""
        else:
            base_command      = 'terragrunt'
            ignore_deps_stmt  = ''
            auto_approve_stmt = '' if no_auto_approve else '-auto-approve'
            interactive_stmt  = ''
            parallelism_stmt  = ''
            include_dir_stmt  = ''
            exclude_dir_stmt  = ''

        common_commands = f"{ignore_deps_stmt} {debug_stmt} {working_dir_stmt} {include_dir_stmt} {exclude_dir_stmt} {' '.join(terragrunt_args)}"

        if command not in ['clean']:
            full_command = commands.get(command, commands.get('generic')).format(
                base_command=base_command,
                command=command,
                lock_level=lock_stmt,
                update=update_stmt,
                upgrade=upgrade_stmt,
                ignore_deps=ignore_deps_stmt,
                no_auto_approve=auto_approve_stmt,
                non_interactive=interactive_stmt,
                parallelism=parallelism_stmt,
                planfile=planfile_stmt,
                common=common_commands,
                planfile_name=self.PLANFILE_NAME,
            )
        else:
            full_command = commands.get(command, commands.get('generic'))

        # remove double spaces
        full_command = re.sub(' +', ' ', full_command)

        self.printer.verbose(f'Full command to execute:\n$ {full_command}')

        return full_command

    def _check_directory_inclusion(self, directory, working_dir, exclude_external_dependencies, include_dirs=[], exclude_dirs=[]):
        """Check whether a given directory should be included given a list of include and exclude glob patterns"""

        dir_excluded = False
        dir_included = True if len(include_dirs) == 0 else False # if we have a list of include dirs, then all others will be ignored
        dir_excluded_reason = ""

        # ensure consistency, remove possible trailing slashes from the dirs                
        directory = directory.rstrip(os.path.sep)

        # ensure consistency, remove possible ./ prefixes from the dirs
        include_dirs = [dir.lstrip(f'.{os.path.sep}') for dir in include_dirs]
        exclude_dirs = [dir.lstrip(f'.{os.path.sep}') for dir in exclude_dirs]

        common_path = os.path.commonpath([os.path.abspath(working_dir), os.path.abspath(directory)])
        self.printer.verbose(f'Common path for dir {directory}: {common_path}')

        if common_path != os.path.abspath(working_dir) \
            and exclude_external_dependencies:
            dir_excluded = True
            dir_excluded_reason = "directory out of scope"
        else:
            for i in exclude_dirs:
                if fnmatch.fnmatch(directory, i):
                    dir_excluded = True
                    dir_excluded_reason = "directory explicitly excluded"

            # if we have a specific set of include_dirs, then everything else should be excluded
            for i in include_dirs:
                if fnmatch.fnmatch(directory, i):
                    dir_included = True

        if dir_excluded: # directory explicitly excluded
            self.printer.verbose(
                f"- Remove directory '{directory}': {dir_excluded_reason}"
                )
        elif not dir_included: # directory NOT explicitly excluded and NOT (no include dirs or not explicitly included)
            self.printer.verbose(
                f"- Remove directory '{directory}': specific list of include dirs given"
                )
        else:
            self.printer.verbose(f"+ Include directory: {directory}")

        return dir_included and not dir_excluded

    def _get_subdirectories_with_file(self, root_dir, file_name, exclude_external_dependencies,
            exclude_dirs=[], include_dirs=[], exclude_hidden_dir=True):

        # Get the current working directory
        current_dir = os.getcwd()
        # change to working directory, to avoid os.walk to include that in the paths
        os.chdir(root_dir)

        try:
            # ensure consistency, remove possible trailing slashes from the dirs
            exclude_dirs = [dir.rstrip(os.path.sep) for dir in exclude_dirs]
            include_dirs = [dir.rstrip(os.path.sep) for dir in include_dirs]

            subdirectories = []
            for directory, dirnames, filenames in os.walk("."):
                # Exclude hidden directories that start with a dot
                dirnames[:] = [d for d in dirnames if not (d.startswith('.') and exclude_hidden_dir)]

                # Check if the current directory contains the specified file
                if file_name in filenames:
                    self.printer.verbose(f"Directory found: {directory}")

                    include = self._check_directory_inclusion(
                        directory=directory.lstrip(f'.{os.path.sep}'),
                        working_dir=".",
                        exclude_external_dependencies=exclude_external_dependencies,
                        include_dirs=include_dirs,
                        exclude_dirs=exclude_dirs,
                    )

                    if include:
                        subdirectories.append(directory.lstrip(f'.{os.path.sep}'))

        finally:
            os.chdir(current_dir)

        return subdirectories

    def _prepare_groups(self, graph, exclude_external_dependencies, working_dir,
                        exclude_dirs=[], include_dirs=[]):
        """ Prepare the list of groups that will be executed """

        working_dir = os.path.abspath(working_dir) if working_dir else os.getcwd()
        self.printer.verbose(f"Check for working dir: {working_dir}")

        # ensure consistency, remove possible trailing slashes from the dirs
        exclude_dirs = [dir.rstrip(os.path.sep) for dir in exclude_dirs]
        include_dirs = [dir.rstrip(os.path.sep) for dir in include_dirs]

        self.printer.verbose(f"Include dirs: {'; '.join(include_dirs)}")
        self.printer.verbose(f"Exclude dirs: {'; '.join(exclude_dirs)}")

        groups = []
        for group in nx.topological_generations(graph):
            try:
                group.remove("\\n") # terragrunt is adding this in some groups for whatever reason
            except ValueError:
                pass

            for idx, directory in enumerate(group):
                include = self._check_directory_inclusion(
                    directory=directory,
                    working_dir=working_dir,
                    exclude_external_dependencies=exclude_external_dependencies,
                    include_dirs=include_dirs,
                    exclude_dirs=exclude_dirs,
                )

                if not include:
                    group[idx] = None

            # remove the null values from the list
            group = list(filter(None, group))
            if len(group) > 0:
                groups.append(group)

        return groups

    def _get_di_graph(self, backwards=False, working_dir=None):
        """ Gets the directed graph of terragrunt dependencies, and parse it into a graph object """
        graph = None
        try:
            f = tempfile.NamedTemporaryFile(mode='w+', prefix='tgwrap-', delete=True)
            self.printer.verbose(f"Opened temp file for graph collection: {f.name}")

            working_dir_stmt = f'--terragrunt-working-dir {working_dir}' if working_dir else ''
            command = \
                f'terragrunt graph-dependencies --terragrunt-non-interactive {working_dir_stmt}'
            rc = subprocess.run(
                shlex.split(command),
                text=True,
                stdout=f,
            )
            self.printer.verbose(rc)

            f.flush()

            graph = nx.DiGraph(nx.nx_pydot.read_dot(f.name))
            if not backwards:
                # For regular operations the graph must be reversed
                graph = graph.reverse()
            else:
                self.printer.verbose("Graph will be interpreted backwards!")
        except TypeError as e:
            self.printer.error('terragrunt has problems generating the graph, check the dependencies please!')
            self.printer.error("once fixed, you can run 'tgwrap show-graph' to verify.")
            raise click.ClickException(e)
        except Exception as e:
            self.printer.error(e)
            raise click.ClickException(e)
        finally:
            f.close()

        return graph

    def _clone_repo(self, manifest, target_dir, version_tag=None):
        """Clones the repo, possibly a specific version, into a temp directory"""

        def check_version_tag(reference, working_dir):
            is_branch = False
            quiet_mode = "" if self.printer.print_verbose else "--quiet"

            # Check if the given reference is a tag
            tag_command = f'git show-ref --verify {quiet_mode} refs/tags/{reference}'
            tag_process = subprocess.run(
                shlex.split(tag_command),
                cwd=working_dir,
                capture_output=True,
                )
            is_tag = tag_process.returncode == 0
            self.printer.verbose(f'Check for tag: {tag_process}')

            # if it is not a tag, then it might be a branch
            if not is_tag:
                branch_command = f'git switch {reference}'
                branch_process = subprocess.run(
                    shlex.split(branch_command),
                    cwd=working_dir,
                    capture_output=True,
                    )
                is_branch = branch_process.returncode == 0
                self.printer.verbose(f'Check for branch: {branch_process}')

            # Print the result
            if is_branch:
                self.printer.verbose(f"The given reference '{reference}' is a branch.")
            elif is_tag:
                self.printer.verbose(f"The given reference '{reference}' is a tag.")
            else:
                msg = f"The given reference '{reference}' is neither a branch nor a tag."
                self.printer.verbose(f"The given reference '{reference}' is neither a branch nor a tag.")
                raise Exception(msg)
                

            return is_branch, is_tag

        # clone the repo
        repo = manifest['git_repository']
        self.printer.verbose(f'Clone repo {repo}')
        
        cmd = f"git clone {repo} {target_dir}"
        rc = subprocess.run(
            shlex.split(cmd),
            check=True,
            stdout=sys.stdout if self.printer.print_verbose else subprocess.DEVNULL,
            stderr=sys.stderr if self.printer.print_verbose else subprocess.DEVNULL,
            )
        self.printer.verbose(rc)

        # now check out the specific version if we don't want latest
        if version_tag and version_tag.lower() != self.LATEST_VERSION:
            # first check if we have a tag or a branch
            is_branch, is_tag = check_version_tag(
                reference=version_tag,
                working_dir=target_dir,
                )

            if is_tag:
                cmd = f"git checkout -b source {version_tag}"
                rc = subprocess.run(
                    shlex.split(cmd),
                    cwd=target_dir,
                    check=True,
                    stdout=sys.stdout if self.printer.print_verbose else subprocess.DEVNULL,
                    stderr=sys.stderr if self.printer.print_verbose else subprocess.DEVNULL,
                    )
                self.printer.verbose(rc)
            elif is_branch:
                pass # should already be present
            else:
                self.printer.error(f'Version tag {version_tag} seems neither a branch or a tag, cannot switch to it!')

    def _analyze_results(self, rc, messages):
        """ Checks for errors """

        error = False
        skip = False

        messages = messages.lower()

        if rc.returncode != 0 or 'error' in messages.lower():
            error = True

        if 'skipping terragrunt module' in messages.lower():
            skip = True

        return error, skip

    def _run_graph_step(self, command, working_dir, add_to_workdir, module, collect_output_file,
        dry_run, progress, output_queue=None, semaphore=None):
        """ Runs a step in the graph """

        MODULE_IDENTIFIER=f'{module}{self.SEPARATOR}'

        stop_processing = False
        error = False
        skip = False
        output = None
        error_msg = None
        messages = ""

        try:
            # if we are in multi-threading mode, acquire a semaphore
            if semaphore:
                semaphore.acquire()

            # if we have a specific working dir, and the dir is relative, combine the two
            if working_dir and not os.path.isabs(module):
                working_dir = os.path.join(os.path.abspath(working_dir), module)
            else:
                working_dir = module
            
            if add_to_workdir:
                working_dir = os.path.join(working_dir, add_to_workdir)

            self.printer.verbose(f'Execute command: {command} in working dir: {working_dir}')

            self.printer.verbose(f'Executing in directory: {working_dir}')

            self.printer.header(
                f'\n\nStart processing module: {module} ({progress})\n\n',
                print_line_before=True,
                )

            if dry_run:
                self.printer.warning(
                    'In dry run mode, no real actions are executed!!'
                    )
            else:
                if collect_output_file:
                    self.printer.verbose('Use an output file for output collection')

                    # module identifier needs to be pre-written to output file, so that the output can be appended to it
                    collect_output_file.write(MODULE_IDENTIFIER)
                    collect_output_file.flush()
                elif output_queue:
                    self.printer.verbose('Use an output queue for output collection')

                    # no output file, but data must be written to queue
                    # so we need to capture the output
                    collect_output_file = subprocess.PIPE

                messages = ""

                planfile = os.path.join(working_dir, self.PLANFILE_NAME)
                if f"-json {self.PLANFILE_NAME}" in command and not os.path.exists(planfile):
                    skip = True
                    output = '\n'
                    self.printer.verbose(f"Planfile '{planfile}' does not exist")
                elif os.path.exists(working_dir):
                    with tempfile.NamedTemporaryFile(mode='w+', prefix='tgwrap-', delete=False) as f:
                        self.printer.verbose(f"Opened temp file for error collection: {f.name}")
                        rc = {'returncode': 0}
                        rc = subprocess.run(
                            shlex.split(command),
                            text=True,
                            cwd=working_dir,
                            stdout=collect_output_file if collect_output_file else sys.stdout,
                            stderr=f,
                        )
                        self.printer.verbose(f'arguments: {rc.args}')
                        self.printer.verbose(f'returncode: {rc.returncode}')
                        try:
                            self.printer.verbose(f'stdout: {rc.stdout[:200]}')
                        except Exception:
                            pass

                    with open(f.name, 'r') as f:
                        messages = f.read()

                    error, skip = self._analyze_results(
                        rc=rc,
                        messages=messages,
                        )
                    
                    # if we have a skipped module, and are collecting output, make sure we end up on a new line

                    output = rc.stdout if rc.stdout else '\n'
                else:
                    skip = True
                    output = '\n'
                    self.printer.verbose(f"Directory '{working_dir}' does not exist")

                if skip:
                    self.printer.verbose("Module is skipped")

                if error:
                    raise Exception(
                        f'An error situation detected while processing the terragrunt dependencies graph in directory {module}'
                    )
                else:
                    self.printer.success(
                        f'Directory {module} processed successfully',
                    )

        except FileNotFoundError:
            error_msg = f'Directory {working_dir} not found, continue'
            self.printer.warning(error_msg)
        except Exception as e:
            error_msg = f"Error occurred:\n{str(e)}"
            self.printer.error(error_msg)
            self.printer.error("Full stack:", print_line_before=True)
            self.printer.normal(messages, print_line_after=True)
            self.printer.normal(f"Directory {module} failed!")

            stop_processing = True
        finally:
            if error_msg:
                output = json.dumps({"exception": error_msg})

            try:
                # communicate the results if desired
                if output_queue:
                    output_queue.put(f'{MODULE_IDENTIFIER}{output}')
                elif collect_output_file and (skip or error):
                    collect_output_file.write(output)
                    collect_output_file.flush()
            except Exception as e:
                self.printer.error(f'Error writing the results: {e}')

            if semaphore:
                semaphore.release()
            try:
                os.remove(f.name)
            except Exception:
                pass

        return stop_processing

    def _run_di_graph(
        self, command, exclude_external_dependencies, start_at_step, dry_run,
        parallel_execution=False, ask_for_confirmation=False, collect_output_file=None,
        backwards=False, working_dir=None, include_dirs=[], exclude_dirs=[],
        use_native_terraform=False, add_to_workdir=None,
        ):
        "Runs the desired command in the directories as defined in the directed graph"

        if use_native_terraform:
            module_dirs = self._get_subdirectories_with_file(
                root_dir = working_dir if working_dir else ".",
                file_name=self.TERRAGRUNT_FILE,
                exclude_hidden_dir=True,
                exclude_external_dependencies=exclude_external_dependencies,
                include_dirs=include_dirs,
                exclude_dirs=exclude_dirs,
            )
            # for native terraform, we just have one group with no inter-dependencies
            groups = [module_dirs]
        else:
            graph = self._get_di_graph(backwards=backwards, working_dir=working_dir)

            # first go through the groups and clean up where needed
            groups = self._prepare_groups(
                graph=graph,
                exclude_external_dependencies=exclude_external_dependencies,
                working_dir=working_dir,
                include_dirs=include_dirs,
                exclude_dirs=exclude_dirs,
                )

        if not groups:
            self.printer.error('No groups to process, this smells fishy!')
        elif ask_for_confirmation or self.printer.verbose:
            self.printer.header("The following groups will be processed:")
            for idx, group in enumerate(groups):
                self.printer.normal(f"\nGroup {idx+1}:")
                for module in group:
                    self.printer.normal(f"- {module}")

        if ask_for_confirmation:
            response = input("\nDo you want to continue? (y/N) ")
            if response.lower() != "y":
                sys.exit(1)

        # We only support multi-threading with 'show'
        nbr_of_threads = multiprocessing.cpu_count() if parallel_execution and 'show' in command.lower() else 1

        if parallel_execution:
            self.printer.warning(f'We are in EXPERIMENTAL multi-threading mode using {nbr_of_threads} threads!')
            q = queue.Queue()
            semaphore = threading.Semaphore(nbr_of_threads)
            threads = []

        counter = 0
        nbr_of_groups = len(groups)
        for idx, group in enumerate(groups):
            group_nbr=idx+1
            self.printer.header(f'Group {group_nbr}')
            self.printer.verbose(group)

            nbr_of_modules = len(group)
            for idx2, module in enumerate(group):
                counter += 1
                module_nbr=idx2+1
                progress = f'module {module_nbr} (of {nbr_of_modules}) of group {group_nbr} (of {nbr_of_groups})'

                step_nbr = group_nbr + module_nbr/100
                if step_nbr < start_at_step:
                    self.printer.normal(f'Skip step {step_nbr}, start at {start_at_step}')
                    continue

                if parallel_execution:
                    self.printer.verbose(f'Start thread #{counter} for step {step_nbr}')
                    t = threading.Thread(
                        target=self._run_graph_step,
                        kwargs={
                            "command": command,
                            "working_dir": working_dir,
                            "add_to_workdir": add_to_workdir,
                            "module": module,
                            "collect_output_file": None, # in parallel mode we can't write directly to the output file
                            "dry_run": dry_run,
                            "progress": progress,
                            "output_queue": q,
                            "semaphore": semaphore,
                            }
                        )
                    t.start()
                    threads.append(t)
                else:
                    stop_processing = self._run_graph_step(
                        command=command,
                        working_dir=working_dir,
                        add_to_workdir=add_to_workdir,
                        module=module,
                        collect_output_file=collect_output_file,
                        dry_run=dry_run,
                        progress=progress,
                    )

                    if stop_processing:
                        self.printer.warning(f"Processing needs to be stopped at step {step_nbr}.")
                        self.printer.normal(
                            f"After you've fixed the problem, you can continue where you left off by adding '--start-at-step {step_nbr}'."
                            )
                        sys.exit(1)

        if parallel_execution:
            # now wait until the threads are done and collect the output
            # todo: how to implement something as stop_processing like in regular execution?
            total_counter = counter
            counter = 0
            for t in threads:
                counter += 1
                self.printer.verbose(f'Wait for thread #{counter} (of {total_counter}) to finish')
                t.join()
                collect_output_file.write(q.get())

        if self.printer.print_verbose:
            total_items = sum(len(group) for group in groups)
            self.printer.verbose(f'Executed {group_nbr} groups and {total_items} steps')

    def _run_sync(
        self, source_path, target_path, auto_approve, include_lock_file, dry_run, clean,
        chmod_to_readonly=False, excludes=[], source_stage=None, target_stage=None, source_domain=None,
        ):
        """ Run a sync copying files from a source to a target path """

        if not self._is_installed('rsync'):
            self.printer.error("'rsync' seems not installed. Cannot continue")
        elif not os.path.exists(source_path):
            self.printer.error(f"Cannot find {source_path}. Cannot continue.")
            if source_domain:
                self.printer.error(
                    "Please ensure you are in the directory that contains your projects, " + \
                    "or use --working-dir option"
                )
            else:
                self.printer.error(
                    "Please ensure you are in the root of your project, or use --working-dir option"
                )
        else:
            self.printer.verbose(f"Copying config: {source_path} => {target_path}")

            try:
                os.makedirs(target_path)
            except OSError:
                # directory already exists
                pass

            dry_run_stmt = '--dry-run' if dry_run else ''
            clean_stmt   = '--delete' if clean else ''
            env_file_stmt   = "--exclude='env.hcl'" if source_stage != target_stage else "--include='env.hcl'"
            lock_file_stmt  = "--include='.terraform.lock.hcl'" if include_lock_file \
                else "--exclude='.terraform.lock.hcl'"
            excludes_stmt = ' '.join([f"--exclude={x}" for x in excludes])

            include_statements = ""
            #
            # Note: this logic is somewhat flawed, basically if the target doesn't exist it assumes it must be
            # a directory, which is not always what you want!!!!!
            #
            if os.path.isdir(target_path):
                include_statements = \
                    f"--include='{self.TERRAGRUNT_FILE}' {lock_file_stmt} {env_file_stmt} {excludes_stmt} " + \
                    "--exclude='.terragrunt-cache/' --exclude='.terraform/' " + \
                    "--exclude='terragrunt-debug.tfvars.json' --exclude=planfile " + \
                    "--exclude='.DS_Store' "

            cmd = f"rsync -aim {dry_run_stmt} {clean_stmt} " + \
                include_statements + \
                f"{source_path} {target_path}"

            cmd = re.sub(' +', ' ', cmd)

            self.printer.header("Will be deploying:", print_line_before=True)
            self.printer.normal(f"from: {source_path}")
            self.printer.normal(f"to:   {target_path}")
            self.printer.verbose(f"Using command:\n$ {cmd}")

            if not auto_approve:
                response = input("\nDo you want to continue? (y/N) ")
                if response.lower() != "y":
                    sys.exit(1)

            rc = subprocess.run(shlex.split(cmd))
            self.printer.verbose(rc)

            # not working, results in an 'permission denied' at first run
            # more info see: https://github.com/gruntwork-io/terragrunt/issues/2578
            # if chmod_to_readonly and os.path.isdir(target_path):
            #     cmd = f"find {target_path} -type f -name '.terraform.lock.hcl' -exec chmod a-w {{}} \;"
            #     self.printer.normal('Change .terraform-lock files to read only')
            #     self.printer.verbose(f"Using command:\n$ {cmd}")
            #     rc = subprocess.run(
            #         cmd,
            #         shell=True,
            #         check=True,
            #         stdout=sys.stdout if self.printer.print_verbose else subprocess.DEVNULL,
            #         stderr=sys.stderr if self.printer.print_verbose else subprocess.DEVNULL,
            #         cwd=target_path,
            #     )
            #     self.printer.verbose(rc)

    def run(self, command, debug, dry_run, no_lock, update, upgrade,
        planfile, auto_approve, clean, working_dir, terragrunt_args):
        """ Executes a terragrunt command on a single module """

        self.printer.verbose(f"Attempting to execute 'run {command}'")
        if terragrunt_args:
            self.printer.verbose(f"- with additional parameters: {' '.join(terragrunt_args)}")

        check_for_file=self.TERRAGRUNT_FILE
        if working_dir:
            check_for_file = os.path.join(working_dir, check_for_file)
        if not os.path.isfile(check_for_file):
            self.printer.error(
                f"{check_for_file} not found, this seems not to be a terragrunt module directory!"
                )
            sys.exit(1)
        else:
            # check if we can get the module part from the source
            source_module = None
            with open(check_for_file, 'r') as file:
                try:
                    content = hcl2.load(file)
                    source = content['terraform'][0]['source']
                    # get the source part, typically the last part after the double /.
                    # also remove a potential version element from it.
                    source_module = re.sub(r'\${[^}]*}', '', source.split('//')[::-1][0])
                except Exception as e:
                    self.printer.warning(f'Could not parse terragrunt.hcl, error (of type {type(e)}) raised, but we fall back to default behaviour.')
                    pass

        cmd = self._construct_command(
            command=command,
            allow_no_run_all=True,
            debug=debug,
            exclude_external_dependencies=True,
            no_lock=no_lock,
            update=update,
            upgrade=upgrade,
            planfile=planfile,
            no_auto_approve=(not auto_approve),
            working_dir=working_dir,
            terragrunt_args=terragrunt_args,
            source_module=source_module,
        )

        if dry_run:
            self.printer.warning(f'In dry run mode, no real actions are executed!!')
        else:
            if clean:
                self.clean(working_dir=working_dir)

            # the `posix=False` is to prevent the split command to remove quotes from strings,
            # e.g. when executing commands like this:
            # tgwrap state mv 'azuread_group.this["viewers"]' 'azuread_group.this["readers"]'
            rc = subprocess.run(shlex.split(cmd, posix=False))
            self.printer.verbose(rc)

            sys.exit(rc.returncode)

    def run_all(self, command, debug, dry_run, no_lock, update, upgrade,
        exclude_external_dependencies, step_by_step, planfile, auto_approve, clean,
        working_dir, start_at_step, limit_parallelism, include_dirs, exclude_dirs, terragrunt_args):
        """ Executes a terragrunt command across multiple modules """

        self.printer.verbose(f"Attempting to execute 'run-all {command}'")
        if terragrunt_args:
            self.printer.verbose(f"- with additional parameters: {' '.join(terragrunt_args)}")

        # auto approve is only relevant with a modifying command
        modifying_command = (command.lower() in ['apply', 'destroy'])
        auto_approve = auto_approve if modifying_command else True

        cmd = self._construct_command(
            command=command,
            allow_no_run_all=False,
            debug=debug,
            exclude_external_dependencies=True if step_by_step else exclude_external_dependencies,
            non_interactive=True if step_by_step else auto_approve,
            no_lock=no_lock,
            update=update,
            upgrade=upgrade,
            planfile=planfile,
            no_auto_approve=False if step_by_step else (not auto_approve),
            working_dir=None if step_by_step else working_dir,
            terragrunt_args=terragrunt_args,
            limit_parallelism=limit_parallelism,
            include_dirs=[] if step_by_step else include_dirs,
            exclude_dirs=[] if step_by_step else exclude_dirs,
        )

        if clean and not dry_run:
            self.clean(working_dir=working_dir)

        if step_by_step:
            self.printer.verbose(
                f'This command will be executed for each individual module:\n$ {cmd}'
                )

            self._run_di_graph(
                command=cmd,
                exclude_external_dependencies=exclude_external_dependencies,
                working_dir=working_dir,
                ask_for_confirmation=(not auto_approve),
                dry_run=dry_run,
                start_at_step=start_at_step,
                backwards=True if command.lower() in ['destroy'] else False,
                include_dirs=include_dirs,
                exclude_dirs=exclude_dirs,
            )
        else:
            if dry_run:
                self.printer.warning('In dry run mode, no real actions are executed!!')
            else:
                rc = subprocess.run(shlex.split(cmd))
                self.printer.verbose(rc)

                sys.exit(rc.returncode)

    def run_import(self, address, id, dry_run, working_dir, no_lock, terragrunt_args):
        """ Executes the terragrunt/terraform import command """

        self.printer.verbose(f"Attempting to execute 'run import'")
        if terragrunt_args:
            self.printer.verbose(f"- with additional parameters: {' '.join(terragrunt_args)}")

        check_for_file=self.TERRAGRUNT_FILE
        if working_dir:
            check_for_file = os.path.join(working_dir, check_for_file)
        if not os.path.isfile(check_for_file):
            self.printer.error(
                f"{check_for_file} not found, this seems not to be a terragrunt module directory!"
                )
            sys.exit(1)

        lock_stmt         = '-lock=false' if no_lock else ''
        working_dir_stmt  = f'--terragrunt-working-dir {working_dir}' if working_dir else ''

        cmd = f"terragrunt import {working_dir_stmt} {lock_stmt} {address} {id} {' '.join(terragrunt_args)}"
        cmd = re.sub(' +', ' ', cmd)
        self.printer.verbose(f'Full command to execute:\n$ {cmd}')

        if dry_run:
            self.printer.warning(f'In dry run mode, no real actions are executed!!')
        else:
            env = os.environ.copy()
            # TERRAGRUNT_SOURCE should not be present (or it should be a fully qualified path (which is typically not the case))
            try:
                value = env.pop('TERRAGRUNT_SOURCE')
                if value:
                    self.printer.verbose(
                        f'Terragrunt source environment variable with value {value} will be ignored'
                        )
            except KeyError:
                pass

            # the `posix=False` is to prevent the split command to remove quotes from strings,
            # e.g. when executing commands like this:
            # tgwrap import 'azuread_group.this["viewers"]' '123e4567-e89b-12d3-a456-426655440000'
            rc = subprocess.run(
                shlex.split(cmd, posix=False),
                env=env,
            )
            self.printer.verbose(rc)

    def analyze(self, exclude_external_dependencies, working_dir, start_at_step,
        out, analyze_config, parallel_execution,
        include_dirs, exclude_dirs, planfile_dir, terragrunt_args):
        """ Analyzes the plan files """

        self.printer.verbose("Attempting to 'analyze'")
        if terragrunt_args:
            self.printer.verbose(f"- with additional parameters: {' '.join(terragrunt_args)}")

        # determine whether we are going to use a native 'terraform show' (faster!) or need 
        # to use a terragrunt show
        if start_at_step > 1 or not exclude_external_dependencies or not planfile_dir:
            self.printer.verbose('Use terragrunt for module selection')

            use_native_terraform = False
            # first run a 'show' and write output to file
            cmd = self._construct_command(
                command='show',
                allow_no_run_all=True,
                exclude_external_dependencies=True,
                debug=False,
                terragrunt_args=terragrunt_args,
            )
        else:
            self.printer.verbose('Use native terraform for module selection')
            use_native_terraform = True
            cmd = f"terraform show -json {self.PLANFILE_NAME}"

        config = None
        if not analyze_config:
            self.printer.warning(
                f"Analyze  config file is not set, this is required for checking for unauthorized deletions and drift detection scores!"
                )
        else:
            self.printer.verbose(
                f"\nAnalyze using config {analyze_config}"
                )
            config = self.load_yaml_file(analyze_config)

        ts_validation_successful = True
        changes = {}
        drifts = {}
        try:
            # then run it and capture the output
            with tempfile.NamedTemporaryFile(mode='w+', prefix='tgwrap-', delete=False) as f:
                self.printer.verbose(f"Opened temp file for output collection: {f.name}")

                self._run_di_graph(
                    command=cmd,
                    dry_run=False, # no need for dryruns when analyzing
                    exclude_external_dependencies=exclude_external_dependencies,
                    collect_output_file=f,
                    working_dir=working_dir,
                    start_at_step=start_at_step,
                    ask_for_confirmation=False,
                    include_dirs=include_dirs,
                    exclude_dirs=exclude_dirs,
                    parallel_execution=parallel_execution,
                    use_native_terraform=use_native_terraform,
                    add_to_workdir=planfile_dir if use_native_terraform else None,
                )

            with open(f.name, 'r') as f:
                for line in f:
                    split_line = line.split(self.SEPARATOR)
                    module = split_line[0]

                    try:
                        plan_file = split_line[1]
                    except IndexError:
                        self.printer.warning(f'Could not determine planfile: {line[:100]}')


                    try:
                        # plan file could be empty (except for new line) if module is skipped
                        if len(plan_file) > 1:
                            data = json.loads(plan_file)

                            # do we have an exception logged?
                            if 'exception' in data:
                                raise Exception(data['exception'])

                            changes[module], ts_success = run_analyze(
                                config=config,
                                data=data,
                                verbose=self.printer.print_verbose,
                                )
                            if not ts_success:
                                ts_validation_successful = False
                        else:
                            self.printer.warning(f'Planfile for module {module} is empty')
                    except json.decoder.JSONDecodeError as e:
                        raise Exception(
                            f"Exception detected or planfile for {module} was not proper json, further analysis not possible:\n{plan_file[:200]}"
                            ) from e
        finally:
            os.remove(f.name)

        self.printer.header("Analysis results:", print_line_before=True)
        for key, value in changes.items():
            self.printer.header(f'Module: {key}')
            if not value["all"]:
                self.printer.success('No changes detected')
            if value["unauthorized"]:
                self.printer.error('Unauthorized deletions:')
                for m in value["unauthorized"]:
                    self.printer.error(f'-> {m}')
            if value["deletions"]:
                self.printer.warning('Deletions:')
                for m in value["deletions"]:
                    self.printer.warning(f'-> {m}')
            if value["creations"]:
                self.printer.normal('Creations:')
                for m in value["creations"]:
                    self.printer.normal(f'-> {m}')
            if value["updates"]:
                self.printer.normal('Updates:')
                for m in value["updates"]:
                    self.printer.normal(f'-> {m}')

        # calulate the total drifts and scoe
        total_drifts = {
            "minor": 0,
            "medium": 0,
            "major": 0,
            "unknown": 0,
            "total": 0,
        }

        for key, value in changes.items():
            for type in ["minor", "medium", "major", "unknown", "total"]:
                total_drifts[type] += value["drifts"][type]

        # the formula below is just a way to achieve a numeric results that is coming from the various drift categories
        total_drift_score = total_drifts['major'] * 10 + total_drifts['medium'] + total_drifts['minor'] / 10
        self.printer.header(f"Drift score: {total_drift_score} ({total_drifts['major']}.{total_drifts['medium']}.{total_drifts['minor']})")
        if total_drifts["unknown"] > 0:
            self.printer.warning(f"For {total_drifts['unknown']} resources, drift score is not configured, please update configuration!")
            self.printer.warning('- Unknowns:')
            for key, value in changes.items():
                for m in value["unknowns"]:
                    self.printer.warning(f' -> {m}')

        if out:
            # in the output we convert the dict of dicts to a list of dicts as it makes processing
            # (e.g. by telegraph) easier.
            changes_for_output = []
            for key, value in changes.items():
                value['module'] = key
                changes_for_output.append(value)

            print(json.dumps(changes_for_output, indent=4))

        if not ts_validation_successful:
            self.printer.error("Analysis detected unauthorised deletions, please check your configuration!!!")
            sys.exit(1)

    def set_lock(self, module, lock_status, auto_approve, dry_run, working_dir):
        """ Set the lock status of the stage you're in """
    
        # do we have a working dir?
        working_dir = working_dir if working_dir else os.getcwd()
        module_path = os.path.join(working_dir, module)

        command = "destroy" if lock_status == "unlock" else "apply" 

        self.run(
            command=command,
            dry_run=dry_run,
            auto_approve=auto_approve,
            working_dir=module_path,
            debug=False,
            clean=True,
            no_lock=False,
            update=False,
            planfile=None,
            terragrunt_args=[],
            )

    def sync(
        self, source_stage, target_stage, source_domain, target_domain, module,
        auto_approve, dry_run, clean, include_lock_file, working_dir, 
        ):
        """ Syncs the terragrunt config files from one stage to another (and possibly to a different domain) """
    
        if target_domain and not source_domain:
            raise Exception("Providing a target domain while omitting the source domain is not supported!")
        if source_domain and not target_domain:
            raise Exception("Providing a source domain while omitting the target domain is not supported!")

        if target_domain and not target_stage:
            self.printer.verbose(f"No target stage given, assume the same as source stage")
            target_stage=source_stage

        if not source_domain and not target_domain and not target_stage:
            raise Exception("When not providing domains, you need to provide a target stage!")

        # do we have a working dir?
        working_dir = working_dir if working_dir else os.getcwd()
        # the domains will be ignored when omitted as input
        source_path = os.path.join(working_dir, source_domain, source_stage, module, '')
        target_path = os.path.join(working_dir, target_domain, target_stage, module, '')

        self._run_sync(
            source_path=source_path,
            target_path=target_path,
            source_domain=source_domain,
            source_stage=source_stage,
            target_stage=target_stage,
            include_lock_file=include_lock_file,
            auto_approve=auto_approve,
            dry_run=dry_run,
            clean=clean,
            chmod_to_readonly=False,
        )

    def sync_dir(
        self, source_directory, target_directory,
        auto_approve, dry_run, clean, include_lock_file, working_dir, 
        ):
        """ Syncs the terragrunt config files from one directory to anothery """
    
        # do we have a working dir?
        working_dir = working_dir if working_dir else os.getcwd()
        # the domains will be ignored when omitted as input
        source_path = os.path.join(working_dir, source_directory, '')
        target_path = os.path.join(working_dir, target_directory, '')

        self._run_sync(
            source_path=source_path,
            target_path=target_path,
            include_lock_file=include_lock_file,
            auto_approve=auto_approve,
            dry_run=dry_run,
            clean=clean,
            chmod_to_readonly=False,
        )

    def deploy(
        self, manifest_file, version_tag, target_stages,
        include_global_config_files, auto_approve, dry_run, working_dir, 
        ):
        """ Deploys the terragrunt config files from a git repository """

        def get_directories(source_path):
            directories = []
            for root, dirs, files in os.walk(source_path):
                for dir in dirs:
                    directory_path = os.path.join(root, dir)
                    directories.append(os.path.basename(directory_path))
            return directories

        try:
            temp_dir = os.path.join(tempfile.mkdtemp(prefix='tgwrap-'), "tg-source")

            # do we have a working dir? 
            working_dir = working_dir if working_dir else os.getcwd()

            manifest = self.load_yaml_file(os.path.join(working_dir, manifest_file))

            source_dir = os.path.join(temp_dir, manifest['base_path'])

            # accept that the `config_path` is not set, only needed when deploying config files
            # and this will be checked later (if applicable)
            try:
                source_config_dir = os.path.join(temp_dir, manifest['config_path'])
            except KeyError:
                source_config_dir = None

            self._clone_repo(
                manifest=manifest,
                target_dir=temp_dir,
                version_tag=version_tag,
                )

            # collect all the base paths of the substacks as you don't want
            # to include them in regular syncs, add some standard paths there by default
            substacks = ['substacks', 'sub_stacks']
            for ss, substack in manifest.get('sub_stacks', {}).items():
                # get the base directory of the sub stack so that we can ignore it when deploying the regular modules
                substacks.append(substack['source'].split(os.path.sep)[0])

            substacks = set(substacks)

            for target_stage in target_stages:
                target_dir = os.path.join(working_dir, '', target_stage)
                self.printer.header(f'Deploy stage {target_stage} to {target_dir}...')
                try:
                    os.mkdir(target_dir)
                except FileExistsError:
                    pass

                deploy_actions = {}
                for key, value in manifest['deploy'].items():
                    if target_stage not in value['applies_to_stages']:
                        self.printer.verbose(f'Target stage {target_stage} not applicable for action {key}.')
                    else:
                        source_stage = value['source_stage']
                        self.printer.verbose(f'Found deployment step {key} using source stage {source_stage}')

                        source_path = os.path.join(source_dir, source_stage, value.get('source_dir', ''))
                        print(source_path)
                        source_modules = {
                            entry:{} for entry in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, entry))
                        }
                        self.printer.verbose(f'Found modules: {source_modules}')

                        include_modules = value['include_modules'] if len(value.get('include_modules', {})) > 0 else source_modules
                        self.printer.verbose(f'Include modules: {include_modules}')

                        # optionally, the moduels can be placed in another dir than the current
                        base_dir = value.get('base_dir', '')

                        for module, module_details in include_modules.items():
                            source_module = module_details.get('source', module)
                            target_module = module_details.get('target', module)

                            full_source_path = os.path.join(source_path, source_module, '')
                            full_target_path = os.path.join(target_dir, base_dir, target_module, '')

                            if not os.path.isfile(os.path.join(full_source_path, self.TERRAGRUNT_FILE)):
                                self.printer.warning(f'Module {source_module} seems substack and not a terragrunt module: skip it!')
                            elif source_module in value.get('exclude_modules', []) or source_module in substacks:
                                self.printer.verbose(f'Exclude module {source_module}')
                            else:
                                key = f'base -> {os.path.join(base_dir, module)}' if base_dir else module
                                deploy_actions[key] = {
                                    "source": full_source_path,
                                    "target": full_target_path,
                                }

                        config_dir = value.get('config_dir', None)
                        module_name = os.path.basename(os.getcwd())

                        if len(value.get('config_files', [])) > 0:
                            # run some checks and sets some variables
                            if not source_config_dir:
                                raise Exception("Config files must be deployed but 'config_path' variable is not set!")
                            elif not config_dir:
                                raise Exception("Config files must be deployed but 'config_dir' variable is not set!")

                            target_path = os.path.join(
                                target_dir, config_dir, module_name, target_stage, '',
                                )
                            # the target path might not exist
                            try:
                                os.mkdir(target_path)
                            except FileExistsError:
                                pass

                        for cf in value.get('config_files', []):
                            self.printer.verbose(f'Found config file : {cf}')

                            source_path = os.path.join(
                                source_config_dir, source_stage, cf
                                )
                            
                            full_target_path = os.path.dirname(os.path.join(target_path, cf))

                            if os.path.exists(source_path):
                                deploy_actions[f'configs -> {cf}'] = {
                                    "source": source_path,
                                    "target": full_target_path,
                                }
                            else:
                                self.printer.warning(f'Source path of config file does not exist: {source_path}')

                        for ss, substack in manifest.get('sub_stacks', {}).items():
                            self.printer.verbose(f'Found substack : {ss}')

                            source_path = os.path.join(
                                source_dir, source_stage, substack['source'], ''
                                )
                            target_path = os.path.join(
                                target_dir, substack['target'], ''
                                )

                            include_modules = substack['include_modules'] if len(substack.get('include_modules', {})) > 0 else []
                            self.printer.verbose(f'Include modules: {include_modules}')

                            if include_modules:
                                # get all directories in the substack and create an exlude_modules list from that
                                source_directories = get_directories(source_path)
                                exclude_modules = list(set(source_directories) - set(include_modules))
                                print("Dirs: ", include_modules, source_directories, source_path, exclude_modules)
                            else:
                                exclude_modules = substack.get('exclude_modules', [])
                            
                            if os.path.exists(source_path):
                                deploy_actions[f'substack -> {substack["target"]}'] = {
                                    "source": source_path,
                                    "target": target_path,
                                    "excludes": exclude_modules,
                                }
                            else:
                                self.printer.warning(f'Source path of substack does not exist: {source_path}')

                if include_global_config_files:
                    for gc, global_config in manifest.get('global_config_files', {}).items():
                        self.printer.verbose(f'Found global config : {gc}')

                        source_path = os.path.join(
                            source_dir, global_config['source']
                            )
                        target = global_config.get('target', global_config['source'])
                        target_path = os.path.dirname(
                            os.path.join(
                                working_dir, target,
                            )
                        )
                        if os.path.exists(source_path):
                            deploy_actions[f'global configs -> {target}'] = {
                                "source": source_path,
                                "target": target_path,
                            }
                        else:
                            self.printer.warning(f'Source path of global configs does not exist: {source_path}')
                else:
                    self.printer.verbose(f'Skipping global configs')

                self.printer.header('Modules to deploy:')
                self.printer.normal(f'-> git repository: {manifest["git_repository"]}')
                self.printer.normal(f'-> version tag: {version_tag}')
                self.printer.normal('Modules:')
                for key, value in deploy_actions.items():
                    self.printer.normal(f'--> {key}')

                if not auto_approve:
                    response = input("\nDo you want to continue? (y/N) ")
                    if response.lower() != "y":
                        sys.exit(1)

                for key, value in deploy_actions.items():
                    self._run_sync(
                        source_path=value['source'],
                        target_path=value['target'],
                        excludes=value.get('excludes', []),
                        include_lock_file=True,
                        auto_approve=True,
                        dry_run=dry_run,
                        clean=False,
                        chmod_to_readonly=True,
                    )

                if not dry_run:
                            # write the version file
                    with open(os.path.join(target_dir, self.VERSION_FILE), 'w') as f:
                        f.write(f"""
    locals {{
        version_tag="{version_tag}"
    }}
    """)

                    # clean up the cache in the deployed directory to avoid strange issues when planning
                    self.clean(working_dir=target_dir)

        except KeyError as e:
            self.printer.error(f'Error interpreting the manifest file. Please ensure it uses the proper format. Could not find element: {e}')
            sys.exit(1)
        except Exception as e:
            self.printer.error(f'Unexpected error: {e}')
            if self.printer.print_verbose:
                raise(e)
            sys.exit(1)
        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

    def check_deployments(self, manifest_file, working_dir, out):
        """ Check the freshness of deployed configuration versions against the platform repository """

        def locate_version_files(current_directory, found_files=[], root_directory=None, level=1):
            " This tries to find a version file in the current directory, or a given number of directories beneath it"

            if not root_directory:
                root_directory = current_directory

            for entry in os.listdir(current_directory):
                full_entry = os.path.join(current_directory, entry)
                if os.path.isdir(full_entry) and level < self.LOCATE_VERSION_FILE_MAX_LEVELS:
                    found_files = locate_version_files(
                        current_directory=full_entry,
                        found_files=found_files,
                        root_directory=root_directory,
                        level=level+1,
                    )
                elif entry == self.VERSION_FILE:
                    found_files.append(os.path.relpath(current_directory, root_directory))
                    
            return found_files

        def get_all_version(repo_dir, min_version=None):
            "Get all the version tags from the repo including their data"

            # Execute 'git tag' command to get a list of all tags
            cmd = "git tag --sort='-refname:short' --format='%(refname:short) %(creatordate:iso8601)'"
            output = subprocess.check_output(
                shlex.split(cmd),
                cwd=repo_dir,
                universal_newlines=True,
                )

            # Split the output into lines
            lines = output.strip().split('\n')

            # Iterate over the lines to extract tag names and creation dates
            timestamp_format = '%Y-%m-%d %H:%M:%S %z'
            tags = {}
            for line in lines:
                tag_name, created_date = line.split(' ', maxsplit=1)
                tags[tag_name] = {'created_date': datetime.strptime(created_date, timestamp_format)}

                if tag_name == min_version:
                    break

            self.printer.verbose(f'Found {len(tags)} tags: {tags}')

            return tags

        try:
            # do we have a working dir? 
            working_dir = working_dir if working_dir else os.getcwd()
            self.printer.header(f'Check released versions ({self.LOCATE_VERSION_FILE_MAX_LEVELS} levels) in directory: {working_dir}')

            result = locate_version_files(working_dir)

            versions = []
            for location in result:
                # Determine the deployed version as defined in the version file
                with open(os.path.join(working_dir, location, self.VERSION_FILE), 'r') as file:
                    content = hcl2.load(file)
                    try:
                        version_tag = content['locals'][0]['version_tag']
                        versions.append(
                            {
                                'path': location,
                                'tag': version_tag
                            }
                        )
                    except KeyError as e:
                        versions.append({location: 'unknown'})

            self.printer.verbose(f'Detected versions: {versions}')

            # remove the 'latest' tag from the detected versions, as it is specific one
            filtered_versions = list(filter(lambda x: x['tag'] != self.LATEST_VERSION, versions))

            if filtered_versions:
                min_version = min(filtered_versions, key=lambda x: x['tag'])
                max_version = max(filtered_versions, key=lambda x: x['tag'])
            else:
                min_version = None
                max_version = None

            self.printer.verbose(f'Detected minimum version {min_version} and maximum version {max_version}')

            temp_dir = os.path.join(tempfile.mkdtemp(prefix='tgwrap-'), "tg-source")
            manifest = self.load_yaml_file(os.path.join(working_dir, manifest_file))
            self._clone_repo(manifest=manifest, target_dir=temp_dir)

            # determine the version tag from the repo, including their date
            all_versions = get_all_version(repo_dir=temp_dir, min_version=min_version['tag'])

            # so now we can determine how old the deployed versions are
            now = datetime.now(timezone.utc)
            for version in versions:
                tag = version['tag']
                if tag == self.LATEST_VERSION:
                    version['release_date'] = 'unknown'
                else:
                    release_date = all_versions[tag]['created_date']
                    version['release_date'] = release_date
                    version['days_since_release'] = (now - release_date).days

            self.printer.header(
                'Deployed versions:' if len(versions) > 0 else 'No deployed versions detected'
                )
            
            for version in versions:
                days_since_release = version.get("days_since_release", 0)
                message = f'-> {version["path"]}: {version["tag"]} (released {days_since_release} days ago)'
                if version['release_date'] == 'unknown':
                    self.printer.normal(message)
                elif days_since_release > 60:
                    self.printer.error(message)
                elif days_since_release > 30:
                    self.printer.error(message)
                elif days_since_release < 7:
                    self.printer.success(message)
                else:
                    self.printer.normal(message)

            self.printer.normal("\n") # just to get an empty line :-/
            self.printer.warning("""
Note:
    This result only says something about the freshness of the deployed configurations,
    but not whether the actual resources are in sync with these.
    Check the drift of these configurations with the actual deployments by
    planning and analyzing the results.
            """)

            if out:
                # use the regular printer, to avoid it being sent to stderr
                print(json.dumps(versions, indent=4, cls=DateTimeEncoder))
    
        except KeyError as e:
            self.printer.error(f'Error interpreting the manifest file. Please ensure it uses the proper format. Could not find element: {e}')
            if self.printer.print_verbose:
                raise(e)
            sys.exit(1)
        except Exception as e:
            self.printer.error(f'Unexpected error: {e}')
            if self.printer.print_verbose:
                raise(e)
            sys.exit(1)
        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

    def show_graph(self, backwards, exclude_external_dependencies, working_dir, include_dirs, exclude_dirs, terragrunt_args):
        """ Shows the dependencies of a project """

        self.printer.verbose(f"Attempting to show dependencies")
        if terragrunt_args:
            self.printer.verbose(f"- with additional parameters: {' '.join(terragrunt_args)}")

        # self.printer.verbose(f"Include dirs: {'; '.join(include_dirs)}")
        # self.printer.verbose(f"Exclude dirs: {'; '.join(exclude_dirs)}")

        "Runs the desired command in the directories as defined in the directed graph"
        graph = self._get_di_graph(backwards=backwards, working_dir=working_dir)

        # first go through the groups and clean up where needed
        groups = self._prepare_groups(
            graph=graph,
            exclude_external_dependencies=exclude_external_dependencies,
            working_dir=working_dir,
            include_dirs=include_dirs,
            exclude_dirs=exclude_dirs,
            )

        if not groups:
            self.printer.error('No groups in scope, this smells fishy!')
        else:
            self.printer.header("The following groups are in scope:")
            for idx, group in enumerate(groups):
                self.printer.normal(f"\nGroup {idx+1}:")
                for directory in group:
                    self.printer.normal(f"- {directory}")

    def clean(self, working_dir):
        """ Clean the temporary files of a terragrunt/terraform project """

        cmd = 'find . -name ".terragrunt-cache" -type d -exec rm -rf {} \; ; find . -name ".terraform" -type d -exec rm -rf {} \;'
        # we see the behaviour that with cleaning up large directories, it returns errorcode=1 upon first try
        # never to shy away from a questionable solution to make your life easier, we just run it again :-)
        rc = 'clean up not started!'
        for check in [False, True]:
            rc = subprocess.run(
                cmd,
                shell=True,
                check=check,
                stdout=sys.stdout if self.printer.print_verbose else subprocess.DEVNULL,
                stderr=sys.stderr if self.printer.print_verbose else subprocess.DEVNULL,
                cwd=working_dir if working_dir else None,
                )
        self.printer.verbose(rc)
        self.printer.normal("Cleaned the temporary files")

    def change_log(self, changelog_file, working_dir, include_nbr_of_releases):
        """ Generate a change log """

        # Run 'git log' to capture the Git log as a string
        cmd = "git log --oneline --decorate --abbrev-commit"
        output = subprocess.check_output(
            shlex.split(cmd),
            text=True,
            cwd=working_dir if working_dir else None,
            )

        # Define a regular expression pattern to extract release tags
        # The following formats are supported:
        #  vYYYY.MM.DD
        #  vYYYYMMDD
        #  vYYYY.MM.DD.01
        #  vYYYYMMDD.01
        release_pattern = r'\b(v\d{4}\.?\d{1,2}\.?\d{1,2}(\.\d+)?)\b'

        # Split the Git log into individual commit entries
        release_commits = {}
        commit_entries = output.strip().split('\n')

        current_release = None
        for entry in commit_entries:
            # Check if the entry contains a release tag
            match = re.search(release_pattern, entry)
            if match:
                current_release = match.group(1)
                if current_release not in release_commits:
                    release_commits[current_release] = []
            elif current_release:
                release_commits[current_release].append(entry)
        # Print the grouped commits to the console (you can write them to a file as needed)
        changelog = ""
        counter = 0
        for release, commits in release_commits.items():
            if len(commits) > 0:
                counter += 1

                changelog = changelog + f"\nRelease: {release}\n  - "
                changelog = changelog + '\n  - '.join(commits) + '\n'

            if include_nbr_of_releases and counter > include_nbr_of_releases:
                break

        # do we need to update an existingchange log file?
        if changelog_file:
            # print the content only in verbose mode
            self.printer.verbose(changelog)

            with open(changelog_file, "r") as f:
                existing_content = f.read()

            start_marker = '<!-- BEGINNING OF OF TGWRAP CHANGELOG SECTION -->'
            end_marker = '<!-- END OF TGWRAP CHANGELOG SECTION -->'

            # Find the start and end positions of the dynamic section
            start_position = existing_content.find(start_marker)
            end_position = existing_content.find(end_marker)

            # Check if both markers are found in the content
            if start_position != -1 and end_position != -1:
                # Replace the dynamic section with the new change log
                updated_content = (
                    existing_content[:start_position]
                    + start_marker
                    + "\n"
                    + changelog
                    + end_marker
                    + existing_content[end_position + len(end_marker):]
                )

                # Step 4: Save the updated content back to the same file
                with open(changelog_file, "w") as f:
                    f.write(updated_content)

                self.printer.normal(f"Change log file {changelog_file} updated successfully.")
            else:
                self.printer.error("Markers not found in changelog file {changelog_file}. Please check the file structure.")
        else:
            # use the regular printer, to avoid it being sent to stderr
            print(changelog)

