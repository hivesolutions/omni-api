from typing import Sequence, TypedDict

class Identifiable(TypedDict):
    identifier: str
    extended_identifier: str
    identifier_prefix: str | None
    identifier_number_digits: int | None
    generated_identifier: int
    validation_code: str | None

class IdentifiableAPI(object):
    def list_identifiables(self, *args, **kwargs) -> Sequence[Identifiable]: ...
