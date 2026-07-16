from typing import Literal, NotRequired

from .contactable import Contactable, ContactableDelta

class Gender:
    MALE: Literal[1] = ...
    FEMALE: Literal[2] = ...

class Person(Contactable):
    surname: str | None
    gender: Literal[1, 2] | None
    national_id_number: str | None
    birth_date: float | None
    birth_day: str | None

class PersonDelta(ContactableDelta):
    surname: NotRequired[str | None]
    gender: NotRequired[Literal[1, 2] | None]
    national_id_number: NotRequired[str | None]
    birth_date: NotRequired[float | None]
    birth_day: NotRequired[str | None]
