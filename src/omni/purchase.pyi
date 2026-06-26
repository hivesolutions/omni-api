from typing import Sequence

from .operation import Operation

class Purchase(Operation):
    pass

class PurchaseAPI(object):
    def list_purchases(self, *args, **kwargs) -> Sequence[Purchase]: ...
    def create_purchase(self, payload: Purchase) -> Purchase: ...
    def get_purchase(self, object_id: int) -> Purchase: ...
