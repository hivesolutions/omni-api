# Add API Types - Template

Skeleton for `src/omni/<module>.pyi`, mirroring the structure of `sale.pyi`. Save with CRLF line endings, run `black .` after filling it in and register the API mixin in `base.pyi`. No license header - stub files start directly at the imports. Relative imports are ordered by module name length (ties alphabetical), matching the codebase style.

```python
from typing import Any, Mapping, NotRequired, Sequence, TypedDict

from .base import BaseDelta, BaseReference
from .operation import Operation, OperationDelta

class EntityName(Operation):
    # scalars: required keys; mandatory=True -> bare type, otherwise -> X | None
    some_flag: int
    some_code: str | None
    # relations: required when eager in both list and show, otherwise NotRequired
    some_relation: NotRequired[Sequence[EntityLine]]

class EntityNameDelta(OperationDelta):
    # partial write body: NotRequired unless the operation functionally requires it,
    # never include secure=True or immutable fields
    some_flag: NotRequired[int]
    owner: NotRequired[BaseReference]
    _parameters: NotRequired[Mapping[str, Any]]

class EntityNamePayload(BaseDelta):
    # key = the Omni model class name in underscore notation
    entity_name: EntityNameDelta

class EntityNameResult(TypedDict):
    # ad-hoc return map, derived from what the controller serializes
    result: str

class EntityNameAPI(object):
    def list_entity_names(self, *args, **kwargs) -> Sequence[EntityName]: ...
    def create_entity_name(self, payload: EntityNamePayload) -> EntityName: ...
    def get_entity_name(self, object_id: int) -> EntityName: ...
    def update_entity_name(
        self, object_id: int, payload: EntityNamePayload
    ) -> EntityName: ...
```

Checklist after filling in:

- [ ] Every public class and method of the `.py` module is stubbed (a `.pyi` replaces the module)
- [ ] New intermediate hierarchy classes created where missing (entity and `Delta` sides)
- [ ] API mixin imported and registered in `base.pyi` (alphabetical imports, `base.py` bases order)
- [ ] `black --check` clean, `pyright --pythonversion 3.13` clean, CRLF endings preserved
- [ ] Wire format verified against the Omni controller (or a live demo instance for writes)
- [ ] `CHANGELOG.md` updated under `## [Unreleased]`
