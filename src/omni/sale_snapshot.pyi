from typing import Literal, NotRequired, Sequence, TypedDict

from .base import BaseDelta

StatsDirectionT = Literal["up", "down", "equal"]
""" The direction of an aggregated stats value
when compared against its target value """

class SaleStatsValue(TypedDict):
    value: float
    target: float
    percentage: float
    direction: StatsDirectionT

class SaleStatsTotals(TypedDict):
    number_sales: SaleStatsValue
    amount_price_vat: SaleStatsValue
    average_sale: SaleStatsValue
    number_returns: SaleStatsValue
    returned_price_vat: SaleStatsValue
    average_return: SaleStatsValue
    net_number_sales: SaleStatsValue
    net_price_vat: SaleStatsValue
    average_net: SaleStatsValue
    number_entries: SaleStatsValue
    entries_sale: SaleStatsValue
    entries_return: SaleStatsValue

class SaleStats(TypedDict):
    name: str
    number_sales: Sequence[int]
    amount_price_vat: Sequence[float]
    number_returns: Sequence[int]
    returned_price_vat: Sequence[float]
    net_number_sales: Sequence[int]
    net_price_vat: Sequence[float]
    number_entries: Sequence[int]
    totals: SaleStatsTotals

class EntryChunkDelta(TypedDict):
    store_id: NotRequired[int]
    count: int
    date: float

class EntryChunkPayload(BaseDelta):
    entry_chunk: EntryChunkDelta

class SaleSnapshotAPI(object):
    def entries_sales_snapshot(self, payload: EntryChunkPayload) -> None: ...
