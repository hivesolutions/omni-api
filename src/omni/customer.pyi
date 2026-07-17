from typing import Literal, NotRequired, Sequence

from .base import BaseDelta
from .person import Person, PersonDelta
from .contactable import Contactable, ContactableDelta
from .identifiable import Identifiable, IdentifiableDelta

PhysicalSignatureT = Literal[1, 2, 3]

class PhysicalSignature:
    SIGNED: Literal[1] = ...
    NOT_SIGNED: Literal[2] = ...
    UNKNOWN: Literal[3] = ...

class Customer(Contactable, Identifiable):
    customer_code: str
    physical_signature: PhysicalSignatureT | None

class CustomerDelta(ContactableDelta, IdentifiableDelta):
    customer_code: NotRequired[str]
    physical_signature: NotRequired[PhysicalSignatureT | None]

class CustomerPerson(Person, Customer):
    pass

class CustomerPersonDelta(PersonDelta, CustomerDelta):
    pass

class CustomerPersonPayload(BaseDelta):
    customer_person: CustomerPersonDelta

class CustomerAPI(object):
    def list_customers(self, *args, **kwargs) -> Sequence[Customer]: ...
    def list_persons(self, *args, **kwargs) -> Sequence[CustomerPerson]: ...
    def get_person(self, object_id: int) -> CustomerPerson: ...
    def update_person(
        self, object_id: int, payload: CustomerPersonPayload
    ) -> CustomerPerson: ...
    @classmethod
    def customer_name(cls, person: CustomerPerson) -> str: ...
