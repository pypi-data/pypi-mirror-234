#!/usr/bin/env python3

"""
This script simply wraps terragrunt (which is a wrapper around terraform...)
and its main function is to allow you to execute a `run-all` command but
broken up in individual steps.

This makes debugging a complex project easier, such as spotting where the
exact problem is.
"""

import sys
import os
from importlib.metadata import version, PackageNotFoundError

import click

from outdated import check_outdated

from .main import TgWrap

PACKAGE_NAME = 'tgwrap'
try:
    __version__ = version(PACKAGE_NAME)
except PackageNotFoundError:
    __version__ = '0.0.0'

def check_latest_version(verbose=False):
    """ check for later versions on pypi """
    def echo(msg):
        if not os.getenv('OUTDATED_IGNORE'):
            click.secho(msg, bold=True, file=sys.stderr)

    try:
        is_outdated, latest_version = check_outdated(PACKAGE_NAME, __version__)
        if is_outdated:
            echo(f'Your local version ({__version__}) is out of date! Latest is {latest_version}!')
        elif verbose:
            echo(f'You are running version {__version__}, latest is {latest_version}')

    except ValueError:
        # this happens when your local version is ahead of the pypi version,
        # which happens only in development
        pass
    except KeyError:
        echo('Could not determine package version, continue nevertheless.')
        pass

CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

TG_COMMANDS=[
    'init', 'validate', 'validate-inputs', 'plan', 'apply',
    'destroy', 'info', 'output', 'show',
    ]
