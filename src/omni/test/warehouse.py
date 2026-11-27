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
from os.path import splitext
from re import M, findall
from unittest import TestCase
from uuid import uuid4
from typing import TYPE_CHECKING

from omni import API, OmniError, Status
from omni import warehouse

from .base import build_mock

if TYPE_CHECKING:
    from omni.warehouse import WarehousePayload


class WarehouseTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_warehouses(self) -> None:
        result = self.api.list_warehouses(object={"find_s": "North", "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/warehouses.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=0, number_records=5, filter_string="North")
        )

    def test_create_warehouse(self) -> None:
        payload: WarehousePayload = {
            "warehouse": {
                "name": "Warehouse - North",
                "warehouse_code": "WNR001",
                "identifier_prefix": "WNR",
                "identifier_number_digits": 6,
            }
        }
        result = self.api.create_warehouse(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/warehouses.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_warehouse(self) -> None:
        result = self.api.get_warehouse(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/warehouses/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict())

    def test_update_warehouse(self) -> None:
        payload: WarehousePayload = {"warehouse": {"warehouse_code": "WNR002"}}
        result = self.api.update_warehouse(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/warehouses/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_delete_warehouse(self) -> None:
        self.api.delete_warehouse(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/warehouses/1/delete.json")
        self.assertEqual("data_j" in kwargs, False)

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = splitext(warehouse.__file__)[0] + ".pyi"
        with open(path) as file:
            names = findall(r"^class (\w+)\(\w+\):", file.read(), M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(warehouse).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 3)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(warehouse, name)(), {})


class WarehouseLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        suffix = uuid4().hex[:6].upper()
        name = "omni_api_test_warehouse_%s" % suffix
        prefix = "W%s" % suffix
        payload: WarehousePayload = {
            "warehouse": {
                "name": name,
                "warehouse_code": "WH%s" % suffix,
                "identifier_prefix": prefix,
                "identifier_number_digits": 2,
            }
        }
        created = self.api.create_warehouse(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "Warehouse")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["warehouse_code"], "WH%s" % suffix)
        self.assertEqual(created["identifier_template"], "%s%%02d" % prefix)
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_warehouse(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)

        warehouses = self.api.list_warehouses(object={"find_s": name})
        self.assertEqual(
            [value["object_id"] for value in warehouses], [full["object_id"]]
        )
        stores = self.api.list_stores(object={"find_s": name})
        self.assertEqual(stores, [])

        update: WarehousePayload = {"warehouse": {"warehouse_code": "WH2%s" % suffix}}
        updated = self.api.update_warehouse(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        self.assertEqual(updated["warehouse_code"], "WH2%s" % suffix)

        with self.assertRaises(OmniError) as context:
            self.api.create_warehouse(payload)
        self.assertEqual(context.exception.name(), "ModelValidationError")

        self.api.delete_warehouse(created["object_id"])
        warehouses = self.api.list_warehouses(object={"find_s": name})
        self.assertEqual(warehouses, [])
