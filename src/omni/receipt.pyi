from typing import Sequence

from .signed_document import SignedDocument

class Receipt(SignedDocument):
    pass

class ReceiptAPI(object):
    @classmethod
    def normalize_receipt(cls, receipt: Receipt) -> None: ...
    def list_receipts(self, *args, **kwargs) -> Sequence[Receipt]: ...
    def get_receipt(self, object_id: int) -> Receipt: ...
