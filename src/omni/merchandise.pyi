from typing import Sequence
from .named import Named

class Merchandise(Named):
    pass

class TransactionalMerchandise(Merchandise):
    company_product_code: str

class MerchandiseAPI(object):
    def list_merchandise(self, *args, **kwargs) -> Sequence[Merchandise]: ...
