from typing import NotRequired
from .named import Named, NamedDelta
from .address import Address
from .contact_information import ContactInformation

class Contactable(Named):
    observations: str | None
    tax_number: str | None
    preferred_name: str | None
    primary_contact_information: ContactInformation | None
    primary_address: Address | None

class ContactableDelta(NamedDelta):
    observations: NotRequired[str | None]
    tax_number: NotRequired[str | None]
    preferred_name: NotRequired[str | None]
    primary_contact_information: NotRequired[ContactInformation | None]
    primary_address: NotRequired[Address | None]
