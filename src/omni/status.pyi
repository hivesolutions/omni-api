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

class StatusDatabase(TypedDict):
    engine: str
    internal_version: str | None
    database_size: int
    database_size_string: str

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
    kafka: NotRequired[StatusKafka]
    pushi: NotRequired[StatusPushi]
    network: NotRequired[Mapping[str, Any]]
    libraries: Sequence[StatusLibrary]

class StatusAPI(object):
    def get_status(self) -> SystemStatus: ...
