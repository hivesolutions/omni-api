from typing import Generic, Literal, Sequence, TypedDict, TypeVar

from .operation import Operation, OperationDelta
from .workflow_message import WorkflowMessageFile

_W = TypeVar("_W", bound=int, default=int)

class WorkflowOperation(Operation, Generic[_W]):
    workflow_state: _W

class WorkflowOperationDelta(OperationDelta):
    pass

WorkflowEventKindT = Literal["state_change", "message"]

class WorkflowEventBase(TypedDict):
    object_id: int
    date: str
    actual_date: float
    user: str | None
    user_object_id: int | None
    user_mtime: float | None

class WorkflowStateChangeEvent(WorkflowEventBase):
    kind: Literal["state_change"]
    state_color: str
    state_string: str
    previous_state_color: str | None
    previous_state_string: str | None
    observations: str | None

class WorkflowMessageEvent(WorkflowEventBase):
    kind: Literal["message"]
    body: str
    body_html: str
    files: Sequence[WorkflowMessageFile]
    edited_date: float | None

WorkflowEvent = WorkflowStateChangeEvent | WorkflowMessageEvent
