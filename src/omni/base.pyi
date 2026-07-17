from typing import Any, Literal, Mapping, NotRequired, Sequence, TypedDict

from appier import OAuth2API

from .consignment import ConsignmentAPI
from .customer import CustomerAPI
from .document import DocumentAPI
from .employee import EmployeeAPI
from .entity import EntityAPI
from .identifiable import IdentifiableAPI
from .inventory_check import InventoryCheckAPI
from .invoice import InvoiceAPI
from .media import MediaAPI
from .merchandise import MerchandiseAPI
from .money_sale_slip import MoneySaleSlipAPI
from .purchase import PurchaseAPI
from .receipt import ReceiptAPI
from .repair import RepairAPI
from .repair_operation import RepairOperationAPI
from .saft_pt import SaftPtAPI
from .sale import SaleAPI
from .sale_snapshot import SaleSnapshotAPI
from .signed_document import SignedDocumentAPI
from .status import StatusAPI
from .store import StoreAPI
from .system_company import SystemCompanyAPI
from .transfer import TransferAPI
from .user import UserAPI
from .web import WebAPI

BASE_URL: str = ...
CLIENT_ID: str = ...
CLIENT_SECRET: str = ...
REDIRECT_URL: str = ...
SCOPE: Sequence[str] = ...

StatusT = Literal[1, 2]
FlagT = Literal[1, 2]

class Status:
    ENABLED: Literal[1] = ...
    DISABLED: Literal[2] = ...

class Flag:
    YES: Literal[1] = ...
    NO: Literal[2] = ...

class Base(TypedDict):
    _class: str
    object_id: int
    unique_id: str
    instance_id: int | None
    status: StatusT
    create_date: float
    modify_date: float
    description: str | None
    description_long: str | None
    representation: str | None
    metadata: Mapping[str, Any] | None

class BaseDelta(TypedDict):
    _class: NotRequired[str]
    description: NotRequired[str | None]
    metadata: NotRequired[Mapping[str, Any] | None]

class BaseReference(TypedDict):
    object_id: int

class Result(TypedDict):
    result: str

class API(
    OAuth2API,
    WebAPI,
    SaleAPI,
    UserAPI,
    StoreAPI,
    MediaAPI,
    EntityAPI,
    StatusAPI,
    RepairAPI,
    SaftPtAPI,
    InvoiceAPI,
    ReceiptAPI,
    PurchaseAPI,
    CustomerAPI,
    TransferAPI,
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
    RepairOperationAPI,
):
    pass
