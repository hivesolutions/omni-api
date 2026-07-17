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

from omni import API, OperationType, Physical, Status, TransferState

from .base import build_mock

if TYPE_CHECKING:
    from omni.transfer import TransferPayload


class TransferTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_transfers(self) -> None:
        self.api.list_transfers(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/transfers.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_create_transfer(self) -> None:
        payload: TransferPayload = {
            "transfer": {
                "origin": {"object_id": 1},
                "destination": {"object_id": 2},
                "transfer_lines": [{"merchandise": {"object_id": 3}, "quantity": 1}],
            }
        }
        self.api.create_transfer(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/transfers.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_get_transfer(self) -> None:
        self.api.get_transfer(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/transfers/1.json")


class TransferLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_create(self) -> None:
        stores = self.api.list_stores(number_records=10)
        physical = [store for store in stores if store["physical"] == Physical.PHYSICAL]
        if len(physical) < 2:
            self.skipTest("not enough physical stores available")
        merchandise = self.api.list_store_merchandise(number_records=30)
        stocked = [
            item
            for item in merchandise
            if (item.get("stock_on_hand") or 0) > 0 and item.get("retail_price")
        ]
        if not stocked:
            self.skipTest("no stocked merchandise available")
        item = stocked[0]

        payload: TransferPayload = {
            "transfer": {
                "origin": {"object_id": physical[0]["object_id"]},
                "destination": {"object_id": physical[1]["object_id"]},
                "transfer_lines": [
                    {"merchandise": {"object_id": item["object_id"]}, "quantity": 1}
                ],
            }
        }
        transfer = self.api.create_transfer(payload)
        self.assertEqual(transfer["workflow_state"], TransferState.CREATED)
        self.assertEqual(transfer["type"], OperationType.INTERNAL)
        self.assertEqual(transfer["status"], Status.ENABLED)
        self.assertEqual(transfer["vat"] >= 0.0, True)
        self.assertNotEqual(transfer["extended_identifier"], None)

        full = self.api.get_transfer(transfer["object_id"])
        self.assertEqual(full["destination"]["object_id"], physical[1]["object_id"])
        lines = full.get("transfer_lines") or []
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["merchandise"]["object_id"], item["object_id"])
        self.assertEqual(lines[0]["quantity"], 1.0)
        self.assertAlmostEqual(
            lines[0]["unit_price"]["value"], item["price"] or 0.0, places=2
        )
