from typing import Sequence

from .person import Person, PersonDelta
from .identifiable import Identifiable, IdentifiableDelta

class Employee(Person, Identifiable):
    pass

class EmployeeDelta(PersonDelta, IdentifiableDelta):
    pass

class EmployeeAPI(object):
    def list_employees(self, *args, **kwargs) -> Sequence[Employee]: ...
    def get_employee(self, object_id: int) -> Employee: ...
    def self_employee(self) -> Employee: ...
