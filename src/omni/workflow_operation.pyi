from .operation import Operation, OperationDelta

class WorkflowOperation(Operation):
    workflow_state: int

class WorkflowOperationDelta(OperationDelta):
    pass
