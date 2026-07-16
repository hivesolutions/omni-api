from typing import Literal, NotRequired

from .base import BaseDelta
from .company import Company, CompanyDelta

class SystemCompany(Company):
    domain: str
    slogan: str | None
    phone_note: str | None
    fiscal_year_start: int
    fiscal_year_end: int
    retail: Literal[1, 2] | None

class SystemCompanyDelta(CompanyDelta):
    slogan: NotRequired[str | None]
    phone_note: NotRequired[str | None]
    fiscal_year_start: NotRequired[int]
    fiscal_year_end: NotRequired[int]
    retail: NotRequired[Literal[1, 2] | None]

class SystemCompanyPayload(BaseDelta):
    system_company: SystemCompanyDelta

class SystemCompanyAPI(object):
    def load_system_company(self) -> None: ...
    def self_system_company(self) -> SystemCompany: ...
    def update_self_system_company(
        self, payload: SystemCompanyPayload
    ) -> SystemCompany: ...
    def media_system_company(
        self,
        position: int | None = ...,
        dimensions: str | None = ...,
        label: str | None = ...,
    ) -> bytes: ...
    def public_media_system_company(
        self,
        position: int | None = ...,
        dimensions: str | None = ...,
        label: str | None = ...,
    ) -> bytes: ...
