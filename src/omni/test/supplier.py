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

from omni import API, Status

from .base import build_mock


class SupplierTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_suppliers(self) -> None:
        self.api.list_suppliers(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/suppliers.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_list_companies(self) -> None:
        self.api.list_companies(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_companies.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_get_company(self) -> None:
        self.api.get_company(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/supplier_companies/1.json")


class SupplierLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_companies(self) -> None:
        companies = self.api.list_companies(number_records=5)
        self.assertNotEqual(len(companies), 0)
        for company in companies:
            self.assertNotEqual(company["object_id"], None)
            self.assertNotEqual(company["name"], "")
            self.assertEqual(company["status"], Status.ENABLED)

        company = companies[0]
        full = self.api.get_company(company["object_id"])
        self.assertEqual(full["object_id"], company["object_id"])
        self.assertEqual(full["name"], company["name"])
        self.assertEqual(full["tax_number"], company["tax_number"])
