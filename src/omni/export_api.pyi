from typing import Any, Mapping, Sequence, TypedDict

class ExportIdentifier(TypedDict):
    cid: int
    section: str | None

class ExportField(TypedDict):
    type: str
    pii: bool

class ExportRelation(TypedDict):
    target: str
    to_many: bool
    pii: bool

class ExportEntity(TypedDict):
    cids: Sequence[ExportIdentifier]
    name: str
    table: str
    id: str
    fields: Mapping[str, ExportField]
    relations: Mapping[str, ExportRelation]

class ExportSchema(TypedDict):
    schema_version: str
    entities: Mapping[str, ExportEntity]
    excluded: Sequence[str]

class ExportCursor(TypedDict):
    after_mtime: float
    after_id: int

class ExportChanges(TypedDict):
    entities: Sequence[Mapping[str, Any]]
    cursor: ExportCursor
    until_mtime: float
    schema_version: str

class ExportRange(TypedDict):
    start_id: int
    end_id: int
    count: int
    mtime_sum: float
    digest: int

class ExportDigests(TypedDict):
    start_id: int
    end_id: int
    ranges: Sequence[ExportRange]
    size: int

class ExportPairs(TypedDict):
    start_id: int
    end_id: int
    pairs: Sequence[tuple[int, float]]

class ExportEntityCursor(TypedDict):
    after_id: int

class ExportEntities(TypedDict):
    entities: Sequence[Mapping[str, Any]]
    entity: str
    cursor: ExportEntityCursor
    schema_version: str

class ExportTotals(TypedDict):
    entity: str
    until_mtime: float
    count: int

class ExportAPI(object):
    def export_schema(self) -> ExportSchema: ...
    def export_changes(self, *args, **kwargs) -> ExportChanges: ...
    def export_digests(self, *args, **kwargs) -> ExportDigests | ExportPairs: ...
    def export_entities(self, entity: str, *args, **kwargs) -> ExportEntities: ...
    def export_totals(self, entity: str, *args, **kwargs) -> ExportTotals: ...
