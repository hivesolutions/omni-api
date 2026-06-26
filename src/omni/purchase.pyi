from typing import Sequence

from .price import Price
from .employee import Employee
from .operation import Operation

class Purchase(Operation):
    financial_discount: float
    financial_discount_vat: float
    vat: float
    discount: float
    discount_vat: float
    price: Price
    primary_buyer: Employee

class PurchaseAPI(object):
    def list_purchases(self, *args, **kwargs) -> Sequence[Purchase]: ...
    def create_purchase(self, payload: Purchase) -> Purchase: ...
    def get_purchase(self, object_id: int) -> Purchase: ...
