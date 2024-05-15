# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from typing import Any, Dict, List, Optional, Tuple, TypedDict


class OperationSampleClientDriver(TypedDict, total=False):
    name: Optional[str]
    version: Optional[str]


class OperationSampleClientOs(TypedDict, total=False):
    type: Optional[str]
    name: Optional[str]
    architecture: Optional[str]
    version: Optional[str]


class OperationSampleClientMongos(TypedDict, total=False):
    host: Optional[str]
    client: Optional[str]
    version: Optional[str]


class OperationSampleClient(TypedDict, total=False):
    hostname: Optional[str]
    driver: Optional[OperationSampleClientDriver]
    os: Optional[OperationSampleClientOs]
    platform: Optional[str]


class OperationSampleEventNetwork(TypedDict, total=False):
    client: OperationSampleClient


class OperationSampleEventDatabaseMetadata(TypedDict, total=False):
    op: Optional[str]
    shard: Optional[str]  # only available when sampling mongos
    collection: Optional[str]
    comment: Optional[str]


class OperationSamplePlanCollectionError(TypedDict, total=False):
    code: str
    message: str


class OperationSamplePlan(TypedDict, total=False):
    definition: dict
    query_hash: Optional[str]
    plan_cache_key: Optional[str]
    signature: str
    collection_errors: Optional[List[OperationSamplePlanCollectionError]]


class OperationSampleEventDatabase(TypedDict, total=False):
    instance: Optional[str]
    plan: Optional[OperationSamplePlan]
    query_signature: Optional[str]  # idle session does not have this
    resource_hash: Optional[str]
    application: Optional[str]
    user: Optional[str]
    statement: Optional[str]
    metadata: OperationSampleEventDatabaseMetadata
    query_truncated: Optional[str]


class OperationSampleOperationStatsLocks(TypedDict, total=False):
    parallel_batch_writer_mode: Optional[str]
    replication_state_transition: Optional[str]
    global_: Optional[str]
    database: Optional[str]
    collection: Optional[str]
    mutex: Optional[str]
    metadata: Optional[str]
    oplog: Optional[str]


class OperationSampleOperationStatsLockMode(TypedDict, total=False):
    r: Optional[int]
    w: Optional[int]
    R: Optional[int]
    W: Optional[int]


class OperationSampleOperationStatsLockStatsBase(TypedDict, total=False):
    acquire_count: Optional[OperationSampleOperationStatsLockMode]
    acquire_wait_count: Optional[OperationSampleOperationStatsLockMode]
    time_acquiring_micros: Optional[OperationSampleOperationStatsLockMode]
    deadlock_count: Optional[OperationSampleOperationStatsLockMode]


class OperationSampleOperationStatsLockStats(TypedDict, total=False):
    parallel_batch_writer_mode: Optional[OperationSampleOperationStatsLockStatsBase]
    eplication_state_transition: Optional[OperationSampleOperationStatsLockStatsBase]
    global_: Optional[OperationSampleOperationStatsLockStatsBase]
    database: Optional[OperationSampleOperationStatsLockStatsBase]
    collection: Optional[OperationSampleOperationStatsLockStatsBase]
    mutex: Optional[OperationSampleOperationStatsLockStatsBase]
    metadata: Optional[OperationSampleOperationStatsLockStatsBase]
    oplog: Optional[OperationSampleOperationStatsLockStatsBase]


class OperationSampleOperationStatsFlowControlStats(TypedDict, total=False):
    accquire_count: Optional[int]
    accquire_wait_count: Optional[int]
    time_accquiring_micros: Optional[int]


class OperationSampleOperationStatsWaitingForLatch(TypedDict, total=False):
    timestamp: str
    captureName: str
    backtrace: List[str]


class OperationSampleOperationStats(TypedDict, total=False):
    active: bool
    desc: Optional[str]
    opid: str
    ns: Optional[str]
    plan_summary: Optional[str]
    current_op_time: str
    microsecs_running: Optional[int]
    prepare_read_conflicts: Optional[int]
    write_conflicts: Optional[int]
    num_yields: Optional[int]
    waiting_for_lock: bool
    locks: Optional[OperationSampleOperationStatsLocks]
    lock_stats: Optional[OperationSampleOperationStatsLockStats]
    waiting_for_flow_control: bool
    flow_control_stats: Optional[OperationSampleOperationStatsFlowControlStats]
    waiting_for_latch: Optional[OperationSampleOperationStatsWaitingForLatch]


class OperationSampleActivityBase(TypedDict, total=False):
    now: int
    query_signature: Optional[str]
    statement: Optional[str]


class OperationSampleOperationMetadata(TypedDict, total=False):
    type: str
    op: Optional[str]
    shard: Optional[str]
    dbname: Optional[str]
    application: Optional[str]
    collection: Optional[str]
    comment: Optional[str]
    truncated: Optional[str]
    client: OperationSampleClient
    user: Optional[str]


class OperationSampleActivityRecord(
    OperationSampleActivityBase, OperationSampleOperationMetadata, OperationSampleOperationStats, total=False
):
    pass


class OperationSampleConnectionRecord(TypedDict, total=False):
    application: Optional[str]
    dbname: Optional[str]
    type: str
    user: Optional[str]
    count: int


class OperationSampleEvent(TypedDict, total=False):
    host: str
    dbm_type: str
    ddagentversion: str
    ddsource: str
    ddtags: str
    timestamp: int
    network: OperationSampleEventNetwork
    db: OperationSampleEventDatabase
    mongodb: OperationSampleActivityRecord


class OperationActivityEvent(TypedDict, total=False):
    host: str
    dbm_type: str
    ddagentversion: str
    ddsource: str
    ddtags: str
    timestamp: int
    mongodb_activity: List[OperationSampleActivityRecord]
    mongodb_connections: List[OperationSampleConnectionRecord]
