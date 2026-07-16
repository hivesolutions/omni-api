from typing import Any, Literal, Mapping, NotRequired, Sequence, TypedDict

from appier import OAuth2API

from .consignment import ConsignmentAPI
from .customer import CustomerAPI
from .document import DocumentAPI
from .employee import EmployeeAPI
from .identifiable import IdentifiableAPI
from .inventory_check import InventoryCheckAPI
from .invoice import InvoiceAPI
from .merchandise import MerchandiseAPI
from .money_sale_slip import MoneySaleSlipAPI
from .purchase import PurchaseAPI
from .receipt import ReceiptAPI
from .saft_pt import SaftPtAPI
from .sale import SaleAPI
from .sale_snapshot import SaleSnapshotAPI
from .signed_document import SignedDocumentAPI
from .store import StoreAPI
from .system_company import SystemCompanyAPI
from .user import UserAPI

BASE_URL: str = ...
CLIENT_ID: str = ...
CLIENT_SECRET: str = ...
REDIRECT_URL: str = ...
SCOPE: Sequence[str] = ...

Status = Literal[1, 2]
Flag = Literal[1, 2]

class Base(TypedDict):
    _class: str
    object_id: int
    unique_id: str
    instance_id: int | None
    status: Status
    create_date: float
    modify_date: float
    description: str | None
    description_long: str | None
    representation: str | None
    metadata: Mapping[str, Any] | None

class BaseDelta(TypedDict):
    description: NotRequired[str | None]
    metadata: NotRequired[Mapping[str, Any] | None]

class BaseReference(TypedDict):
    object_id: int

class API(
    OAuth2API,
    SaleAPI,
    UserAPI,
    StoreAPI,
    SaftPtAPI,
    InvoiceAPI,
    ReceiptAPI,
    PurchaseAPI,
    CustomerAPI,
    DocumentAPI,
    EmployeeAPI,
    MerchandiseAPI,
    ConsignmentAPI,
    IdentifiableAPI,
    SaleSnapshotAPI,
    SystemCompanyAPI,
    MoneySaleSlipAPI,
    InventoryCheckAPI,
    SignedDocumentAPI,
):
    pass
