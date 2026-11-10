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
from omni import family

from .base import build_mock

if TYPE_CHECKING:
    from omni.family import FamilyPayload


class FamilyTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_families(self) -> None:
        result = self.api.list_families(object={"find_s": "Jewellery", "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/families.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=0, number_records=5, filter_string="Jewellery")
        )

    def test_create_family(self) -> None:
        payload: FamilyPayload = {
            "family": {"name": "Jewellery", "description": "Rings and chains"}
        }
        result = self.api.create_family(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/families.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_family(self) -> None:
        result = self.api.get_family(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/families/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_family(self) -> None:
        payload: FamilyPayload = {"family": {"name": "Fine Jewellery"}}
        result = self.api.update_family(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/families/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_delete_family(self) -> None:
        self.api.delete_family(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/families/1/delete.json")
        self.assertEqual("data_j" in kwargs, False)

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = splitext(family.__file__)[0] + ".pyi"
        with open(path) as file:
            names = findall(r"^class (\w+)\(\w+\):", file.read(), M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(family).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 3)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(family, name)(), {})


class FamilyLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        name = "omni_api_test_family_%s" % uuid4().hex[:8]
        payload: FamilyPayload = {
            "family": {"name": name, "description": "Rings and chains"}
        }
        created = self.api.create_family(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "Family")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["description"], "Rings and chains")
        self.assertEqual(created["representation"], name)
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_family(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)

        families = self.api.list_families(object={"find_s": name})
        self.assertEqual(
            [value["object_id"] for value in families], [full["object_id"]]
        )

        update: FamilyPayload = {"family": {"description": "Watches"}}
        updated = self.api.update_family(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        self.assertEqual(updated["description"], "Watches")

        with self.assertRaises(OmniError) as context:
            self.api.create_family(payload)
        self.assertEqual(context.exception.name(), "ModelValidationError")
        families = self.api.list_families(object={"find_s": name})
        self.assertEqual(
            [value["object_id"] for value in families], [full["object_id"]]
        )

        self.api.delete_family(created["object_id"])
        families = self.api.list_families(object={"find_s": name})
        self.assertEqual(families, [])
        with self.assertRaises(OmniError) as context:
            self.api.delete_family(created["object_id"])
        self.assertEqual(context.exception.name(), "InvalidOperation")
