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
from time import time
from unittest import TestCase
from uuid import uuid4
from typing import TYPE_CHECKING

from omni import API, ConsignmentState, Status

from .base import build_mock

if TYPE_CHECKING:
    from omni.consignment import ConsignmentPayload


class ConsignmentTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_consignments(self) -> None:
        self.api.list_consignments(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/consignments.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_create_consignment(self) -> None:
        payload: ConsignmentPayload = {
            "consignment": {
                "start_date": 1784236800,
                "supplier": {"object_id": 1},
                "delivery_site": {"object_id": 2},
                "consignment_lines": [
                    {
                        "merchandise": {"object_id": 3},
                        "consigned_quantity": 2,
                        "vat_rate": 23.0,
                        "unit_discount": 0.0,
                        "unit_price": {"value": 10.0},
                    }
                ],
            },
            "document": {"_class": "ConsignmentSlip", "identifier": "CS-0001"},
        }
        self.api.create_consignment(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/consignments.json")
        self.assertEqual(kwargs["data_j"], payload)


class ConsignmentLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_create_consignment(self) -> None:
        purchases = self.api.list_purchases(number_records=5)
        suppliers = [
            supplier for purchase in purchases if (supplier := purchase.get("supplier"))
        ]
        if not suppliers:
            self.skipTest("no supplier available")
        supplier = suppliers[0]
        store = self.api.list_stores(number_records=1)[0]
        merchandise = self.api.list_store_merchandise(number_records=30)
        stocked = [
            item
            for item in merchandise
            if (item.get("stock_on_hand") or 0) > 0 and item.get("retail_price")
        ]
        if not stocked:
            self.skipTest("no stocked merchandise available")
        item = stocked[0]
        item_price = item["price"] or 0.0
        vat_rate = item["vat_rate"] or 0.0
        start_date = int(time())
        identifier = "CS-%s" % uuid4().hex[:8].upper()

        payload: ConsignmentPayload = {
            "consignment": {
                "start_date": start_date,
                "supplier": {"object_id": supplier["object_id"]},
                "delivery_site": {"object_id": store["object_id"]},
                "consignment_lines": [
                    {
                        "merchandise": {"object_id": item["object_id"]},
                        "consigned_quantity": 2,
                        "vat_rate": vat_rate,
                        "unit_discount": 0.0,
                        "unit_price": {"value": item_price},
                    }
                ],
            },
            "document": {"_class": "ConsignmentSlip", "identifier": identifier},
        }
        consignment = self.api.create_consignment(payload)
        self.assertEqual(consignment["workflow_state"], ConsignmentState.OPEN)
        self.assertEqual(consignment["start_date"], start_date)
        self.assertEqual(consignment["status"], Status.ENABLED)
        self.assertEqual(consignment["discount"], 0.0)
        self.assertNotEqual(consignment["extended_identifier"], None)

        full = self.api.get_consignment(consignment["object_id"])
        supplier_full = full.get("supplier")
        self.assertNotEqual(supplier_full, None)
        if supplier_full:
            self.assertEqual(supplier_full["object_id"], supplier["object_id"])
        delivery_site = full.get("delivery_site")
        self.assertNotEqual(delivery_site, None)
        if delivery_site:
            self.assertEqual(delivery_site["object_id"], store["object_id"])
        lines = full.get("consignment_lines") or []
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["merchandise"]["object_id"], item["object_id"])
        self.assertEqual(lines[0]["consigned_quantity"], 2.0)
        self.assertEqual(lines[0]["vat_rate"], vat_rate)
        self.assertAlmostEqual(lines[0]["unit_price"]["value"], item_price, places=2)
        self.assertAlmostEqual(
            full["vat"], 2 * item_price * vat_rate / 100.0, delta=0.05
        )
