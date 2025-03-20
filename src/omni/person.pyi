from .contactable import Contactable

class Person(Contactable):
    surname: str | None
    gender: int | None
    national_id_number: str | None
    birth_date: float | None
    birth_day: str | None
