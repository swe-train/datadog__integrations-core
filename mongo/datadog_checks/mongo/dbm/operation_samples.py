# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)


import time
from typing import Dict, List, Optional

from bson import json_util

try:
    import datadog_agent
except ImportError:
    from datadog_checks.base.stubs import datadog_agent

from datadog_checks.base.utils.db.sql import compute_exec_plan_signature
from datadog_checks.base.utils.db.utils import DBMAsyncJob
from datadog_checks.base.utils.tracking import tracked_method
from datadog_checks.mongo.common import ReplicaSetDeployment

from .types import (
    OperationActivityEvent,
    OperationSampleActivityRecord,
    OperationSampleClient,
    OperationSampleEvent,
    OperationSampleOperationMetadata,
    OperationSampleOperationStats,
    OperationSamplePlan,
)


class MongoDbExplainExceptionBase(Exception):
    pass


SAMPLE_EXCLUDE_KEYS = {
    "statement",
    "application",
    "dbname",
    "user",
    "client",
}


def agent_check_getter(self):
    return self._check


class MongoOperationSamples(DBMAsyncJob):
    def __init__(self, check):
        self._operation_samples_config = check._config.operation_samples
        self._collection_interval = self._operation_samples_config["collection_interval"]

        super(MongoOperationSamples, self).__init__(
            check,
            rate_limit=1 / self._collection_interval,
            run_sync=not self._operation_samples_config.get("async", False),  # Default to running sync
            enabled=self._operation_samples_config["enabled"],
            dbms="mongodb",
            min_collection_interval=check._config.min_collection_interval,
            job_name="operation-samples",
        )

    def run_job(self):
        self.collect_operation_samples()

    @tracked_method(agent_check_getter=agent_check_getter)
    def collect_operation_samples(self):
        if not self._should_collect_operation_samples():
            return

        now = time.time()

        activities = []

        for activity, sample in self._get_operation_samples(now):
            self._check.log.debug("Sending operation sample: %s", sample)
            self._check.database_monitoring_query_sample(json_util.dumps(sample))
            activities.append(activity)

        activities_payload = self._create_activities_payload(now, activities)
        self._check.log.debug("Sending activities payload: %s", activities_payload)
        self._check.database_monitoring_query_activity(json_util.dumps(activities_payload))

    def _should_collect_operation_samples(self) -> bool:
        deployment = self._check.api_client.deployment_type
        if isinstance(deployment, ReplicaSetDeployment) and deployment.is_arbiter:
            self._check.log.debug("Skipping operation samples collection on arbiter node")
            return False
        return True

    def _get_operation_samples(self, now):
        for operation in self._get_current_op():
            try:
                if not self._should_include_operation(operation):
                    continue

                command = operation.get("command")
                obfuscated_command = datadog_agent.obfuscate_mongodb_string(json_util.dumps(command))
                query_signature = self._get_query_signature(obfuscated_command)
                operation_metadata = self._get_operation_metadata(operation)

                activity = self._create_activity(
                    now, operation, operation_metadata, obfuscated_command, query_signature
                )

                explain_plan = self._get_explain_plan(op=operation.get("op"), command=command)
                sample = self._create_operation_sample_payload(
                    now, operation_metadata, obfuscated_command, query_signature, explain_plan, activity
                )
                yield activity, sample
            except Exception as e:
                self._check.log.error("Unexpected error while collecting operation samples: %s", e)
                continue

    def _get_current_op(self):
        operations = self._check.api_client.current_op()
        for operation in operations:
            self._check.log.debug("Found operation: %s", operation)
            yield operation

    def _should_include_operation(self, operation: dict) -> bool:
        command = operation.get("command")
        if not command:
            self._check.log.debug("Skipping operation without command: %s", operation)
            return False
        if "hello" in command and operation.get("op") == "command":
            # MongoDB drivers and clients use hello to determine the state of
            # the replica set members and to discover additional members of a replica set.
            self._check.log.debug("Skipping hello operation: %s", operation)
            return False
        return True

    def _should_explain(self, op: Optional[str], command: dict) -> bool:
        dbname = command.get("$db")
        if not dbname or dbname == "admin":
            # Skip system operations
            self._check.log.debug("Skipping explain system operation: %s", command)
            return False

        if not op or op == "none":
            # Skip operations that are not queries
            self._check.log.debug("Skipping explain operation without operation type: %s", command)
            return False

        if op in ("getMore", "insert", "update", "getmore", "killcursors", "remove"):
            # Skip operations that are not queries
            self._check.log.debug("Skipping explain operation type %s: %s", op, command)
            return False

        return True

    def _get_explain_plan(self, op: Optional[str], command: dict) -> OperationSamplePlan:
        if not self._should_explain(op, command):
            return

        dbname = command.pop("$db")
        try:
            explain_plan = self._check.api_client[dbname].command("explain", command)
            if "command" in explain_plan:
                explain_plan.pop("command")  # Remove the original command from the explain plan
            query_planner = self._get_query_planner(explain_plan)
            return {
                "definition": explain_plan,
                "query_hash": query_planner.get("queryHash"),
                "plan_cache_key": query_planner.get("planCacheKey"),
                "signature": compute_exec_plan_signature(json_util.dumps(explain_plan)),
            }
        except Exception as e:
            self._check.log.error("Could not explain command %s: %s", command, e)
            return {
                "collection_errors": [
                    {
                        "code": str(type(e).__name__),  # str
                        "message": str(e),  # str
                    }
                ],
            }

    def _get_query_planner(self, explain_plan: dict) -> dict:
        if not explain_plan:
            return {}

        if "stage" in explain_plan:
            # The explain plan is nested under the $cursor key
            # usually when the command is a aggregation pipeline
            cursor = explain_plan.get("$cursor", {})
            return cursor.get("queryPlanner", {})
        else:
            return explain_plan.get("queryPlanner", {})

    def _get_command_collection(self, command: dict) -> Optional[str]:
        for key in ("collection", "find", "aggregate", "update", "insert", "delete", "findAndModify"):
            collection = command.get(key)
            if collection and isinstance(collection, str):  # edge case like {"aggregate": 1}
                return collection

    def _get_operation_client(self, operation: dict) -> OperationSampleClient:
        client_metadata = operation.get("clientMetadata", {})

        return {
            "hostname": operation.get("client") or operation.get("client_s"),
            "driver": client_metadata.get("driver"),
            "os": client_metadata.get("os"),
            "platform": client_metadata.get("platform"),
        }

    def _get_operation_user(self, operation: dict) -> Optional[str]:
        effective_users = operation.get("effectiveUsers")
        if not effective_users:
            return None
        return effective_users[0].get("user")

    def _get_command_truncation_state(self, command: dict) -> Optional[str]:
        if not command:
            return None
        return "truncated" if command.get("$truncated") else "not_truncated"

    def _get_operation_metadata(self, operation: dict) -> OperationSampleOperationMetadata:
        command = operation.get("command", {})
        return {
            "type": operation.get("type"),
            "op": operation.get("op"),
            "shard": operation.get("shard"),
            "dbname": command.get("$db"),
            "application": operation.get("appName"),
            "collection": self._get_command_collection(command),
            "comment": command.get("comment"),
            "truncated": self._get_command_truncation_state(command),
            "client": self._get_operation_client(operation),
            "user": self._get_operation_user(operation),
        }

    def _get_operation_stats(self, operation: dict) -> OperationSampleOperationStats:
        return {
            "active": operation.get("active", False),  # bool
            "desc": operation.get("desc"),  # str
            "opid": operation.get("opid"),  # str
            "ns": operation.get("ns"),  # str
            "plan_summary": operation.get("planSummary"),  # str
            "current_op_time": operation.get("currentOpTime"),  # str  start time of the operation
            "microsecs_running": operation.get("microsecs_running"),  # int
            "transaction_time_open_micros": operation.get("transaction", {}).get("timeOpenMicros"),  # int
            # Conflicts
            "prepare_read_conflicts": operation.get("prepareReadConflicts", 0),  # int
            "write_conflicts": operation.get("writeConflicts", 0),  # int
            "num_yields": operation.get("numYields", 0),  # int
            # Locks
            "waiting_for_lock": operation.get("waitingForLock", False),  # bool
            "locks": self._format_key_name(operation.get("locks", {})),  # dict
            "lock_stats": self._format_key_name(operation.get("lockStats", {})),  # dict
            # Flow control
            "waiting_for_flow_control": operation.get("waitingForFlowControl", False),  # bool
            "flow_control_stats": self._format_key_name(operation.get("flowControlStats", {})),  # dict
            # Latches
            "waiting_for_latch": operation.get("waitingForLatch", False),  # bool
        }

    def _get_query_signature(self, obfuscated_command: str) -> str:
        return compute_exec_plan_signature(obfuscated_command)

    def _create_operation_sample_payload(
        self,
        now: float,
        operation_metadata: OperationSampleOperationMetadata,
        obfuscated_command: str,
        query_signature: str,
        explain_plan: OperationSamplePlan,
        activity: OperationSampleActivityRecord,
    ) -> OperationSampleEvent:
        event = {
            "host": self._check._resolved_hostname,
            "dbm_type": "plan",
            "ddagentversion": datadog_agent.get_version(),
            "ddsource": "mongodb",
            "ddtags": ",".join(self._check._get_tags(include_deployment_tags=True)),
            "timestamp": now * 1000,
            "network": {
                "client": operation_metadata["client"],
            },
            "db": {
                "instance": operation_metadata["dbname"],
                "plan": explain_plan,
                "query_signature": query_signature,
                "resource_hash": query_signature,
                "application": operation_metadata["application"],
                "user": operation_metadata["user"],
                "statement": obfuscated_command,
                "metadata": {
                    "op": operation_metadata["op"],
                    "shard": operation_metadata["shard"],
                    "collection": operation_metadata["collection"],
                    "comment": operation_metadata["comment"],
                },
                "query_truncated": operation_metadata["truncated"],
            },
            "mongodb": {key: value for key, value in activity.items() if key not in SAMPLE_EXCLUDE_KEYS},
        }
        return event

    def _create_activity(
        self,
        now: float,
        operation: dict,
        operation_metadata: OperationSampleOperationMetadata,
        obfuscated_command: str,
        query_signature: str,
    ) -> Optional[OperationSampleActivityRecord]:
        activity = (
            {
                "now": now,
                "query_signature": query_signature,
                "statement": obfuscated_command,
            }
            | self._get_operation_stats(operation)
            | operation_metadata
        )

        return activity

    def _create_activities_payload(
        self, now: float, activities: List[OperationSampleActivityRecord]
    ) -> OperationActivityEvent:
        return {
            "host": self._check._resolved_hostname,
            "ddagentversion": datadog_agent.get_version(),
            "ddsource": "mongodb",
            "dbm_type": "activity",
            "collection_interval": self._collection_interval,
            "ddtags": self._check._get_tags(include_deployment_tags=True),
            "timestamp": now * 1000,
            "mongodb_activity": activities,
        }

    def _format_key_name(self, metric_dict: Dict) -> dict:
        # convert camelCase to snake_case
        formatted = {}
        for key, value in metric_dict.items():
            formatted_key = str(self._check.convert_to_underscore_separated(key))
            if formatted_key in metric_dict:
                # If the formatted_key already exists (conflict), use the original key
                formatted_key = key
            if isinstance(value, dict):
                formatted[formatted_key] = self._format_key_name(value)
            else:
                formatted[formatted_key] = value
        return formatted
