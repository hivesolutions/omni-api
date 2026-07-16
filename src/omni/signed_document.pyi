from typing import Any, Literal, Mapping, NotRequired, Sequence, TypedDict

from .document import Document

class SignedDocument(Document):
    submitted_at: Literal[1, 2]
    submitted_at_version: int | None
    submitted_at_date: float | None
    submitted_at_server: str | None
    certificate_at_begin_date: float | None
    certificate_at_end_date: float | None
    certificate_at_common_name: str | None
    username_at: str | None
    at_document_identifier: str | None
    atcud: str | None
    signed: Literal[1, 2]
    system_entry_date: float
    price: float
    digest_document_type: str
    digest: str | None
    digest_chunk: str | None
    key_version: int | None

class SignedDocumentResult(TypedDict):
    result: str

class SubmitAtResult(SignedDocumentResult):
    payload: Mapping[str, Any]

class SignedDocumentAPI(object):
    def list_signed_documents(self, *args, **kwargs) -> Sequence[SignedDocument]: ...
    def qr_code_document(self, object_id: int) -> bytes: ...
    def digest_identifier_document(self, object_id: int) -> str: ...
    def verify_signed_document(self, object_id: int) -> SignedDocumentResult: ...
    def submit_invoice_at(self, object_id: int) -> SubmitAtResult: ...
    def submit_transport_at(self, object_id: int) -> SubmitAtResult: ...
