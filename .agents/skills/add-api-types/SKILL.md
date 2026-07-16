---
name: add-api-types
description: Add or complete .pyi type stubs for Omni API operations. Use when typing a new API method or entity, covering read entity types, Delta/Payload write types, hierarchy alignment and verification of the real wire format against the Omni server source or a live instance.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Add API Types

Type an API operation end-to-end: the read entity, the write `Delta`/`Payload` types, the API method signatures and the registration in `base.pyi`, all derived from the Omni server source (not guessed from the client code).

## Files

- `src/omni/<module>.pyi` - mirrors `src/omni/<module>.py`; a stub file replaces the module for type checkers, so every public class and method of the `.py` must be stubbed or it disappears from the API type
- Type-only modules (no `.py` counterpart) are an established pattern (`price.pyi`, `person.pyi`, `operation.pyi`, `purchase_line.pyi`)
- `src/omni/base.pyi` - `Base` (the Omni `RootEntity`), `BaseDelta`, `BaseReference` and the `API` class that registers every stubbed API mixin
- The Omni server repo (sibling checkout, eg: `../omni`) - controllers and models are the source of truth for shapes
- `CHANGELOG.md` - entry under `## [Unreleased]` per the house style

## Instructions

1. **Locate the server-side truth** in the Omni repo: the route tuple in `<module>/src/omni_<module>/system.py` maps the URL to a controller action; the controller shows the wire contract (which request fields it reads, what it serializes); the model shows the fields (`mandatory`, `secure`, `immutable` flags), `set_validation()` and the calculated attributes (`_attr_*` methods).
2. **Pick the type kinds** needed from the Type Kinds table below and read the matching worked example in [examples.md](examples.md).
3. **Write the read entity** per the Field Typing Rules below, anchored at the right level of the hierarchy (`Base` = `RootEntity`, `Operation(Base, Identifiable)`, `SignedDocument(Document(Base, Identifiable))`, `Contactable(Named(Base))`). If an intermediate class in the chain does not exist in the stubs yet, create it - never short-circuit to `Base`.
4. **Write the `Delta`** mirroring the entity chain at the same level (`Sale(Operation)` -> `SaleDelta(OperationDelta)`). Exclude `secure=True` and `immutable` fields - colony's apply silently skips secure attributes, so typing them would promise something the server ignores. Reference relations with `BaseReference` (`{object_id}`); polymorphic relations take a `_class` key (see `PaymentMethodDelta`).
5. **Write the `Payload` wrapper** per the Payload Wire Format section - the wrapper is the actual request body, the `Delta` is the value under the model-name key.
6. **Place each type in the module** mirroring the Omni model layout: line types live in their own `<x>_line.pyi` (like `sale_line.pyi`), documents under `document.pyi`/`signed_document.pyi`, and so on.
7. **Register any new API mixin** in `base.pyi`: imports in alphabetical order, class bases in the same relative order as `base.py`.
8. **Format and check**: `black` formatting, `pyright --pythonversion 3.13` with zero errors, CRLF line endings preserved (the whole repo uses CRLF).
9. **Verify against a live instance** whenever the operation writes or the serialization is uncertain - see Live Testing below. A payload type is only proven when the same body both passes the type checker and succeeds on the wire.
10. **Update `CHANGELOG.md`** under `## [Unreleased]` (one short high-level bullet, no code identifiers).

## Type Kinds

| Kind        | Naming                                   | Base class                          | Used for                                                  |
| ----------- | ----------------------------------------- | ------------------------------------ | ---------------------------------------------------------- |
| Read entity | entity name (`Sale`, `Invoice`)          | mirrors the Omni model chain        | returns of list/get and issue operations                  |
| Delta       | `<Entity>Delta`                          | parent's `Delta` (`OperationDelta`) | partial write bodies (create/update)                      |
| Payload     | `<Entity>Payload`                        | `BaseDelta`                         | the request body wrapper actually sent on the wire        |
| Result map  | descriptive (`SaleVat`, `SubmitAtResult`) | `TypedDict`                         | ad-hoc endpoint returns that are not entity serializations |
| Reference   | `BaseReference`                          | `TypedDict`                         | `{object_id}` relation references inside deltas           |

## Field Typing Rules

Read entities model the list/get contract - in a list or get operation every field is set, if anything with a `None` value:

