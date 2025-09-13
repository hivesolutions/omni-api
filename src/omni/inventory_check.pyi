from typing import Sequence

from .operation import Operation

class InventoryCheck(Operation):
    pass

class InventoryCheckAPI(object):
    def list_inventory_checks(self, *args, **kwargs) -> Sequence[InventoryCheck]: ...
    def get_inventory_check(self, object_id: int) -> InventoryCheck: ...
