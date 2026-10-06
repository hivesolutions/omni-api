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


import os
import re
from os import environ
from unittest import TestCase
from uuid import uuid4
from typing import TYPE_CHECKING

from omni import API, Status, brand

from .base import build_mock

if TYPE_CHECKING:
    from omni.brand import BrandPayload


class BrandTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_brands(self) -> None:
        result = self.api.list_brands(object={"find_s": "Seiko", "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/brands.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=0, number_records=5, filter_string="Seiko")
        )

    def test_create_brand(self) -> None:
        payload: BrandPayload = {"brand": {"name": "Seiko", "description": "Watches"}}
        result = self.api.create_brand(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/brands.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_brand(self) -> None:
        result = self.api.get_brand(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/brands/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_brand(self) -> None:
        payload: BrandPayload = {"brand": {"name": "Seiko Watches"}}
        result = self.api.update_brand(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/brands/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = os.path.splitext(brand.__file__)[0] + ".pyi"
        with open(path) as file:
            names = re.findall(r"^class (\w+)\(\w+\):", file.read(), re.M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(brand).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(names, ["Brand", "BrandDelta", "BrandPayload"])
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(brand, name)(), {})


class BrandLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        name = "omni_api_test_brand_%s" % uuid4().hex[:8]
        payload: BrandPayload = {"brand": {"name": name, "description": "Watches"}}
        created = self.api.create_brand(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "Brand")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["description"], "Watches")
        self.assertEqual(created["representation"], name)
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_brand(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)
        self.assertEqual(full["description_long"], "Watches")
        self.assertEqual(full["metadata"], None)

        brands = self.api.list_brands(object={"find_s": name})
        self.assertEqual([value["object_id"] for value in brands], [full["object_id"]])

        update: BrandPayload = {"brand": {"description": "Straps"}}
        updated = self.api.update_brand(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        self.assertEqual(updated["description"], "Straps")
