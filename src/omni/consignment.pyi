from typing import Any, Literal, Mapping, NotRequired, Sequence

from .base import BaseDelta, BaseReference
from .price import Price
from .document import DocumentDelta
from .store import Store
from .employee import Employee
from .consignment_line import ConsignmentLine, ConsignmentLineDelta
from .supplier import Supplier
from .workflow_operation import WorkflowOperation, WorkflowOperationDelta

ConsignmentStateT = Literal[1, 2, 3]

class ConsignmentState:
    OPEN: Literal[1] = ...
    CLOSED: Literal[2] = ...
    EXPIRED: Literal[3] = ...

class Consignment(WorkflowOperation[ConsignmentStateT]):
    start_date: float
    end_date: float | None
    vat: float
    discount: float
    discount_vat: float | None
    communication_frequency: float | None
    price: Price
    primary_buyer: Employee
    supplier: NotRequired[Supplier | None]
    delivery_site: NotRequired[Store]
    consignment_lines: NotRequired[Sequence[ConsignmentLine]]

class ConsignmentDelta(WorkflowOperationDelta):
    start_date: float
    supplier: BaseReference
    delivery_site: BaseReference
    end_date: NotRequired[float | None]
    communication_frequency: NotRequired[float | None]
    discount: NotRequired[float]
    owner: NotRequired[BaseReference]
    primary_buyer: NotRequired[BaseReference]
    consignment_lines: Sequence[ConsignmentLineDelta]
    _parameters: NotRequired[Mapping[str, Any]]

class ConsignmentPayload(BaseDelta):
    consignment: ConsignmentDelta
    document: NotRequired[DocumentDelta]

class ConsignmentAPI(object):
    def list_consignments(self, *args, **kwargs) -> Sequence[Consignment]: ...
    def create_consignment(self, payload: ConsignmentPayload) -> Consignment: ...
    def get_consignment(self, object_id: int) -> Consignment: ...
