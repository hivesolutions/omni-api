from typing import Any, Literal, Mapping, NotRequired, Sequence, TypedDict

from .base import BaseDelta, BaseReference
from .price import Price
from .invoice import Invoice
from .payment import PaymentDelta
from .receipt import Receipt
from .customer import Customer, CustomerPersonDelta
from .operation import Operation, OperationDelta, VatItem
from .sale_line import SaleLine, SaleLineDelta
from .sale_snapshot import SaleStats
from .money_sale_slip import MoneySaleSlip

class StockDeductionType:
    NO_DEDUCTION: Literal[1] = ...
    STOCK_ON_HAND: Literal[2] = ...
    RESERVED_STOCK: Literal[3] = ...

class VatExemption:
    NO_EXEMPTION: Literal[1] = ...
    NORMAL_EXEMPTION: Literal[2] = ...
    UNKNOWN: Literal[3] = ...

class ReturnState:
    RETURNABLE: Literal[1] = ...
    NON_RETURNABLE: Literal[2] = ...

class SaleCustomerType:
    NEW: Literal["new"] = ...
    EXISTING: Literal["existing"] = ...
    ANONYMOUS: Literal["anonymous"] = ...

class Sale(Operation):
    stock_deduction_type: Literal[1, 2, 3]
    financial_discount: float | None
    financial_discount_vat: float | None
    exemption: float
    bail: float
    vat: float
    discount: float
    discount_vat: float
    global_discount_vat: float
    voucher_discount_vat: float
    vat_exemption: Literal[1, 2, 3]
    vat_exemption_code: str | None
    payment_state: Literal[1, 2, 3, 4, 5]
    return_state: Literal[1, 2]
    price: Price
    price_vat: float
    no_discount_price_vat: float
    customer: Customer | None
    sale_lines: NotRequired[Sequence[SaleLine]]

class SaleVat(TypedDict):
    vat_list: Sequence[VatItem] | None

class SaleCustomerParameters(TypedDict):
    type: Literal["new", "existing", "anonymous"]

class SaleCustomer(CustomerPersonDelta):
    _parameters: SaleCustomerParameters
    object_id: NotRequired[int]

class SaleDelta(OperationDelta):
    stock_deduction_type: NotRequired[Literal[1, 2, 3]]
    owner: NotRequired[BaseReference]
    primary_seller: NotRequired[BaseReference]
    sale_lines: Sequence[SaleLineDelta]
    primary_payment: PaymentDelta
    _parameters: NotRequired[Mapping[str, Any]]

class SalePayload(BaseDelta):
    transaction: SaleDelta
    customer: SaleCustomer
    lines: NotRequired[Sequence[SaleLineDelta]]

class SaleAPI(object):
    def list_sales(self, *args, **kwargs) -> Sequence[Sale]: ...
    def create_sale(self, payload: SalePayload) -> Sale: ...
    def get_sale(self, object_id: int) -> Sale: ...
    def vat_sale(self, object_id: int) -> SaleVat: ...
    def issue_money_sale_slip_sale(
        self, object_id: int, metadata: Mapping[str, Any] = ...
    ) -> MoneySaleSlip: ...
    def issue_invoice_sale(
        self, object_id: int, metadata: Mapping[str, Any] | None = ...
    ) -> Invoice: ...
    def issue_receipt_sale(
        self, object_id: int, metadata: Mapping[str, Any] | None = ...
    ) -> Receipt: ...
    def ensure_receipt_sale(
        self, object_id: int, metadata: Mapping[str, Any] | None = ...
    ) -> Receipt: ...
    def self_sales(self, *args, **kwargs) -> Sequence[Sale]: ...
    def stats_sales(
        self,
        date: float | None = ...,
        unit: str = ...,
        span: int = ...,
        store_id: int | str | None = ...,
        has_global: bool | None = ...,
        output: str = ...,
    ) -> Mapping[str, SaleStats]: ...
