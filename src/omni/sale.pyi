from typing import Sequence

from .price import Price
from .customer import Customer
from .operation import Operation
from .sale_line import SaleLine

class Sale(Operation):
    stock_deduction_type: int
    financial_discount: float
    financial_discount_vat: float
    exemption: float
    bail: float
    vat: float
    discount: float
    discount_vat: float
    vat_exemption: int
    vat_exemption_code: str
    price: Price
    price_vat: float
    no_discount_price_vat: float
    customer: Customer | None
    sale_lines: Sequence[SaleLine]

class SaleAPI(object):
    def list_sales(self, *args, **kwargs) -> Sequence[Sale]: ...
    def create_sale(self, payload: Sale) -> Sale: ...
    def get_sale(self, object_id: int) -> Sale: ...