- Scalars are always required keys: `mandatory=True` -> bare type; non-mandatory -> `X | None`. Never `NotRequired` on a scalar of a read entity - that is Delta territory.
- Relations are required when eager-loaded in both the list and show retrievals (check the controller filter and the model's `get_for_show`), eg: `Sale.price`, `Sale.customer`. Otherwise `NotRequired` - the relation can be eventually not loaded, eg: `Sale.sale_lines` (only on get), `Document.issue_operation`.
- Calculated attributes (`_attr_*` methods, eg: `price_vat`, `digest_chunk`) serialize only in `map=True` flows but are still typed required per the list/get contract.
- Create/update/issue responses go through `get_map(recursive=False)`: reduced maps without relations or calculated attributes. The list/get contract still wins - do not degrade the read entity because of them.
- Every serialized entity carries `_class` and `metadata` (not `meta`) - both live on `Base`.
- Enumerated fields carry their semantics twice, following the `TaskState` precedent: a `T`-suffixed `Literal` alias types the field (`DocumentStatusT = Literal[1, 2, 3]`, `document_status: DocumentStatusT`) and a runtime namespace class in the `.py` module holds the named constants (`class DocumentStatus(object): DRAFT = 1; PRINTED = 2; COMPLETED = 3`, at the bottom of the module), declared in the stub with `Literal[N]`-typed attributes so `doc["document_status"] == DocumentStatus.COMPLETED` narrows. Values come from the Omni model constants; the shared `StatusT`/`Status` and `FlagT`/`Flag` (the 1 - yes, 2 - no pattern) pairs live in `base`; export the classes from `__init__.py` like `TaskState`. Never an `IntEnum` - the wire values are plain ints.

Deltas are partial by definition:

- All fields `NotRequired` except the ones the operation functionally requires (`SaleDelta` keeps `sale_lines` and `primary_payment` required; `SaftPtReportDelta` keeps `fiscal_year` required).
- Financial totals are computed server-side for sales (`calculate_financials` from the inventory line prices) - the client sends only lines and payments, never `vat`/`price` (they are `secure` anyway).

## Payload Wire Format

- `Model.new(request)` and `get_for_edit(id, apply=True)` read the request field named after the model class in underscore notation (colony `to_underscore`): `{"employee": {...}}`, `{"system_company": {...}}`, `{"transactional_merchandise": {...}}`. Hence `<Entity>Payload(BaseDelta)` with a single `<underscore_name>` key.
- A flat body is silently ignored - no error, no change (verified live). This is the reason flat payload types are bugs.
- Some controllers read explicit fields instead: sale create reads `transaction` + `customer` + `lines`; purchase create reads `purchase_transaction` + `document`; a bare JSON list body surfaces as the `root` field (merchandise prices/costs).
- Customer selection on sale create rides on `_parameters`: `{"type": "new" | "existing" | "anonymous"}` (plus `object_id` for `existing`).

## Verification

Static checks, always required before committing:

```bash
python3 -m black --check src/omni/*.pyi
npx pyright --pythonversion 3.13 src/omni/*.pyi
file src/omni/*.pyi | grep -vc CRLF   # must print 0
```

## Live Testing

Testing against a live local Omni API is one of the best ways to validate the structure of the API: reading the server source tells you what should happen, but only a real request shows the exact keys, nullability and reduced response maps on the wire. Prefer it over source reading alone whenever a write operation or an uncertain serialization is involved.

1. **Boot a disposable demo instance** from the Omni repo (sibling checkout), with an isolated sqlite database - never reuse the repo `.env` as-is, its `DB_URL` targets a live database:

   ```bash
   cd ../omni
   env -i HOME="$HOME" PATH="$PWD/.venv/bin:/usr/bin:/bin" \
       RUN_MODE=development COLONY_CONFIG_FILE=config/python/singleton.py \
       PLUGIN_PATH='./*/src;./*/*src;../colony-*/*/src;../colony-*/*/*src' \
       META_PATH='../colony-config/*;../omni-config/*' \
       DB_ENGINE=sqlite DB_FILE=demo_audit.db RESET_DB=1 AT_TEST_MODE=1 \
       .venv/bin/python scripts/load_demo_data.py
   # then the same env plus:
   #   COLONY_PREFIX=/mvc SERVER=netius HOST=127.0.0.1 PORT=8082
   #   SESSION=file SESSION_PATH=./session ALIAS_PATH=./assets/extra/alias.json
   # and run: .venv/bin/colony_wsgi
   ```

2. **Connect with the client itself**: with `COLONY_PREFIX=/mvc` the prefix is prepended internally, so the client `base_url` must NOT include `/mvc` (`http://127.0.0.1:8082/`). Demo credentials live in `data/demo/users.json` (eg: `root` / `Root@12345`).
3. **Dump and compare key sets** for each response family: list, get, and the create/update/issue returns. This is where the read rules come from - which keys are always present, which are `None`, which relations appear only when eager-loaded, and how much smaller the `get_map(recursive=False)` responses are.
4. **Probe write payloads empirically**: send the flat body and the wrapped body and diff the effect (a flat body returning 200 while changing nothing is the wrapper proof). Use the server log's validation errors as discovery - messages like `payments - paid amount is not 6.99` or `sale_lines - relation validation failed` enumerate exactly what the payload is missing.
5. **Finish with a typed client script**: one script that annotates its payloads and reads with the new types, run twice - through pyright and against the live server. The type is only proven when both pass on the same code.

The instance is disposable: demo data can be reloaded at will with `RESET_DB=1`, so exercising creates and updates against it is safe.

## Gotchas

- `.pyi` files use CRLF like the rest of the repo; write them byte-exact, editors and scripts may silently convert.
- `NotRequired` is imported from `typing`, which requires the checker to target Python 3.11+ (`--pythonversion 3.13`).
- A TypedDict subclass cannot re-declare an inherited key with a different type - declare shared keys once at the right level (eg: `payload` on `Document`, not per document subclass).
- Stats endpoints return the `simple` shape by default: a mapping keyed by object id string with `"-1"` for the global aggregate; `output="extended"` is a different envelope entirely.
- Never point a local test run at the Omni repo `.env` as-is - its `DB_URL` targets a live database; always override with an isolated sqlite `DB_FILE`.
