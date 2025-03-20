from typing import Sequence

from .person import Person
from .contactable import Contactable

class Customer(Contactable):
    customer_code: str
    physical_signature: int | None

class CustomerPerson(Person, Customer):
    pass

class CustomerAPI(object):
    def list_customers(self, *args, **kwargs) -> Sequence[Customer]: ...
    def list_persons(self, *args, **kwargs) -> Sequence[CustomerPerson]: ...
    def get_person(self, object_id: int) -> CustomerPerson: ...
    @classmethod
    def customer_name(cls, person: CustomerPerson) -> str: ...
