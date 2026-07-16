from typing import NotRequired

from .contactable import Contactable, ContactableDelta

class Person(Contactable):
    surname: str | None
    gender: int | None
    national_id_number: str | None
    birth_date: float | None
    birth_day: str | None

class PersonDelta(ContactableDelta):
    surname: NotRequired[str | None]
    gender: NotRequired[int | None]
    national_id_number: NotRequired[str | None]
    birth_date: NotRequired[float | None]
    birth_day: NotRequired[str | None]
