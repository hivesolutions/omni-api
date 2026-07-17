from typing import Any, Literal, Mapping, NotRequired, Sequence

from .base import BaseDelta, BaseReference
from .price import Price
from .store import Store
from .employee import Employee
from .transfer_line import TransferLine, TransferLineDelta
from .signed_document import SignedDocument
from .workflow_operation import WorkflowOperation, WorkflowOperationDelta

TransferStateT = Literal[1, 2, 3, 4, 5, 6, 7]

class TransferState:
    UNSET: Literal[1] = ...
    CREATED: Literal[2] = ...
    RESERVED: Literal[3] = ...
    SENT: Literal[4] = ...
    RECEIVED: Literal[5] = ...
    CLOSED: Literal[6] = ...
    CANCELED: Literal[7] = ...

class Transfer(WorkflowOperation):
    vat: float
    price: NotRequired[Price]
    price_vat: NotRequired[float]
    origin: NotRequired[Store]
    destination: Store
    sender: NotRequired[Employee | None]
    receiver: NotRequired[Employee | None]
    transfer_lines: NotRequired[Sequence[TransferLine]]
    transportation_slip: NotRequired[SignedDocument | None]

class TransferDelta(WorkflowOperationDelta):
    origin: BaseReference
    destination: BaseReference
    transfer_lines: Sequence[TransferLineDelta]
    sender: NotRequired[BaseReference]
    receiver: NotRequired[BaseReference]
    _parameters: NotRequired[Mapping[str, Any]]

class TransferPayload(BaseDelta):
    transfer: TransferDelta

class TransferAPI(object):
    def list_transfers(self, *args, **kwargs) -> Sequence[Transfer]: ...
    def create_transfer(self, payload: TransferPayload) -> Transfer: ...
    def get_transfer(self, object_id: int) -> Transfer: ...
