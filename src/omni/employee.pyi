from typing import Sequence

from .person import Person, PersonDelta
from .identifiable import Identifiable, IdentifiableDelta

class Employee(Person, Identifiable):
    pass

class EmployeeDelta(PersonDelta, IdentifiableDelta):
    pass

class EmployeeAPI(object):
    def list_employees(self, *args, **kwargs) -> Sequence[Employee]: ...
    def create_employee(self, payload: Employee) -> Employee: ...
    def get_employee(self, object_id: int) -> Employee: ...
    def update_employee(self, object_id: int, payload: EmployeeDelta) -> Employee: ...
    def self_employee(self) -> Employee: ...
    def stats_employee(
        self,
        date: float | None = ...,
        unit: str = ...,
        span: int = ...,
        store_id: int | None = ...,
        employee_id: int | None = ...,
        has_global: bool | None = ...,
        output: str = ...,
    ) -> dict: ...
