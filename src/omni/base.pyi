from typing import Any, Literal, Mapping, NoReturn, NotRequired, Sequence, TypedDict

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
from .supplier import SupplierAPI
from .system_company import SystemCompany, SystemCompanyAPI
from .transfer import TransferAPI
from .user import BaseUser, UserAPI
from .web import WebAPI

BASE_URL: str = ...
CLIENT_ID: str = ...
CLIENT_SECRET: str = ...
REDIRECT_URL: str = ...
SCOPE: Sequence[OAuthScopeT] = ...

OAuthScopeT = Literal[
    "analytics.employee_snapshot.list",
    "analytics.sale_snapshot.list",
    "base",
    "base.user",
    "base.admin",
    "customers.customer.list",
    "customers.customer_person.list",
    "customers.customer_person.create",
    "customers.customer_person.show",
    "customers.customer_person.update",
    "customers.customer_company.list",
    "customers.customer_company.create",
    "customers.customer_company.show",
    "customers.customer_company.update",
    "documents.signed_document.list",
    "documents.signed_document.submit_invoice_at",
    "documents.signed_document.unsubmit_invoice_at",
    "documents.signed_document.submit_transport_at",
    "extras.saft_pt_report.show",
    "foundation.apn.subscribe",
    "foundation.approval_policy.list",
    "foundation.approval_policy.create",
    "foundation.approval_policy.show",
    "foundation.approval_policy.update",
    "foundation.approval_request.list",
    "foundation.approval_request.list.self",
    "foundation.approval_request.show",
    "foundation.approval_request.show.self",
    "foundation.approval_request.approve",
    "foundation.approval_request.reject",
    "foundation.approval_request.withdraw",
    "foundation.authentication_event.list",
    "foundation.authentication_event.list.self",
    "foundation.authentication_event.show",
    "foundation.authentication_event.show.self",
    "foundation.employee.list",
    "foundation.employee.create",
    "foundation.employee.show",
    "foundation.employee.show.self",
    "foundation.employee.update",
    "foundation.employee.delete",
    "foundation.log_entry.list",
    "foundation.log_entry.show",
    "foundation.media.list",
    "foundation.media.show",
    "foundation.media.update",
    "foundation.media.delete",
    "foundation.root_entity.list",
    "foundation.root_entity.show",
    "foundation.root_entity.update",
    "foundation.root_entity.show_media",
    "foundation.root_entity.set_media",
    "foundation.root_entity.clear_media",
    "foundation.status.show",
    "foundation.store.list",
    "foundation.store.create",
    "foundation.store.show",
    "foundation.store.update",
    "foundation.store.delete",
    "foundation.supplier_company.list",
    "foundation.supplier_company.show",
    "foundation.system_company.list",
    "foundation.system_company.create",
    "foundation.system_company.show",
    "foundation.system_company.show.self",
    "foundation.system_company.update",
    "foundation.system_company.update.self",
    "foundation.system_company.delete",
    "foundation.system_user.list",
    "foundation.system_user.create",
    "foundation.system_user.show",
    "foundation.system_user.show.self",
    "foundation.system_user.update",
    "foundation.system_user.delete",
    "foundation.web.subscribe",
    "foundation.web_push.subscribe",
    "inventory.inventory_check.list",
    "inventory.inventory_check.show",
    "inventory.inventory_line.list",
    "inventory.inventory_line.show",
    "inventory.inventory_line.update",
    "inventory.product.list",
    "inventory.product.create",
    "inventory.product.show",
    "inventory.product.update",
    "inventory.repair.list",
    "inventory.repair.create",
    "inventory.repair.show",
    "inventory.repair.update",
    "inventory.service.list",
    "inventory.service.create",
    "inventory.service.show",
    "inventory.service.update",
    "inventory.price_adjustment.list",
    "inventory.price_adjustment.create",
    "inventory.price_adjustment.request",
    "inventory.price_adjustment.approve",
    "inventory.price_adjustment.show",
    "inventory.stock_adjustment.list",
    "inventory.stock_adjustment.create",
    "inventory.stock_adjustment.request",
    "inventory.stock_adjustment.approve",
    "inventory.stock_adjustment.show",
    "inventory.sub_product.list",
    "inventory.sub_product.create",
    "inventory.sub_product.show",
    "inventory.sub_product.update",
    "inventory.transfer.list",
    "inventory.transfer.create",
    "inventory.transfer.request",
    "inventory.transfer.approve",
    "inventory.transfer.show",
    "inventory.transactional_merchandise.list",
    "inventory.transactional_merchandise.create",
    "inventory.transactional_merchandise.show",
    "inventory.transactional_merchandise.update",
    "purchases.consignment.list",
    "purchases.consignment.create",
    "purchases.consignment.show",
    "purchases.purchase_transaction.list",
    "purchases.purchase_transaction.create",
    "purchases.purchase_transaction.show",
    "sales.credit_note.list",
    "sales.credit_note.show",
    "sales.customer_return.list",
    "sales.customer_return.list.self",
    "sales.customer_return.show",
    "sales.invoice.list",
    "sales.invoice.show",
    "sales.money_sale_slip.list",
    "sales.money_sale_slip.show",
    "sales.receipt.list",
    "sales.receipt.show",
    "sales.repair_operation.list",
    "sales.repair_operation.create",
    "sales.repair_operation.show",
    "sales.repair_operation.update",
    "sales.repair_reference.list",
    "sales.repair_reference.create",
    "sales.repair_reference.show",
    "sales.sale_line.show",
    "sales.sale_order.list",
    "sales.sale_transaction.list",
    "sales.sale_transaction.list.self",
    "sales.sale_transaction.show",
]

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
    SupplierAPI,
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
    base_url: str
    open_url: str
    prefix: str
    client_id: str | None
    client_secret: str | None
    redirect_url: str
    scope: Sequence[OAuthScopeT]
    access_token: str | None
    session_id: str | None
    username: str | None
    password: str | None
    object_id: int | None
    acl: Mapping[str, int] | None
    tokens: Sequence[str] | None
    company: SystemCompany | None
    wrap_exception: bool
    mode: int

    def __init__(
        self,
        *args,
        base_url: str = ...,
        open_url: str = ...,
        prefix: str = ...,
        client_id: str | None = ...,
        client_secret: str | None = ...,
        redirect_url: str = ...,
        scope: Sequence[OAuthScopeT] = ...,
        access_token: str | None = ...,
        session_id: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        object_id: int | None = ...,
        acl: Mapping[str, int] | None = ...,
        tokens: Sequence[str] | None = ...,
        company: SystemCompany | None = ...,
        wrap_exception: bool = ...,
        mode: int = ...,
        **kwargs,
    ) -> None: ...
    def login(self, username: str | None = ..., password: str | None = ...) -> str: ...
    def get_session_id(self) -> str | None: ...
    def handle_error(self, error: Exception) -> NoReturn: ...
    def oauth_authorize(self, state: str | None = ...) -> str: ...
    def oauth_access(self, code: str) -> str: ...
    def oauth_session(self) -> str: ...
    def ping(self) -> BaseUser: ...
