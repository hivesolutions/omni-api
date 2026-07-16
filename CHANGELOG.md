# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Completed type stubs for the remaining sale operations
* Type stubs for documents, signed documents, invoices, receipts, money sale slips, payments, companies and sale statistics
* Typed creation and update payloads validated against a live demo instance
* Agent skill describing how to author type stubs for API operations
* Enumerated integer fields typed as literal value sets

### Changed

*

### Fixed

* Update and create payload types now reflect the wrapped wire format expected by the server

## [0.9.0] - 2026-06-26

### Added

* Support for the list and get purchase operations in `PurchaseAPI`
* Support for the list and get consignment operations in `ConsignmentAPI`

## [0.8.0] - 2026-06-25

### Added

* Support for the update employee operation in `EmployeeAPI`

## [0.7.0] - 2026-06-25

### Changed

* Bumped `actions/checkout` from `v4` to `v7` in CI workflows
* Switched CI test execution to `pytest` and packaging to `python -m build`
* Updated deploy workflow to build under Python 3.12

## [0.6.0] - 2026-06-25

### Added

* Type stub for `stats_employee` method in `EmployeeAPI`
* Support for the create employee operation in `EmployeeAPI`

## [0.5.5] - 2024-09-15

### Added

* New support for Merchandise operations

## [0.5.4] - 2024-09-13

### Added

* Support for `InventoryCheck` entity and model
* More types for known operations

## [0.5.3] - 2024-04-20

### Added

* Definition of the `Task` class

### Fixed

* Dictionary structure of the payload structures

## [0.5.2] - 2024-04-10

### Changed

* Improved payload values for SAFT-PT API

## [0.5.1] - 2024-04-10

### Added

* Support for `SaftPtAPI` API methods

### Changed

* Made code `black` compliant
* Removed extra elements of Python files header

## [0.5.0] - 2023-01-19

### Added

* Support for the `digest_identifier_document()` method
* Support for the `ReceiptAPI`
* Support for issue and ensure receipt operations for `SaleAPI`

## [0.4.3] - 2023-01-06

### Added

* Support for the `get_status` method

## [0.4.2] - 2023-01-04

### Added

* Support for the update self on `SystemCompany`

### Changed

* Renamed repository

## [0.4.1] - 2022-02-05

### Added

* Long description added to `setup.py`

### Fixed

* More secure handling of errors

## [0.4.0] - 2021-12-30

### Added

* Support for QR Code route in `signed_document` entity
