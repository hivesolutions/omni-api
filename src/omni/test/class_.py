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
from omni import class_

from .base import build_mock

if TYPE_CHECKING:
    from omni.class_ import ClassPayload
    from omni.family import FamilyPayload


class ClassTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_classes(self) -> None:
        result = self.api.list_classes(object={"find_s": "Rings", "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/classes.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=0, number_records=5, filter_string="Rings")
        )

    def test_create_class(self) -> None:
        payload: ClassPayload = {"class": {"name": "Rings", "family": {"object_id": 1}}}
        result = self.api.create_class(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/classes.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_class(self) -> None:
        result = self.api.get_class(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/classes/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_class(self) -> None:
        payload: ClassPayload = {"class": {"family": {"object_id": 2}}}
        result = self.api.update_class(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/classes/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_delete_class(self) -> None:
        self.api.delete_class(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/classes/1/delete.json")
        self.assertEqual("data_j" in kwargs, False)

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well, the payload being
        # declared with the functional syntax as its key (class) is a
        # reserved word
        path = splitext(class_.__file__)[0] + ".pyi"
        with open(path) as file:
            names = findall(
                r"^(?:class (\w+)\(\w+\):|(\w+) = TypedDict\()", file.read(), M
            )
        names = ["".join(name) for name in names]
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(class_).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 3)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(class_, name)(), {})


class ClassLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        suffix = uuid4().hex[:8]
        family_name = "omni_api_test_family_%s" % suffix
        family: FamilyPayload = {"family": {"name": family_name}}
        family_created = self.api.create_family(family)
        other_family: FamilyPayload = {
            "family": {"name": "omni_api_test_other_family_%s" % suffix}
        }
        other_family_created = self.api.create_family(other_family)

        name = "omni_api_test_class_%s" % suffix
        payload: ClassPayload = {
            "class": {
                "name": name,
                "description": "Rings of all styles",
                "family": {"object_id": family_created["object_id"]},
            }
        }
        created = self.api.create_class(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "Class")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["description"], "Rings of all styles")
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_class(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)
        self.assertEqual(
            (full.get("family") or {}).get("object_id"), family_created["object_id"]
        )

        classes = self.api.list_classes(object={"find_s": name})
        self.assertEqual([value["object_id"] for value in classes], [full["object_id"]])

        update: ClassPayload = {
            "class": {"family": {"object_id": other_family_created["object_id"]}}
        }
        updated = self.api.update_class(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        full = self.api.get_class(created["object_id"])
        self.assertEqual(
            (full.get("family") or {}).get("object_id"),
            other_family_created["object_id"],
        )

        with self.assertRaises(OmniError) as context:
            self.api.create_class(
                {
                    "class": {
                        "name": family_name,
                        "family": {"object_id": family_created["object_id"]},
                    }
                }
            )
        self.assertEqual(context.exception.name(), "ModelValidationError")

        self.api.delete_class(created["object_id"])
        classes = self.api.list_classes(object={"find_s": name})
        self.assertEqual(classes, [])
        with self.assertRaises(OmniError) as context:
            self.api.delete_class(created["object_id"])
        self.assertEqual(context.exception.name(), "InvalidOperation")

        self.api.delete_family(other_family_created["object_id"])
        self.api.delete_family(family_created["object_id"])
