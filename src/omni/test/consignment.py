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

from omni import API, ConsignmentState

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

    def test_list(self) -> None:
        consignments = self.api.list_consignments(number_records=3)
        for consignment in consignments:
            self.assertNotEqual(consignment["object_id"], None)
            self.assertEqual(
                consignment["workflow_state"]
                in (
                    ConsignmentState.OPEN,
                    ConsignmentState.CLOSED,
                    ConsignmentState.EXPIRED,
                ),
                True,
            )
