from typing import Any, Mapping, NotRequired, Sequence

from .base import Base, BaseDelta, FlagT, Result
from .task import Task
from .identifiable import Identifiable

class Script(Base):
    identifier: str
    code: str
    is_transaction: FlagT

class ScriptDelta(BaseDelta):
    identifier: NotRequired[str]
    code: NotRequired[str]
    is_transaction: NotRequired[FlagT]

class ScriptPayload(BaseDelta):
    script: ScriptDelta

class ScriptTask(Task, Identifiable):
    name: str
    scheduled_date: float | None
    start_date: float | None
    end_date: float | None
    estimated_end_date: float | None
    progress: float
    exec_context: Mapping[str, Any] | None
    exception_message: str | None
    exception_traceback: str | None
    log_data: Mapping[str, Any] | None
    script_id: int | None

class ScriptAPI(object):
    def list_scripts(self, *args, **kwargs) -> Sequence[Script]: ...
    def create_script(self, payload: ScriptPayload) -> Script: ...
    def get_script(self, object_id: int) -> Script: ...
    def update_script(self, object_id: int, payload: ScriptPayload) -> Script: ...
    def delete_script(self, object_id: int) -> Result: ...
    def execute_script(self, object_id: int) -> ScriptTask: ...
