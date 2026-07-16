from typing import Sequence

from .signed_document import SignedDocument

class Invoice(SignedDocument):
    pass

class InvoiceAPI(object):
    @classmethod
    def normalize_invoice(cls, invoice: Invoice) -> None: ...
    def list_invoices(self, *args, **kwargs) -> Sequence[Invoice]: ...
    def get_invoice(self, object_id: int) -> Invoice: ...
