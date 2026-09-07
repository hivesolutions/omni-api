#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Omni ERP. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from typing import TYPE_CHECKING
from unittest import TestCase
from unittest.mock import MagicMock

from .base import build_mock

if TYPE_CHECKING:
    from omni.supplier_bill import (
        SupplierBillPayload,
        SupplierBillPaymentPayload,
        SupplierBillInstalmentPayload,
        SupplierBillSchedulePayload,
        SupplierBillReasonPayload,
        SupplierBillMessagePayload,
    )


class SupplierBillTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_supplier_bills(self) -> None:
        result = self.api.list_supplier_bills(
            filters=["supplier:equals:7"], start_record=10, number_records=5
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs,
            dict(filters=["supplier:equals:7"], start_record=10, number_records=5),
        )

    def test_get_permissions_supplier_bill(self) -> None:
        result = self.api.get_permissions_supplier_bill()

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/permissions.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_create_supplier_bill(self) -> None:
        payload: SupplierBillPayload = {
            "supplier_bill": {"purchase": {"object_id": 10}, "reference": "statement-1"}
        }
        result = self.api.create_supplier_bill(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_get_supplier_bill(self) -> None:
        result = self.api.get_supplier_bill(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_supplier_bill(self) -> None:
        payload: SupplierBillPayload = {"supplier_bill": {"reference": "statement-1"}}
        result = self.api.update_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_approve_supplier_bill(self) -> None:
        result = self.api.approve_supplier_bill(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/approve.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_request_supplier_bill(self) -> None:
        result = self.api.request_supplier_bill(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/request.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_cancel_supplier_bill(self) -> None:
        payload: SupplierBillReasonPayload = {"reason": "Incorrect reference"}
        result = self.api.cancel_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills/1/cancel.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_report_supplier_bills(self) -> None:
        result = self.api.report_supplier_bills(
            filters=["supplier:equals:7"], start_record=10, number_records=5
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills/report.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs,
            dict(filters=["supplier:equals:7"], start_record=10, number_records=5),
        )

    def test_export_supplier_bills(self) -> None:
        result = self.api.export_supplier_bills(
            filters=["supplier:equals:7"], start_record=10, number_records=5
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_bills/export.csv")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs,
            dict(filters=["supplier:equals:7"], start_record=10, number_records=5),
        )

    def test_create_payment_supplier_bill(self) -> None:
        payload: SupplierBillPaymentPayload = {
            "supplier_bill_payment": {
                "entry_type": 1,
                "applied_amount": 30,
                "currency": "EUR",
                "description": "Statement 1",
                "request_key": "statement-1",
            }
        }
        result = self.api.create_payment_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/payments.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_request_payment_supplier_bill(self) -> None:
        payload: SupplierBillPaymentPayload = {
            "supplier_bill_payment": {
                "entry_type": 1,
                "applied_amount": 30,
                "currency": "EUR",
                "description": "Statement 1",
                "request_key": "statement-1",
            }
        }
        result = self.api.request_payment_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/payments/request.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_reverse_payment_supplier_bill(self) -> None:
        payload: SupplierBillReasonPayload = {"reason": "Incorrect reference"}
        result = self.api.reverse_payment_supplier_bill(1, 2, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/payments/2/reverse.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_create_instalment_supplier_bill(self) -> None:
        payload: SupplierBillInstalmentPayload = {
            "supplier_bill_instalment": {"amount": 30, "due_date": 1790812800}
        }
        result = self.api.create_instalment_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/instalments.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_update_instalment_supplier_bill(self) -> None:
        payload: SupplierBillInstalmentPayload = {
            "supplier_bill_instalment": {"amount": 30, "due_date": 1790812800}
        }
        result = self.api.update_instalment_supplier_bill(1, 2, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/instalments/2/update.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_list_schedules_supplier_bill(self) -> None:
        result = self.api.list_schedules_supplier_bill(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/schedules.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_create_schedule_supplier_bill(self) -> None:
        payload: SupplierBillSchedulePayload = {
            "supplier_bill_schedule": {
                "name": "Monthly",
                "amount": 30,
                "interval_days": 30,
                "next_due_date": 1790812800,
            }
        }
        result = self.api.create_schedule_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/schedules.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_update_schedule_supplier_bill(self) -> None:
        payload: SupplierBillSchedulePayload = {
            "supplier_bill_schedule": {
                "name": "Monthly",
                "amount": 30,
                "interval_days": 30,
                "next_due_date": 1790812800,
            }
        }
        result = self.api.update_schedule_supplier_bill(1, 2, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/schedules/2/update.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_list_messages_supplier_bill(self) -> None:
        result = self.api.list_messages_supplier_bill(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/messages.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_create_message_supplier_bill(self) -> None:
        payload: SupplierBillMessagePayload = {"body": "Receipt reference"}
        result = self.api.create_message_supplier_bill(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/messages.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_update_message_supplier_bill(self) -> None:
        payload: SupplierBillMessagePayload = {"body": "Receipt reference"}
        result = self.api.update_message_supplier_bill(1, 2, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/messages/2/update.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_delete_message_supplier_bill(self) -> None:
        result = self.api.delete_message_supplier_bill(1, 2)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "DELETE")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/messages/2.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_delete_file_message_supplier_bill(self) -> None:
        result = self.api.delete_file_message_supplier_bill(1, 2, 3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "DELETE")
        self.assertEqual(
            url, "http://localhost:8080/omni/supplier_bills/1/messages/2/files/3.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_error(self) -> None:
        error = RuntimeError("Permission denied")
        self.api.get = MagicMock(side_effect=error)
        with self.assertRaises(RuntimeError) as context:
            self.api.get_supplier_bill(1)
        self.assertEqual(context.exception, error)

    def test_message_payload_options_supplier_bill(self) -> None:
        files = [("receipt.pdf", "application/pdf", b"receipt data")]
        payload: SupplierBillMessagePayload = {"body": "Receipt", "files": files}
        self.api.create_message_supplier_bill(1, payload)
        self.api.update_message_supplier_bill(1, 2, payload)
        for method, url, kwargs in self.api.requests:
            self.assertEqual(method, "POST")
            self.assertEqual(kwargs["data_m"], payload)
            self.assertEqual(kwargs["data_m"]["files"][0][2], b"receipt data")
        self.assertEqual(payload.get("files"), files)
        self.assertEqual(
            self.api._message_payload_options_supplier_bill(
                dict(body="Receipt", files=[])
            ),
            dict(data_j=dict(body="Receipt")),
        )
