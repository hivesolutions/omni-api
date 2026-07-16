from typing import Literal, NotRequired, Sequence, TypedDict

from .base import Base, BaseDelta
from .price import Price
from .payment import Payment
from .customer import Customer
from .operation import Operation, VatItem
from .sale_line import SaleLine
from .identifiable import Identifiable, IdentifiableDelta
from .system_company import SystemCompany

class DocumentStatus:
    DRAFT: Literal[1] = ...
    PRINTED: Literal[2] = ...
    COMPLETED: Literal[3] = ...

class DocumentType:
    INTERNAL: Literal[1] = ...
    INBOUND: Literal[2] = ...
    OUTBOUND: Literal[3] = ...

class DocumentOperation(Operation):
    vat: float
    discount: float | None
    discount_vat: float | None
    price: Price
    price_vat: float
    vat_list: Sequence[VatItem]
    lines_discount_vat: float
    customer: NotRequired[Customer | None]
    sale_lines: NotRequired[Sequence[SaleLine]]
    lines: NotRequired[Sequence[SaleLine]]
    payments: NotRequired[Sequence[Payment]]

class DocumentPayload(TypedDict):
    system_company: NotRequired[SystemCompany]
    operation: NotRequired[DocumentOperation]

class Document(Base, Identifiable):
    issue_date: float
    document_status: Literal[1, 2, 3]
    document_type: Literal[1, 2, 3]
    title: str | None
    observations: str | None
    payload: DocumentPayload | None
    operation_code: str | None
    issue_operation: NotRequired[Operation]
    redeem_operation: NotRequired[Operation | None]

class DocumentDelta(BaseDelta, IdentifiableDelta):
    _class: NotRequired[str]
    issue_date: NotRequired[float]
    title: NotRequired[str | None]
    observations: NotRequired[str | None]

class DocumentAPI(object):
    def list_documents(self, *args, **kwargs) -> Sequence[Document]: ...
    @classmethod
    def default_customers(cls, documents: Sequence[Document]) -> None: ...
    @classmethod
    def default_customer(cls, document: Document) -> None: ...
