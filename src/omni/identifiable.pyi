from typing import TypedDict

class Identifiable(TypedDict):
    identifier: str
    extended_identifier: str
    identifier_prefix: str | None
    identifier_number_digits: int | None
    generated_identifier: int
    validation_code: str | None
