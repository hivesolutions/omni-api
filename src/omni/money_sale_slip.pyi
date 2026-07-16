from typing import Sequence

from .signed_document import SignedDocument

class MoneySaleSlip(SignedDocument):
    pass

class MoneySaleSlipAPI(object):
    @classmethod
    def normalize_money_sale_slip(cls, money_sale_slip: MoneySaleSlip) -> None: ...
    def list_money_sale_slips(self, *args, **kwargs) -> Sequence[MoneySaleSlip]: ...
    def get_money_sale_slip(self, object_id: int) -> MoneySaleSlip: ...
