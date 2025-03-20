from .base import Base

class Address(Base):
    address_type: str | None
    street_name: str | None
    door_number: str | None
    floor: str | None
    zip_code: str | None
    zip_code_name: str | None
    city: str | None
    state: str | None
    province: str | None
    country: str | None
