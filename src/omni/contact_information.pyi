from .base import Base

class ContactInformation(Base):
    contact_type: str | None
    mobile_phone_number: str | None
    phone_number: str | None
    fax_number: str | None
    email: str | None
    web_page: str | None
    facebook_id: str | None
    twitter_id: str | None
