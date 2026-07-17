from typing import Sequence

from .company import Company
from .contactable import Contactable
from .identifiable import Identifiable

class Supplier(Contactable, Identifiable):
    pass

class SupplierCompany(Company, Supplier):
    pass

class SupplierAPI(object):
    def list_suppliers(self, *args, **kwargs) -> Sequence[Supplier]: ...
