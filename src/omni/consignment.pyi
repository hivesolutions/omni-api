from typing import Literal, Sequence

from .price import Price
from .employee import Employee
from .workflow_operation import WorkflowOperation

ConsignmentStateT = Literal[1, 2, 3]

class ConsignmentState:
    OPEN: Literal[1] = ...
    CLOSED: Literal[2] = ...
    EXPIRED: Literal[3] = ...

class Consignment(WorkflowOperation):
    start_date: float
    end_date: float | None
    vat: float
    discount: float
    discount_vat: float | None
    communication_frequency: float | None
    price: Price
    primary_buyer: Employee

class ConsignmentAPI(object):
    def list_consignments(self, *args, **kwargs) -> Sequence[Consignment]: ...
    def create_consignment(self, payload: Consignment) -> Consignment: ...
    def get_consignment(self, object_id: int) -> Consignment: ...
