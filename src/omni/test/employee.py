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

from omni import API, Status

from .base import build_mock

if TYPE_CHECKING:
    from omni.employee import EmployeePayload


class EmployeeTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_employees(self) -> None:
        self.api.list_employees(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/employees.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_update_employee(self) -> None:
        payload: EmployeePayload = {"employee": {"observations": "test"}}
        self.api.update_employee(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/employees/1/update.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_self_employee(self) -> None:
        self.api.self_employee()

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/employees/self.json")

    def test_stats_employee(self) -> None:
        self.api.stats_employee(unit="month", span=3, has_global=True)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(
            url, "http://localhost:8080/omni/employee_snapshots/stats.json"
        )
        self.assertEqual(kwargs["unit"], "month")
        self.assertEqual(kwargs["span"], 3)
        self.assertEqual(kwargs["has_global"], True)


class EmployeeLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_self(self) -> None:
        employee = self.api.self_employee()
        self.assertNotEqual(employee["object_id"], None)
        self.assertNotEqual(employee["name"], None)

        full = self.api.get_employee(employee["object_id"])
        self.assertEqual(full["object_id"], employee["object_id"])
        self.assertEqual(full["name"], employee["name"])
        self.assertEqual(full["surname"], employee["surname"])
        self.assertEqual(full["status"], Status.ENABLED)

    def test_update(self) -> None:
        employee = self.api.list_employees(number_records=1)[0]
        previous = employee["observations"]

        payload: EmployeePayload = {
            "employee": {"name": employee["name"], "observations": "updated"}
        }
        updated = self.api.update_employee(employee["object_id"], payload)
        self.assertEqual(updated["observations"], "updated")
        self.assertEqual(updated["name"], employee["name"])

        full = self.api.get_employee(employee["object_id"])
        self.assertEqual(full["observations"], "updated")

        restore: EmployeePayload = {
            "employee": {"name": employee["name"], "observations": previous}
        }
        restored = self.api.update_employee(employee["object_id"], restore)
        self.assertEqual(restored["observations"], previous)

        full = self.api.get_employee(employee["object_id"])
        self.assertEqual(full["observations"], previous)
