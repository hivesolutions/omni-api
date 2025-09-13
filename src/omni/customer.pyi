from typing import NotRequired, Sequence

from .person import Person, PersonDelta
from .contactable import Contactable, ContactableDelta

class Customer(Contactable):
    customer_code: str
    physical_signature: int | None

class CustomerDelta(ContactableDelta):
    customer_code: NotRequired[str]
    physical_signature: NotRequired[int | None]

class CustomerPerson(Person, Customer):
    pass

class CustomerPersonDelta(PersonDelta, CustomerDelta):
    pass

class CustomerAPI(object):
    def list_customers(self, *args, **kwargs) -> Sequence[Customer]: ...
    def list_persons(self, *args, **kwargs) -> Sequence[CustomerPerson]: ...
    def get_person(self, object_id: int) -> CustomerPerson: ...
    def update_person(
        self, object_id: int, payload: CustomerPersonDelta
    ) -> CustomerPerson: ...
    @classmethod
    def customer_name(cls, person: CustomerPerson) -> str: ...