STAGES=['global', 'sbx', 'dev', 'qas', 'run', 'tst', 'acc', 'prd']
class DefaultGroup(click.Group):
    '''
    Allow a default command for a group
    '''
    ignore_unknown_options = True

    def __init__(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', None)
        super().__init__(*args, **kwargs)
        self.default_cmd_name = None
        if default_command is not None:
            self.set_default_command(default_command)

    def set_default_command(self, command):
        """ Sets the command that can be omitted (and is considered default) """
        if isinstance(command, str):
            cmd_name = command
        else:
            cmd_name = command.name
            self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        if not args and self.default_cmd_name is not None:
            args.insert(0, self.default_cmd_name)
        return super().parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands and self.default_cmd_name is not None:
            ctx.args0 = cmd_name
            cmd_name = self.default_cmd_name
        return super().get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        args0 = getattr(ctx, 'args0', None)
        if args0 is not None:
            args.insert(0, args0)
        return cmd_name, cmd, args

@click.group(
    cls=DefaultGroup,
    default_command="run",
    context_settings=CLICK_CONTEXT_SETTINGS,
)
def main():
    pass

@main.command(
    name="run",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument('command', type=click.Choice(TG_COMMANDS + ['state', 'render-json']))
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--debug', '-d', is_flag=True, default=False,
    help='Run the terragrunt command with debug logging enabled (where applicable)',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed (only in combination with step-by-step mode)',
    show_default=True
    )
@click.option('--no-lock', '-n', is_flag=True, default=False,
    help='Do not apply a lock while executing the command (or set the TGWRAP_NO_LOCK environment variable, only applicable with plan)',
    envvar='TGWRAP_NO_LOCK', show_default=True,
    )
@click.option('--update', '-u', is_flag=True, default=False,
    help='Updates the source (and/or provider if applicable)',
    show_default=True
    )
@click.option('--upgrade', '-U', is_flag=True, default=False,
    help='Installs the latest provider versions (init only)',
    show_default=True
    )
@click.option('--planfile', '-p', is_flag=True, default=False,
    help='Use the generated planfile when applying the changes',
    show_default=True
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--clean', '-c', is_flag=True, default=False,
    help='Clean up .terragrunt-cache before executing the command',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.argument('terragrunt-args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def run(command, verbose, debug, dry_run, no_lock, update, upgrade,
    planfile, auto_approve, clean, working_dir, terragrunt_args):
    """ [default] Executes a terragrunt command on a single project """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose, check_tg_source=True)
    tgwrap.run(
        command=command,
        debug=debug,
        dry_run=dry_run,
        no_lock=no_lock,
        update=update,
        upgrade=upgrade,
        planfile=planfile,
        auto_approve=auto_approve,
        clean=clean,
        working_dir=working_dir,
        terragrunt_args=terragrunt_args,
    )

@main.command(
    name="run-all",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument('command', type=click.Choice(TG_COMMANDS))
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--debug', '-d', is_flag=True, default=False,
    help='Run the terragrunt command with debug logging enabled (where applicable)',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed (only in combination with step-by-step mode)',
    show_default=True
    )
@click.option('--no-lock', '-n', is_flag=True, default=False,
    help='Do not apply a lock while executing the command (or set the TGWRAP_NO_LOCK environment variable, only applicable with plan)',
    envvar='TGWRAP_NO_LOCK', show_default=True,
    )
@click.option('--update', '-u', is_flag=True, default=False,
    help='Updates the source (and/or provider if applicable)',
    show_default=True
    )
@click.option('--upgrade', '-U', is_flag=True, default=False,
    help='Installs the latest provider versions (init only)',
    show_default=True
    )
@click.option('--exclude-external-dependencies/--include-external-dependencies', '-x/-i',
    is_flag=True, default=True,
    help='Whether or not external dependencies must be ignored',
    show_default=True
    )
@click.option('--step-by-step', '-s', is_flag=True, default=False,
    help='Run the command step by step and stop when an error occurs (where applicable)',
    show_default=True
    )
@click.option('--planfile', '-p', is_flag=True, default=False,
    help='Use the generated planfile when applying the changes',
    show_default=True
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--clean', '-c', is_flag=True, default=False,
    help='Clean up .terragrunt-cache before executing the command',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.option('--start-at-step', '-S', type=float, default=1.0,
    help='When running in step-by-step mode, start processing at the given step number',
    )
@click.option('--limit-parallelism', '-l', type=int, default=None,
    help='Limit the parallelism to the given number, unlimitted if omitted',
    )
@click.option('--include-dir', '-I',
    multiple=True, default=[],
    help='A glob of a directory that needs to be included, this option can be used multiple times. For example: -I "integrations/\*/\*"',
    show_default=True
    )
@click.option('--exclude-dir', '-E',
    multiple=True, default=[],
    help='A glob of a directory that needs to be excluded, this option can be used multiple times. For example: -E "integrations/\*/\*"',
    show_default=True,
    )
@click.argument('terragrunt-args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def run_all(command, verbose, debug, dry_run, no_lock, update, upgrade, exclude_external_dependencies,
    step_by_step, planfile, auto_approve, clean, working_dir, start_at_step,
    limit_parallelism, include_dir, exclude_dir, terragrunt_args):
    """ Executes a terragrunt command across multiple projects """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose, check_tg_source=True)
    tgwrap.run_all(
        command=command,
        debug=debug,
        dry_run=dry_run,
        no_lock=no_lock,
        update=update,
        upgrade=upgrade,
        exclude_external_dependencies=exclude_external_dependencies,
        step_by_step=step_by_step,
        planfile=planfile,
        auto_approve=auto_approve,
        clean=clean,
        working_dir=working_dir,
        start_at_step=start_at_step,
        limit_parallelism=limit_parallelism,
        include_dirs=include_dir,
        exclude_dirs=exclude_dir,
        terragrunt_args=terragrunt_args,
    )

@main.command(
    name="import",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--address', '-a', required=True,
    help='Terraform resource address',
    )
@click.option('--id', '-i', required=True,
    help='Id of the resource to be imported',
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.option('--no-lock', '-n', is_flag=True, default=False,
    help='Do not apply a lock while executing the command (or set the TGWRAP_NO_LOCK environment variable, only applicable with plan)',
    envvar='TGWRAP_NO_LOCK', show_default=True,
    )
@click.argument('terragrunt-args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def run_import(address, id, verbose, dry_run, working_dir, no_lock, terragrunt_args):
    """ Executes the terragrunt/terraform import command """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.run_import(
        address=address,
        id=id,
        dry_run=dry_run,
        working_dir=working_dir,
        no_lock=no_lock,
        terragrunt_args=terragrunt_args,
    )

@main.command(
    name="analyze",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--exclude-external-dependencies/--include-external-dependencies', '-x/-i',
    is_flag=True, default=True,
    help='Whether or not external dependencies must be ignored',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.option('--start-at-step', '-S', type=float, default=1.0,
    help='When running in step-by-step mode, start processing at the given step number',
    )
@click.option('--out', '-o', is_flag=True, default=False,
    help='Show output as json',
    show_default=True
    )
@click.option('--analyze-config', '-A', default=None,
    help='Name of the analyze config file (or set TGWRAP_ANALYZE_CONFIG environment variable)',
    envvar='TGWRAP_ANALYZE_CONFIG', type=click.Path(),
    )
@click.option('--parallel-execution', '-p', is_flag=True, default=False,
    help='Whether or not to use parallel execution',
    )
@click.option('--include-dir', '-I',
    multiple=True, default=[],
    help='A glob of a directory that needs to be included, this option can be used multiple times. For example: -I "integrations/\*/\*"',
    show_default=True
    )
@click.option('--exclude-dir', '-E',
    multiple=True, default=[],
    help='A glob of a directory that needs to be excluded, this option can be used multiple times. For example: -E "integrations/\*/\*"',
    show_default=True,
    )
@click.option('--planfile-dir', '-P', default=None,
    help='Relative path to directory with plan file (or set TGWRAP_PLANFILE_DIR environment variable), see README for more details',
    envvar='TGWRAP_PLANFILE_DIR', type=click.Path(),
    )
@click.argument('terragrunt-args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def run_analyze(verbose, exclude_external_dependencies, working_dir, start_at_step,
            out, analyze_config, parallel_execution,
            include_dir, exclude_dir, planfile_dir, terragrunt_args):
    """ Analyzes the plan files """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.analyze(
        exclude_external_dependencies=exclude_external_dependencies,
        working_dir=working_dir,
        start_at_step=start_at_step,
        out=out,
        analyze_config=analyze_config,
        parallel_execution=parallel_execution,
        include_dirs=include_dir,
        exclude_dirs=exclude_dir,
        planfile_dir=planfile_dir,
        terragrunt_args=terragrunt_args,
    )

@main.command(
    name="lock",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--module', '-m', required=True,
    help='Name of the locking module (or set TGWRAP_LOCK_MODULE environment variable)',
    envvar='TGWRAP_LOCK_MODULE'
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is assumed to be your stage is the target',
    )
@click.version_option(version=__version__)
def lock(module, auto_approve, verbose, dry_run, working_dir):
    """ Lock a particular stage """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose, check_tg_source=True)
    tgwrap.set_lock(
        module=module,
        lock_status="lock",
        auto_approve=auto_approve,
        dry_run=dry_run,
        working_dir=working_dir,
    )

@main.command(
    name="unlock",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--module', '-m', required=True,
    help='Name of the locking module (or set TGWRAP_LOCK_MODULE environment variable)',
    envvar='TGWRAP_LOCK_MODULE'
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is assumed to be your stage is the target',
    )
@click.version_option(version=__version__)
def unlock(module, auto_approve, verbose, dry_run, working_dir):
    """ Unlock a particular stage """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose, check_tg_source=True)
    tgwrap.set_lock(
        module=module,
        lock_status="unlock",
        auto_approve=auto_approve,
        dry_run=dry_run,
        working_dir=working_dir,
    )

@main.command(
    name="sync",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--source-domain', '-S', default="",
    help='Source domain of config files, when omitted the DLZ where you run this command is assumed.',
    )
@click.option('--target-domain', '-T', default="",
    help='Target domain where config files will be copied to, when omitted the DLZ where you run this command is assumed.',
    )
@click.option('--source-stage', '-s', required=True,
    type=click.Choice(STAGES, case_sensitive=True),
    help='Source stage of config files',
    )
@click.option('--target-stage', '-t',
    type=click.Choice(STAGES, case_sensitive=True),
    help='Target of config files',
    )
@click.option('--module', '-m', default="",
    help='Name of the module, if omitted all modules will be copied.',
    )
@click.option('--clean', '-c', is_flag=True, default=False,
    help='Clean up files on target side that do not exist as source',
    show_default=True
    )
@click.option('--include-lock-file', '-i', is_flag=True, default=False,
    help='Include the terraform lock file',
    show_default=True
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.version_option(version=__version__)
def sync(
    source_domain, source_stage, target_domain, target_stage, module, auto_approve,
    verbose, dry_run, clean, include_lock_file, working_dir
    ):
    """ Syncs the terragrunt config files from one stage to another (and possibly to a different domain) """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.sync(
        source_domain=source_domain,
        source_stage=source_stage,
        target_domain=target_domain,
        target_stage=target_stage,
        module=module,
        auto_approve=auto_approve,
        dry_run=dry_run,
        clean=clean,
        include_lock_file=include_lock_file,
        working_dir=working_dir,
    )

@main.command(
    name="sync-dir",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--source-directory', '-s', required=True,
    help='Directory where source config files reside.',
    )
@click.option('--target-directory', '-t', required=True,
    help='Directory where config files will be synced to.',
    )
@click.option('--clean', '-c', is_flag=True, default=False,
    help='Clean up files on target side that do not exist as source',
    show_default=True
    )
@click.option('--include-lock-file', '-i', is_flag=True, default=False,
    help='Include the terraform lock file',
    show_default=True
    )
@click.option('--auto-approve', '-a', is_flag=True, default=False,
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    show_default=True
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--dry-run', '-D', is_flag=True, default=False,
    help='dry-run mode, no real actions are executed',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.version_option(version=__version__)
def sync_dir(
    source_directory, target_directory, auto_approve,
    verbose, dry_run, clean, include_lock_file, working_dir
    ):
    """ Syncs the terragrunt config files from one directory to anothery """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.sync_dir(
        source_directory=source_directory,
        target_directory=target_directory,
        auto_approve=auto_approve,
        dry_run=dry_run,
        clean=clean,
        include_lock_file=include_lock_file,
        working_dir=working_dir,
    )

@main.command(
    name="deploy",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--manifest-file', '-m',
    help='Manifest file describing the deployment options',
    required=True, default="manifest.yaml", show_default=True,
    type=click.Path(),
    )
@click.option('--version-tag', '-V',
    help="Version tag, use 'latest' to, well, get the latest version.",
    required=True, default='latest', show_default=True,
    )
@click.option('--target-stage', '-t',
    multiple=True,
    help='Stage to deploy to',
    type=click.Choice(STAGES, case_sensitive=True), required=True,
    )
@click.option('--include-global-config-files/--exclude-global-config-files', '-i/-x',
    help='Whether or not to include deploying the (in the manifest specified) global config files',
    is_flag=True, default=True, show_default=True,
    )
@click.option('--auto-approve', '-a',
    help='Do not ask for confirmation before applying planned changes (where applicable)',
    is_flag=True, default=False, show_default=True,
    )
@click.option('--verbose', '-v',
    help='Verbose printing',
    is_flag=True, default=False, show_default=True,
    )
@click.option('--dry-run', '-D',
    help='dry-run mode, no real actions are executed',
    is_flag=True, default=False, show_default=True,
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.version_option(version=__version__)
def deploy(
    manifest_file, version_tag, target_stage, include_global_config_files,
    auto_approve, verbose, dry_run, working_dir
    ):
    """ Deploys the terragrunt config files from a git repository """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.deploy(
        manifest_file=manifest_file,
        version_tag=version_tag,
        target_stages=target_stage,
        include_global_config_files=include_global_config_files,
        auto_approve=auto_approve,
        dry_run=dry_run,
        working_dir=working_dir,
    )

@main.command(
    name="check-deployments",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--manifest-file', '-m',
    help='Manifest file describing the deployment options',
    required=True, default="manifest.yaml", show_default=True,
    type=click.Path(),
    )
@click.option('--verbose', '-v',
    help='Verbose printing',
    is_flag=True, default=False, show_default=True,
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.option('--out', '-o', is_flag=True, default=False,
    help='Show output as json',
    show_default=True
    )
@click.version_option(version=__version__)
def check_deployments(manifest_file, verbose, working_dir, out):
    """ Check the freshness of deployed configuration versions against the platform repository """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.check_deployments(
        manifest_file=manifest_file,
        working_dir=working_dir,
        out=out,
    )

@main.command(
    name="show-graph",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--backwards', '-b',
    is_flag=True, default=False,
    help='Whether or not the graph must be shown backwards',
    show_default=True
    )
@click.option('--exclude-external-dependencies/--include-external-dependencies', '-x/-i',
    is_flag=True, default=True,
    help='Whether or not external dependencies must be ignored',
    show_default=True
    )
@click.option('--include-dir', '-I',
    multiple=True, default=[],
    help='A glob of a directory that needs to be included, this option can be used multiple times. For example: -I "integrations/\*/\*"',
    show_default=True
    )
@click.option('--exclude-dir', '-E',
    multiple=True, default=[],
    help='A glob of a directory that needs to be excluded, this option can be used multiple times. For example: -E "integrations/\*/\*"',
    show_default=True,
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.argument('terragrunt-args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(version=__version__)
def show_graph(verbose, backwards, exclude_external_dependencies, working_dir, include_dir, exclude_dir, terragrunt_args):
    """ Shows the dependencies of a project """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose, check_tg_source=True)
    tgwrap.show_graph(
        backwards=backwards,
        exclude_external_dependencies=exclude_external_dependencies,
        working_dir=working_dir,
        include_dirs=include_dir,
        exclude_dirs=exclude_dir,
        terragrunt_args=terragrunt_args,
    )

@main.command(
    name="clean",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.version_option(version=__version__)
def clean(verbose, working_dir):
    """ Clean the temporary files of a terragrunt/terraform project """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.clean(
        working_dir=working_dir,
    )

@main.command(
    name="change-log",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option('--changelog-file', '-c',
    help='Existing change log file, if passed the content will be included in the given file',
    required=False,
    type=click.Path(),
    )
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose printing',
    show_default=True
    )
@click.option('--working-dir', '-w', default=None,
    help='Working directory, when omitted the current directory is used',
    )
@click.option('--include-nbr-of-releases', '-i',
    type=int, default=20, show_default=True,
    help='Max number of releases to include',
    )
@click.version_option(version=__version__)
def change_log(changelog_file, verbose, working_dir, include_nbr_of_releases):
    """ Experimental! Generate a change log """

    check_latest_version(verbose)

    tgwrap = TgWrap(verbose=verbose)
    tgwrap.change_log(
        changelog_file=changelog_file,
        working_dir=working_dir,
        include_nbr_of_releases=include_nbr_of_releases,
    )

# this is needed for the vscode debugger to work
if __name__ == '__main__':
    main()
