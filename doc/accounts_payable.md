# Accounts Payable

Supplier bills link existing purchases to their payment workflow. The examples use an authenticated client configured as described in [Usage](../README.md#usage). Read the [settlement contract](https://github.com/hivesolutions/omni/blob/master/doc/design/010-accounts_payable.md) for opening balances, supplier credits, returns, currency handling and reversals.

## Creating a Supplier Bill

Create a bill for an existing purchase with its supplier reference and payment terms. The `purchase` relation is required when creating a bill. Updates can omit it; the linked purchase cannot be changed.

```python
bill = api.create_supplier_bill({
    "supplier_bill": {
        "purchase": {"object_id": 10},
        "reference": "INV/2026/1",
        "payment_terms_days": 30,
    }
})
```

## Confirming the Opening Balance

Entry type 2 records a historical adjustment and explicitly confirms the opening balance without creating a payment. A zero adjustment confirms the balance without reducing it.

```python
api.create_payment_supplier_bill(bill["object_id"], {
    "supplier_bill_payment": {
        "entry_type": 2,
        "applied_amount": 0,
        "currency": bill["currency"],
        "description": "Opening balance confirmed against supplier statement",
        "request_key": "statement-2026-1",
    }
})
```

## Registration Types

Use `create_payment_supplier_bill` for the following registrations:

| Entry Type | Registration          | Effect                                                 |
| ---------- | --------------------- | ------------------------------------------------------ |
| 1          | Payment               | Records a payment already made                         |
| 2          | Historical adjustment | Records historical settlement and confirms the balance |
| 3          | Supplier credit       | Records credit against the bill                        |
| 4          | Refund                | Records a received supplier refund                     |
| 5          | Credit transfer       | Applies available credit from another bill             |

These methods do not initiate provider payments. Use a stable request key when retrying the same registration; the server rejects duplicate registrations.

## Permissions

`get_permissions_supplier_bill` returns the server's action permissions. All routes continue to enforce permissions and validate the current balance on the server.

## Reports and Exports

`list_supplier_bills`, `report_supplier_bills` and `export_supplier_bills` accept the usual filter arguments. Export returns CSV bytes.

## Attachments

Attach receipts through the bill's workflow messages. Each file contains its name, content type and bytes.

```python
api.create_message_supplier_bill(
    bill["object_id"],
    {"body": "Receipt", "files": [("receipt.txt", "text/plain", b"Receipt")]},
)
```
