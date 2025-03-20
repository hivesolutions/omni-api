from .named import Named
from .address import Address
from .contact_information import ContactInformation

class Contactable(Named):
    observations: str | None
    tax_number: str | None
    preferred_name: str | None
    primary_contact_information: ContactInformation | None
    primary_address: Address | None
