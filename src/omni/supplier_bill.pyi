from typing import Literal, Mapping, NotRequired, Sequence, TypedDict

from .base import BaseDelta, BaseReference, Result
from .user import BaseUser
from .store import FunctionalUnit
from .payment import Payment
from .purchase import Purchase
from .supplier import Supplier
from .operation import Operation
from .approval_request import ApprovalRequest
from .workflow_message import WorkflowMessage
from .workflow_operation import WorkflowEvent, WorkflowOperation, WorkflowOperationDelta

SupplierBillStateT = Literal[1, 2, 3]
SupplierBillPaymentTypeT = Literal[1, 2, 3, 4, 5]
SupplierBillSettlementStateT = Literal[
    "unconfirmed", "unpaid", "partially_paid", "paid"
]
SupplierBillAgingBucketT = Literal["current", "1-30", "31-60", "61-90", "90+"]

class SupplierBillState:
    PENDING: Literal[1] = ...
    APPROVED: Literal[2] = ...
    CANCELED: Literal[3] = ...

class SupplierBillPaymentType:
    PAYMENT: Literal[1] = ...
    HISTORICAL: Literal[2] = ...
    CREDIT: Literal[3] = ...
    REFUND: Literal[4] = ...
    TRANSFER: Literal[5] = ...

class SupplierBill(WorkflowOperation[SupplierBillStateT]):
    bill_date: float
    due_date: float
    reference: str | None
    payment_terms_days: int
    currency: str
    reference_currency: str | None
    exchange_rate: float | None
    amount_vat: float
    paid_amount: float
    adjusted_amount: float
    outstanding_amount: float
    credit_amount: float
    balance_confirmed: Literal[0, 1]
    observations: str | None
    purchase: Purchase
    supplier: Supplier
    billing_site: FunctionalUnit | None
    settlement_state: SupplierBillSettlementStateT
    aging_bucket: SupplierBillAgingBucketT
    overdue: bool
    bill_payments: NotRequired[Sequence[SupplierBillPayment]]

class SupplierBillDelta(WorkflowOperationDelta):
    purchase: NotRequired[BaseReference]
    bill_date: NotRequired[float]
    due_date: NotRequired[float]
    reference: NotRequired[str | None]
    payment_terms_days: NotRequired[int]
    observations: NotRequired[str | None]

class SupplierBillPayload(BaseDelta):
    supplier_bill: SupplierBillDelta

class SupplierBillPayment(Operation):
    entry_type: SupplierBillPaymentTypeT
    applied_amount: float
    application_date: float
    currency: str
    request_key: str
    payment_method: str
    reversed: Literal[0, 1]
    reversal_date: float | None
    reversal_reason: str | None
    previous_balance: float
    resulting_balance: float
    settled_amount: float
    returned_amount: float
    supplier_bill: WorkflowOperation[SupplierBillStateT]
    source_bill: WorkflowOperation[SupplierBillStateT] | None
    supplier_return: Operation | None
    payment: Payment | None
    create_user: BaseUser | None
    modify_user: BaseUser | None

class SupplierBillPaymentDelta(BaseDelta):
    entry_type: NotRequired[SupplierBillPaymentTypeT]
    applied_amount: float
    application_date: NotRequired[float]
    currency: str
    request_key: str
    payment_method: NotRequired[
        Literal["BankTransferPayment", "CashPayment", "CheckPayment", "CustomPayment"]
    ]
    source_bill: NotRequired[BaseReference]
    supplier_return: NotRequired[BaseReference]

class SupplierBillPaymentPayload(BaseDelta):
    supplier_bill_payment: SupplierBillPaymentDelta

class SupplierBillReasonPayload(TypedDict):
    reason: str

class SupplierBillMessagePayload(TypedDict):
    body: str
    files: NotRequired[Sequence[tuple[str, str, bytes]]]

class SupplierBillBalance(TypedDict):
    supplier: Supplier
    currency: str
    outstanding_amount: float
    credit_amount: float
    paid_amount: float
    buckets: Mapping[SupplierBillAgingBucketT, float]

class SupplierBillReport(TypedDict):
    balances: Sequence[SupplierBillBalance]
    unconfirmed_count: int

class SupplierBillAPI(object):
    def list_supplier_bills(self, *args, **kwargs) -> Sequence[SupplierBill]: ...
    def get_permissions_supplier_bill(self) -> dict[str, bool]: ...
    def create_supplier_bill(self, payload: SupplierBillPayload) -> SupplierBill: ...
    def get_supplier_bill(self, object_id: int) -> SupplierBill: ...
    def update_supplier_bill(
        self, object_id: int, payload: SupplierBillPayload
    ) -> SupplierBill: ...
    def approve_supplier_bill(self, object_id: int) -> SupplierBill: ...
    def request_supplier_bill(self, object_id: int) -> ApprovalRequest: ...
    def cancel_supplier_bill(
        self, object_id: int, payload: SupplierBillReasonPayload
    ) -> SupplierBill: ...
    def report_supplier_bills(self, *args, **kwargs) -> SupplierBillReport: ...
    def export_supplier_bills(self, *args, **kwargs) -> str | bytes: ...
    def create_payment_supplier_bill(
        self, object_id: int, payload: SupplierBillPaymentPayload
    ) -> SupplierBillPayment: ...
    def request_payment_supplier_bill(
        self, object_id: int, payload: SupplierBillPaymentPayload
    ) -> ApprovalRequest: ...
    def reverse_payment_supplier_bill(
        self, object_id: int, payment_id: int, payload: SupplierBillReasonPayload
    ) -> SupplierBillPayment: ...
    def list_messages_supplier_bill(
        self, object_id: int
    ) -> Sequence[WorkflowEvent]: ...
    def create_message_supplier_bill(
        self, object_id: int, payload: SupplierBillMessagePayload
    ) -> WorkflowMessage: ...
    def update_message_supplier_bill(
        self, object_id: int, message_id: int, payload: SupplierBillMessagePayload
    ) -> WorkflowMessage: ...
    def delete_message_supplier_bill(
        self, object_id: int, message_id: int
    ) -> Result: ...
    def delete_file_message_supplier_bill(
        self, object_id: int, message_id: int, file_id: int
    ) -> Result: ...
