# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>


def instance_connect_timeout():
    return 10


def instance_database_instance_collection_interval():
    return False


def instance_dbm():
    return False


def instance_disable_generic_tags():
    return False


def instance_empty_default_hostname():
    return False


def instance_log_unobfuscated_plans():
    return False


def instance_log_unobfuscated_queries():
    return False


def instance_max_custom_queries():
    return 20


def instance_min_collection_interval():
    return 15


def instance_only_custom_queries():
    return False


def instance_port():
    return 3306


def instance_use_global_custom_queries():
    return 'true'