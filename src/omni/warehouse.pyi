from typing import NotRequired, Sequence

from .base import BaseDelta
from .store import FunctionalUnit, FunctionalUnitDelta

class Warehouse(FunctionalUnit):
    warehouse_code: str | None

class WarehouseDelta(FunctionalUnitDelta):
    warehouse_code: NotRequired[str | None]
    identifier_prefix: NotRequired[str]
    identifier_number_digits: NotRequired[int]

class WarehousePayload(BaseDelta):
    warehouse: WarehouseDelta

class WarehouseAPI(object):
    def list_warehouses(self, *args, **kwargs) -> Sequence[Warehouse]: ...
    def create_warehouse(self, payload: WarehousePayload) -> Warehouse: ...
    def get_warehouse(self, object_id: int) -> Warehouse: ...
    def update_warehouse(
        self, object_id: int, payload: WarehousePayload
    ) -> Warehouse: ...
    def delete_warehouse(self, object_id: int) -> None: ...
