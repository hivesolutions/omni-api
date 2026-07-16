# Add API Types - Examples

Real exemplars from `src/omni/`, one per type kind. Read the exemplar before writing the new type and copy its structure and field ordering. Each was validated with pyright and against a live demo Omni instance - testing against the live local Omni API is one of the best ways to validate the structure of the API, and several of the shapes below (the payload wrappers, the reduced create responses, the nullable VAT list) were only discovered that way.

## Read entity - `Sale` (`sale.pyi`)

Mirrors the Omni `SaleTransaction(Sale(Operation))` model, anchored as `Sale(Operation)` with `Operation(Base, Identifiable)`.

- Mandatory scalars are bare types (`vat: float`, `payment_state: int`); non-mandatory scalars are required keys with `| None` (`vat_exemption_code: str | None`, `financial_discount: float | None`).
- `price: Price` and `customer: Customer | None` are required because the list and show controllers both eager-load them; `sale_lines: NotRequired[Sequence[SaleLine]]` because lines are only loaded on get.
- Calculated attributes (`price_vat`, `no_discount_price_vat`) are typed required per the list/get contract even though `create_sale`'s reduced response omits them.

## Delta and Payload - `SaleDelta` / `SalePayload` (`sale.pyi`)

The sale create controller reads `transaction`, `customer` and `lines` fields, so the payload is not a single-key wrapper:

```python
class SaleDelta(OperationDelta):
    stock_deduction_type: NotRequired[int]
    owner: NotRequired[BaseReference]
    primary_seller: NotRequired[BaseReference]
    sale_lines: Sequence[SaleLineDelta]
    primary_payment: PaymentDelta
    _parameters: NotRequired[Mapping[str, Any]]

class SalePayload(BaseDelta):
    transaction: SaleDelta
    customer: SaleCustomer
    lines: NotRequired[Sequence[SaleLineDelta]]
```

Minimal body proven against the demo instance (financials are computed server-side from inventory prices; payments must equal the price with VAT):

```json
{
    "transaction": {
        "sale_lines": [{"merchandise": {"object_id": 401}, "quantity": 1}],
        "primary_payment": {
            "payment_lines": [{
                "amount": {"value": 6.99},
                "payment_method": {"_class": "CashPayment"}
            }]
        }
    },
    "customer": {"_parameters": {"type": "anonymous"}}
}
```

Note what is absent: `vat`, `price` and per-line `unit_price` are `secure` fields, silently skipped by apply - they are excluded from the deltas on purpose.

## Single-key Payload wrapper - `EmployeePayload` (`employee.pyi`)

`Model.new(request)` / `get_for_edit(apply=True)` read the field named after the model class in underscore notation:

```python
class EmployeePayload(BaseDelta):
    employee: EmployeeDelta
```

Live evidence for the wrapper: posting `{"description": "X"}` flat returns 200 and changes nothing; posting `{"employee": {"description": "X"}}` applies the change. The same pattern covers `SystemCompanyPayload`, `CustomerPersonPayload`, `MerchandisePayload` and `PurchasePayload` (which adds the `document` field read explicitly by the purchase create controller).

## Hierarchy-complete line module - `purchase_line.pyi`

`PurchaseMerchandise(RootEntity)` in Omni becomes a dedicated type-only module mirroring `sale_line.pyi`, holding both the read entity and its delta:

```python
class PurchaseLine(Base):
    quantity: float
    ...
    unit_price: Price
    merchandise: TransactionalMerchandise

class PurchaseLineDelta(BaseDelta):
    merchandise: BaseReference
    quantity: float
    unit_price: NotRequired[PriceDelta]
```

Purchase line `unit_price` is writable (not `secure`), unlike the sale line one - always check the field flags before including a field in a delta.

## Result maps - `SaleVat`, `VatItem`, `SaleStats` (`sale.pyi`, `operation.pyi`, `sale_snapshot.pyi`)

Ad-hoc endpoint returns that are not entity serializations get descriptive `TypedDict` types derived from the serializing code:

- `SaleVat.vat_list` is `Sequence[VatItem] | None` because `get_vat_list()` returns `None` when the VAT table cannot be computed and the controller serializes it anyway.
- `VatItem.reason` is `NotRequired[str | None]` because only the sale-family `get_vat_list()` implementations add it - purchase and consignment ones do not.
- `SaleStats` mirrors `SaleSnapshot._set_snapshot_stats` (the per-slot series lists) and `SaleStatsTotals` mirrors `_aggregate_stats` (the twelve aggregates), each aggregate being a `SaleStatsValue` from `aggregate_values` (`value`/`target`/`percentage`/`direction`). The return of `stats_sales` is `Mapping[str, SaleStats]` keyed by store object id string, `"-1"` for the global aggregate.
