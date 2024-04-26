from typing import NotRequired, Sequence

from .base import Base, BaseDelta
from .task import Task

class SaftPtReport(Base):
    _version: str
    fiscal_year: int
    start_date: float
    end_date: float
    task: NotRequired[Task]

class SaftPtReportDelta(BaseDelta):
    _version: str
    fiscal_year: int
    start_date: float
    end_date: float

class SaftPtReportPayload(BaseDelta):
    saft_pt_report: SaftPtReportDelta

class SaftPtAPI(object):
    def list_saft_pt(self, *args, **kwargs) -> Sequence[SaftPtReport]: ...
    def create_saft_pt(self, payload: SaftPtReportPayload) -> SaftPtReport: ...
    def get_saft_pt(self, object_id: int) -> SaftPtReport: ...
    def file_saft_pt(self, object_id: int) -> bytes: ...
    def file_decompressed_saft_pt(self, object_id: int) -> bytes: ...
