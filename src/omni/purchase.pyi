from typing import Any, Mapping, NotRequired, Sequence

from .base import BaseDelta, BaseReference
from .price import Price
from .document import DocumentDelta
from .employee import Employee
from .operation import Operation, OperationDelta
from .supplier import Supplier
from .purchase_line import PurchaseLine, PurchaseLineDelta

class Purchase(Operation):
    financial_discount: float | None
    financial_discount_vat: float | None
    vat: float
    discount: float
    discount_vat: float | None
    price: Price
    supplier: NotRequired[Supplier | None]
    primary_buyer: NotRequired[Employee]
    purchase_lines: NotRequired[Sequence[PurchaseLine]]

class PurchaseDelta(OperationDelta):
    owner: NotRequired[BaseReference]
    supplier: NotRequired[BaseReference]
    purchase_lines: Sequence[PurchaseLineDelta]
    _parameters: NotRequired[Mapping[str, Any]]

class PurchasePayload(BaseDelta):
    purchase_transaction: PurchaseDelta
    document: NotRequired[DocumentDelta]

class PurchaseAPI(object):
    def list_purchases(self, *args, **kwargs) -> Sequence[Purchase]: ...
    def create_purchase(self, payload: PurchasePayload) -> Purchase: ...
    def get_purchase(self, object_id: int) -> Purchase: ...
