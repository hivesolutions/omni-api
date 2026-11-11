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
from omni import sub_class

from .base import build_mock

if TYPE_CHECKING:
    from omni.class_ import ClassPayload
    from omni.family import FamilyPayload
    from omni.sub_class import SubClassPayload


class SubClassTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_sub_classes(self) -> None:
        result = self.api.list_sub_classes(
            object={"find_s": "Wedding Ring", "limit": 5}
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/sub_classes.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs,
            dict(start_record=0, number_records=5, filter_string="Wedding Ring"),
        )

    def test_create_sub_class(self) -> None:
        payload: SubClassPayload = {
            "sub_class": {"name": "Wedding Ring", "class_": {"object_id": 1}}
        }
        result = self.api.create_sub_class(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/sub_classes.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_sub_class(self) -> None:
        result = self.api.get_sub_class(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/sub_classes/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_sub_class(self) -> None:
        payload: SubClassPayload = {"sub_class": {"class_": {"object_id": 2}}}
        result = self.api.update_sub_class(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/sub_classes/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_delete_sub_class(self) -> None:
        self.api.delete_sub_class(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/sub_classes/1/delete.json")
        self.assertEqual("data_j" in kwargs, False)

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = splitext(sub_class.__file__)[0] + ".pyi"
        with open(path) as file:
            names = findall(r"^class (\w+)\(\w+\):", file.read(), M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(sub_class).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 3)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(sub_class, name)(), {})


class SubClassLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        suffix = uuid4().hex[:8]
        family: FamilyPayload = {"family": {"name": "omni_api_test_family_%s" % suffix}}
        family_created = self.api.create_family(family)
        class_e: ClassPayload = {
            "class": {
                "name": "omni_api_test_class_%s" % suffix,
                "family": {"object_id": family_created["object_id"]},
            }
        }
        class_created = self.api.create_class(class_e)
        other_class: ClassPayload = {
            "class": {
                "name": "omni_api_test_other_class_%s" % suffix,
                "family": {"object_id": family_created["object_id"]},
            }
        }
        other_class_created = self.api.create_class(other_class)

        name = "omni_api_test_sub_class_%s" % suffix
        payload: SubClassPayload = {
            "sub_class": {
                "name": name,
                "description": "Wedding and engagement rings",
                "class_": {"object_id": class_created["object_id"]},
            }
        }
        created = self.api.create_sub_class(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "SubClass")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["description"], "Wedding and engagement rings")
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_sub_class(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)
        self.assertEqual(
            (full.get("class_") or {}).get("object_id"), class_created["object_id"]
        )

        sub_classes = self.api.list_sub_classes(object={"find_s": name})
        self.assertEqual(
            [value["object_id"] for value in sub_classes], [full["object_id"]]
        )

        update: SubClassPayload = {
            "sub_class": {"class_": {"object_id": other_class_created["object_id"]}}
        }
        updated = self.api.update_sub_class(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        full = self.api.get_sub_class(created["object_id"])
        self.assertEqual(
            (full.get("class_") or {}).get("object_id"),
            other_class_created["object_id"],
        )

        with self.assertRaises(OmniError) as context:
            self.api.create_sub_class(payload)
        self.assertEqual(context.exception.name(), "ModelValidationError")

        self.api.delete_sub_class(created["object_id"])
        sub_classes = self.api.list_sub_classes(object={"find_s": name})
        self.assertEqual(sub_classes, [])
        with self.assertRaises(OmniError) as context:
            self.api.delete_sub_class(created["object_id"])
        self.assertEqual(context.exception.name(), "InvalidOperation")

        self.api.delete_class(other_class_created["object_id"])
        self.api.delete_class(class_created["object_id"])
        self.api.delete_family(family_created["object_id"])
