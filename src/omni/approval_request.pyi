from typing import Literal, NotRequired, Sequence, TypedDict

from .base import Base
from .employee import Employee
from .workflow_operation import WorkflowOperation

ApprovalRequestStateT = Literal[1, 2, 3, 4, 5, 6, 7, 8]

class ApprovalRequest(WorkflowOperation[ApprovalRequestStateT]):
    operation_type: str
    payload: str
    amount: float | None
    reason: str | None
    decision_reason: str | None
    decision_date: float | None
    maker: NotRequired[Employee | None]
    checker: NotRequired[Employee | None]
    result: NotRequired[Base | None]
    result_cid: int | None
    result_entity_name: str | None

class ApprovalRequestReasonPayload(TypedDict):
    reason: str

class ApprovalRequestAPI(object):
    def list_approval_requests(self, *args, **kwargs) -> Sequence[ApprovalRequest]: ...
    def get_approval_request(self, object_id: int) -> ApprovalRequest: ...
    def approve_approval_request(self, object_id: int) -> ApprovalRequest: ...
    def reject_approval_request(
        self, object_id: int, payload: ApprovalRequestReasonPayload
    ) -> ApprovalRequest: ...
    def withdraw_approval_request(self, object_id: int) -> ApprovalRequest: ...
