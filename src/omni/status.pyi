from typing import Any, Mapping, NotRequired, Sequence, TypedDict

class StatusInfo(TypedDict):
    version: str
    date: str
    commit: str | None
    commit_short: str | None
    build_date: int | None

class StatusSystem(TypedDict):
    layout_mode: str
    run_mode: str
    start_timestamp: float
    version: str
    release: str
    build: str
    release_date_time: str
    environment: str

class StatusMigration(TypedDict):
    object_id: int
    uuid: str
    timestamp: int
    description: str | None
    result: str
    operation: str | None
    operator: str | None
    duration: int
    start_s: str
    end_s: str

class StatusDatabase(TypedDict):
    engine: str
    internal_version: str | None
    server_version: NotRequired[str | None]
    database_size: int
    database_size_string: str
    host: NotRequired[str | None]
    port: NotRequired[int | None]
    latency: NotRequired[float]
    latency_string: NotRequired[str]
    last_migration: NotRequired[StatusMigration | None]

class StatusRuntime(TypedDict):
    uptime: float
    uptime_string: str
    pid: int
    memory: int | None
    memory_string: str | None
    threads: int
    cpu_count: int | None
    load: Sequence[float] | None
    load_string: str | None
    load_high: bool
    disk_free: int | None
    disk_total: int | None
    disk_free_string: str | None
    disk_total_string: str | None
    disk_low: bool
    server_time: float

class StatusKafka(TypedDict):
    server: str
    security_protocol: str
    sasl_mechanism: str
    default_topic: str
    client_version: str | None

class StatusPushi(TypedDict):
    app_id: str | None
    app_key: str | None
    app_secret: str | None
    base_url: str | None
    ws_url: str | None
    version: str | None

class StatusLibrary(TypedDict):
    name: str
    version: str | None

class SystemStatus(TypedDict):
    info: StatusInfo
    system: StatusSystem
    database: StatusDatabase
    server_software: str | None
    hostname: str
    runtime: NotRequired[StatusRuntime]
    kafka: NotRequired[StatusKafka]
    pushi: NotRequired[StatusPushi]
    network: NotRequired[Mapping[str, Any]]
    libraries: Sequence[StatusLibrary]

class StatusAPI(object):
    def get_status(self) -> SystemStatus: ...
