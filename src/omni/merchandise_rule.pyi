from typing import Literal, NotRequired, Sequence, TypedDict

from .base import Base, BaseDelta, BaseReference
from .brand import Brand
from .merchandise import Merchandise

MerchandiseRuleTargetT = Literal[1, 2]
MerchandiseRuleTargetStringT = Literal["code", "name"]

class MerchandiseRuleTarget:
    CODE: Literal[1] = ...
    NAME: Literal[2] = ...

class MerchandiseRule(Base):
    name: str
    priority: int
    target: MerchandiseRuleTargetT
    pattern: str
    target_string: MerchandiseRuleTargetStringT
    group_: NotRequired[Merchandise | None]
    brand: NotRequired[Brand | None]
    categories: NotRequired[Sequence[Merchandise]]

class MerchandiseRuleDelta(BaseDelta):
    name: NotRequired[str]
    priority: NotRequired[int]
    target: NotRequired[MerchandiseRuleTargetT]
    pattern: NotRequired[str]
    group_: NotRequired[BaseReference]
    brand: NotRequired[BaseReference]
    categories: NotRequired[Sequence[BaseReference]]

class MerchandiseRulePayload(BaseDelta):
    merchandise_rule: MerchandiseRuleDelta

class MerchandiseRuleImport(TypedDict):
    name: str
    priority: NotRequired[int | None]
    target: NotRequired[MerchandiseRuleTargetT | MerchandiseRuleTargetStringT | None]
    pattern: NotRequired[str]
    group: NotRequired[str | None]
    brand: NotRequired[str | None]
    categories: NotRequired[Sequence[str] | None]

class MerchandiseRuleImportResult(TypedDict):
    created: int
    updated: int

class MerchandiseRuleAPI(object):
    def list_merchandise_rules(self, *args, **kwargs) -> Sequence[MerchandiseRule]: ...
    def create_merchandise_rule(
        self, payload: MerchandiseRulePayload
    ) -> MerchandiseRule: ...
    def get_merchandise_rule(self, object_id: int) -> MerchandiseRule: ...
    def update_merchandise_rule(
        self, object_id: int, payload: MerchandiseRulePayload
    ) -> MerchandiseRule: ...
    def import_merchandise_rules(
        self, items: Sequence[MerchandiseRuleImport]
    ) -> MerchandiseRuleImportResult: ...
