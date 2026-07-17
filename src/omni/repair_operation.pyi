from typing import Literal, NotRequired, Sequence

from .base import BaseDelta, BaseReference, Result
from .sale import Sale
from .price import Price
from .store import Store
from .customer import Customer
from .employee import Employee
from .merchandise import TransactionalMerchandise
from .repair_slip import RepairSlip
from .workflow_message import WorkflowMessage, WorkflowMessagePayload
from .workflow_operation import (
    WorkflowEvent,
    WorkflowOperation,
    WorkflowOperationDelta,
)

RepairOperationStateT = Literal[1, 2, 3, 4, 5, 6, 7, 8]
RepairTypeT = Literal[1, 2]
RepairPriorityT = Literal[1, 2, 3]

class RepairOperationState:
    UNSET: Literal[1] = ...
    OPENED: Literal[2] = ...
    APPROVED: Literal[3] = ...
    REJECTED: Literal[4] = ...
    QUOTATION: Literal[5] = ...
    RECEIVED: Literal[6] = ...
    SENT: Literal[7] = ...
    CLOSED: Literal[8] = ...

class RepairType:
    WARRANTY: Literal[1] = ...
    QUOTATION: Literal[2] = ...

class RepairPriority:
    LOW: Literal[1] = ...
    MEDIUM: Literal[2] = ...
    HIGH: Literal[3] = ...

class RepairOperation(WorkflowOperation[RepairOperationStateT]):
    title: str
    repair_type: RepairTypeT
    item_reference: str | None
    sale_identifier: str | None
    item_damage: str | None
    problem_description: str | None
    repair_description: str | None
    estimated_date: float | None
    priority: RepairPriorityT | None
    supplier_reference: str | None
    owner: Store
    employee: NotRequired[Employee | None]
    customer: NotRequired[Customer | None]
    merchandise: NotRequired[TransactionalMerchandise | None]
    repair_slip: NotRequired[RepairSlip | None]
    sale_transaction: NotRequired[Sale | None]
    price: NotRequired[Price | None]

class RepairOperationDelta(WorkflowOperationDelta):
    title: str
    repair_type: RepairTypeT
    item_reference: NotRequired[str | None]
    sale_identifier: NotRequired[str | None]
    item_damage: NotRequired[str | None]
    problem_description: NotRequired[str | None]
    repair_description: NotRequired[str | None]
    estimated_date: NotRequired[float]
    priority: NotRequired[RepairPriorityT]
    supplier_reference: NotRequired[str | None]
    owner: NotRequired[BaseReference]
    employee: NotRequired[BaseReference]
    customer: NotRequired[BaseReference]
    supplier: NotRequired[BaseReference]
    merchandise: NotRequired[BaseReference]
    sale_transaction: NotRequired[BaseReference]

class RepairOperationPayload(BaseDelta):
    repair_operation: RepairOperationDelta

class RepairOperationAPI(object):
    def list_repair_operations(self, *args, **kwargs) -> Sequence[RepairOperation]: ...
    def create_repair_operation(
        self, payload: RepairOperationPayload
    ) -> RepairOperation: ...
    def get_repair_operation(self, object_id: int) -> RepairOperation: ...
    def update_repair_operation(
        self, object_id: int, payload: RepairOperationPayload
    ) -> RepairOperation: ...
    def approve_repair_operation(self, object_id: int) -> RepairOperation: ...
    def reject_repair_operation(self, object_id: int) -> RepairOperation: ...
    def quote_repair_operation(self, object_id: int) -> RepairOperation: ...
    def receive_repair_operation(self, object_id: int) -> RepairOperation: ...
    def send_repair_operation(self, object_id: int) -> RepairOperation: ...
    def close_repair_operation(self, object_id: int) -> RepairOperation: ...
    def issue_repair_slip_repair_operation(self, object_id: int) -> RepairSlip: ...
    def list_messages_repair_operation(
        self, object_id: int
    ) -> Sequence[WorkflowEvent]: ...
    def create_message_repair_operation(
        self, object_id: int, payload: WorkflowMessagePayload
    ) -> WorkflowMessage: ...
    def update_message_repair_operation(
        self, object_id: int, message_id: int, payload: WorkflowMessagePayload
    ) -> WorkflowMessage: ...
    def delete_message_repair_operation(
        self, object_id: int, message_id: int
    ) -> Result: ...
