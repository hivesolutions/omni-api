from typing import Any, Callable, Mapping, Sequence, TextIO

STEP: int = ...

def to_string(value: Any, encoding: str | None = ...) -> Any: ...
def to_date(value: Any, encoding: str | None = ...) -> str: ...

FUNCS: Mapping[str, Callable[..., Any]] = ...

def get_field(
    object: Mapping[str, Any],
    name: str,
    encoding: str | None = ...,
    type_m: Mapping[str, str] = ...,
) -> Any: ...
def open_export(path: str) -> TextIO: ...
def export(
    file: TextIO,
    caller: Callable[..., Sequence[Mapping[str, Any]]],
    attributes: Sequence[str],
    names: Sequence[str] | None = ...,
    type_m: Mapping[str, str] | None = ...,
    step: int = ...,
    callback: Callable[[int, Sequence[Mapping[str, Any]]], Any] | None = ...,
) -> None: ...
