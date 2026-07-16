from typing import NotRequired

from .contactable import Contactable, ContactableDelta

class Company(Contactable):
    ownership_equity: float | None
    corporate_registration_entity: str | None
    corporate_registration_code: str | None

class CompanyDelta(ContactableDelta):
    ownership_equity: NotRequired[float | None]
    corporate_registration_entity: NotRequired[str | None]
    corporate_registration_code: NotRequired[str | None]
