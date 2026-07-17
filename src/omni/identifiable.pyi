from typing import NotRequired, Sequence, TypedDict

class Identifiable(TypedDict):
    object_id: int
    instance_id: int | None
    representation: str | None
    identifier: str
    extended_identifier: str
    identifier_prefix: str | None
    identifier_number_digits: int | None
    identifier_sequence: int
    generated_identifier: int
    validation_code: str | None

class IdentifiableDelta(TypedDict):
    identifier: NotRequired[str | None]
    extended_identifier: NotRequired[str | None]
    identifier_prefix: NotRequired[str | None]
    identifier_number_digits: NotRequired[int | None]
    validation_code: NotRequired[str | None]

class IdentifiableAPI(object):
    def list_identifiables(self, *args, **kwargs) -> Sequence[Identifiable]: ...
