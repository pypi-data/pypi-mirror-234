"""
This is based on the venerable [terrasafe](https://github.com/PrismeaOpsTeam/Terrasafe)
but we got more and more need for customisation hence we decided to clone it. Thanks guys!
"""

import os
import fnmatch
import re

from .printer import Printer

def run_analyze(config, data, verbose=False):
    """ Run the terrasafe validation and return the unauthorized deletions """

    printer = Printer(verbose)

    changes = {
        "drifts": {
            "minor": 0,
            "medium": 0,
            "major": 0,
            "unknown": 0,
            "total": 0,
        },
        "all": [],
        "creations" : [],
        "updates" : [],
        "deletions" : [],
        "unauthorized" : [],
        "unknowns" : [],
    }

    ignored_from_env_var = parse_ignored_from_env_var()

    detected_changes = get_resource_actions(data)

    if config:
        ts_default_levels =  {
            'low': 'ignore_deletion',
            'medium': 'ignore_deletion_if_recreation',
            'high': 'unauthorized_deletion',
            }
        ts_config = {}
        for criticallity, ts_level in ts_default_levels.items():
            ts_config[ts_level] = [f"*{key}*" for key, value in config[criticallity].items() if value.get('terrasafe_level', ts_level) == ts_level]

        for resource in detected_changes['deletions']:
            resource_address = resource["address"]
            if is_resource_match_any(resource_address, ts_config["unauthorized_deletion"]):
                printer.verbose(f'Resource {resource_address} can not be destroyed for any reason')
            if is_resource_match_any(resource_address, ts_config["ignore_deletion"]):
                continue
            if is_resource_recreate(resource) and is_resource_match_any(
                resource_address,
                ts_config["ignore_deletion_if_recreation"]
                ):
                continue
            if is_resource_match_any(resource_address, ignored_from_env_var):
                printer.verbose(f"deletion of {resource_address} authorized by env var.")
                continue
            if is_deletion_in_disabled_file(resource["type"], resource["name"]):
                printer.verbose(f"deletion of {resource_address} authorized by disabled file feature")
                continue
            changes['unauthorized'].append(resource_address)

        if changes['unauthorized']:
            printer.verbose("Unauthorized deletion detected for those resources:")
            for deletion in changes['unauthorized']:
                printer.verbose(f" - {deletion}")
            printer.verbose("If you really want to delete those resources: comment it or export this environment variable:")
            printer.verbose(f"export TERRASAFE_ALLOW_DELETION=\"{';'.join(changes['unauthorized'])}\"")

        dd_default_levels =  {
            'low': {
                'default': 'minor',
                'delete': 'medium',
            },
            'medium': {
                'default': 'medium',
                'delete': 'major',
            },
            'high': {
                'default': 'major',
                'update': 'medium',
            },
        }
        dd_config = {}
        for criticallity, settings in dd_default_levels.items():
            # first get the proper value for each action
            create = settings.get('create', settings.get('default'))
            update = settings.get('update', settings.get('default'))
            delete = settings.get('delete', settings.get('default'))

            # then see if there are overrides for specific resources in the config file
            for key, value in config[criticallity].items():
                # as a first step, use the defaults for the module
                modified_key=f"*{key}*"
                dd_config[modified_key] = {
                    'create': create,
                    'update': update,
                    'delete': delete,
                }
                if 'drift_impact' in value:
                    # see if the resource wants to override the default values
                    dd_config[modified_key] = {
                        'create': value['drift_impact'].get('create', create),
                        'update': value['drift_impact'].get('update', update),
                        'delete': value['drift_impact'].get('delete', delete),
                    }

        # now we have the proper lists, calculate the drifts
        for key, value in {'deletions': 'delete', 'creations': 'create', 'updates': 'update'}.items():
            for resource in detected_changes[key]:
                resource_address = resource["address"]
    
                has_match, resource_config = get_matching_dd_config(resource_address, dd_config)
                if has_match:
                    # so what drift classification do we have?
                    dd_class = resource_config[value]
                    changes['drifts'][dd_class] += 1
                else:
                    changes['drifts']['unknown'] += 1
                    if resource_address not in changes['unknowns']:
                        changes['unknowns'].append(resource_address)

                changes['drifts']['total'] += 1

    # remove ballast from the following lists
    changes['all'] = [ # ignore read and no-ops
        resource["address"] for resource in detected_changes['all']
        if (not 'no-op' in resource["change"]["actions"] and not 'read' in resource["change"]["actions"])
        ]
    changes['deletions'] = [ # ignore deletions that are already in the unauthorized list
        resource["address"] for resource in detected_changes['deletions']
        if resource["address"] not in changes['unauthorized']
        ]
    changes['creations'] = [resource["address"] for resource in detected_changes['creations']]
    changes['updates'] = [resource["address"] for resource in detected_changes['updates']]

    return changes, (not changes['unauthorized'])


def parse_ignored_from_env_var():
    ignored = os.environ.get("TERRASAFE_ALLOW_DELETION")
    if ignored:
        return ignored.split(";")
    return []


def get_resource_actions(data):
    # check format version
    if data["format_version"].split(".")[0] != "0" and data["format_version"].split(".")[0] != "1":
        raise Exception("Only format major version 0 or 1 is supported")

    if "resource_changes" in data:
        resource_changes = data["resource_changes"]
    else:
        resource_changes = []

    changes = {
        'all': resource_changes,
        'deletions': list(filter(has_delete_action, resource_changes)),
        'creations': list(filter(has_create_action, resource_changes)),
        'updates': list(filter(has_update_action, resource_changes)),
    }

    return changes


def has_delete_action(resource):
    return "delete" in resource["change"]["actions"]


def has_create_action(resource):
    return "create" in resource["change"]["actions"]


def has_update_action(resource):
    return "update" in resource["change"]["actions"]


def is_resource_match_any(resource_address, pattern_list):
    for pattern in pattern_list:
        pattern = re.sub(r"\[(.+?)\]", "[[]\g<1>[]]", pattern)
        if fnmatch.fnmatch(resource_address, pattern):
            return True
    return False


def get_matching_dd_config(resource_address, dd_config):
    for pattern, config in dd_config.items():
        pattern = re.sub(r"\[(.+?)\]", "[[]\g<1>[]]", pattern)
        if fnmatch.fnmatch(resource_address, pattern):
            return True, config
    return False, None

# 1 \*databricks_dbfs_file* {'create': 'minor', 'update': 'minor', 'delete': 'minor'}
# 2 \*databricks_dbfs_file* module.dbx_ws_conf.databricks_dbfs_file.spark_jars["spark-listeners-loganalytics_3.1.1_2.12-1.0.0.jar"]


def is_resource_recreate(resource):
    actions = resource["change"]["actions"]
    return "create" in actions and "delete" in actions


def is_deletion_in_disabled_file(resource_type, resource_name):
    regex = re.compile(rf'\s*resource\s*\"{resource_type}\"\s*\"{resource_name}\"')
    tf_files = get_all_files(".tf.disabled")
    for filepath in tf_files:
        with open(filepath, 'r') as file:
            for line in file:
                if regex.match(line):
                    return True


def get_all_files(extension):
    res = []
    for root, dirs, file_names in os.walk("."):
        for file_name in file_names:
            if fnmatch.fnmatch(file_name, "*" + extension):
                res.append(os.path.join(root, file_name))
    return res
