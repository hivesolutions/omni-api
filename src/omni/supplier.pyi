from typing import Sequence

from .person import Person
from .company import Company
from .contactable import Contactable
from .identifiable import Identifiable

class Supplier(Contactable, Identifiable):
    pass

class SupplierPerson(Person, Supplier):
    pass

class SupplierCompany(Company, Supplier):
    pass

class SupplierAPI(object):
    def list_suppliers(self, *args, **kwargs) -> Sequence[Supplier]: ...
    def list_companies(self, *args, **kwargs) -> Sequence[SupplierCompany]: ...
    def get_company(self, object_id: int) -> SupplierCompany: ...
