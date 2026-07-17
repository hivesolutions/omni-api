from typing import Generic, TypeVar

from .operation import Operation, OperationDelta

_W = TypeVar("_W", bound=int, default=int)

class WorkflowOperation(Operation, Generic[_W]):
    workflow_state: _W

class WorkflowOperationDelta(OperationDelta):
    pass
