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

from os import environ
from unittest import TestCase
from typing import TYPE_CHECKING

from omni import API, Flag, PaymentState

from .base import build_mock


if TYPE_CHECKING:
    from omni.sale import SalePayload


class SaleTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_create_sale(self) -> None:
        payload: SalePayload = {
            "transaction": {
                "sale_lines": [{"merchandise": {"object_id": 1}, "quantity": 1}],
                "primary_payment": {
                    "payment_lines": [
                        {
                            "amount": {"value": 10.0},
                            "payment_method": {"_class": "CashPayment"},
                        }
                    ]
                },
            },
            "customer": {"_parameters": {"type": "anonymous"}},
        }
        self.api.create_sale(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/sales.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_issue_invoice_sale(self) -> None:
        self.api.issue_invoice_sale(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/sales/1/issue_invoice.json")
        self.assertEqual(kwargs["data_j"], dict(metadata=None))

    def test_list_sales(self) -> None:
        self.api.list_sales(object={"find_d": ["description:test"], "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/sales.json")
        self.assertEqual(kwargs["start_record"], 0)
        self.assertEqual(kwargs["number_records"], 5)
        self.assertEqual(kwargs["filters[]"], ["description:test:"])

    def test_stats_sales(self) -> None:
        self.api.stats_sales(store_id="21,29", has_global=True)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/sale_snapshots/stats.json")
        self.assertEqual(kwargs["store_id"], "21,29")
        self.assertEqual(kwargs["has_global"], True)


class SaleLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_checkout(self) -> None:
        merchandise = self.api.list_store_merchandise(number_records=30)
        sellable = [
            item
            for item in merchandise
            if (item.get("stock_on_hand") or 0) > 0 and item.get("retail_price")
        ]
        item = sellable[0]
        retail_price = item["retail_price"] or 0.0
        self.assertNotEqual(retail_price, 0.0)

        payload: SalePayload = {
            "transaction": {
                "sale_lines": [
                    {"merchandise": {"object_id": item["object_id"]}, "quantity": 1}
                ],
                "primary_payment": {
                    "payment_lines": [
                        {
                            "amount": {"value": retail_price},
                            "payment_method": {"_class": "CashPayment"},
                        }
                    ]
                },
            },
            "customer": {"_parameters": {"type": "anonymous"}},
        }
        sale = self.api.create_sale(payload)
        self.assertEqual(sale["payment_state"], PaymentState.PAID)
        self.assertNotEqual(sale["object_id"], None)

        invoice = self.api.issue_invoice_sale(sale["object_id"])
        self.assertEqual(invoice["signed"], Flag.YES)
        self.assertEqual(invoice["operation_code"], sale["extended_identifier"])

        receipt = self.api.ensure_receipt_sale(sale["object_id"])
        self.assertNotEqual(receipt["extended_identifier"], None)

        vat = self.api.vat_sale(sale["object_id"])
        self.assertNotEqual(vat["vat_list"], None)

        stats = self.api.stats_sales(has_global=True)
        self.assertEqual("-1" in stats, True)
        for _store_id, store_stats in stats.items():
            self.assertEqual("totals" in store_stats, True)
