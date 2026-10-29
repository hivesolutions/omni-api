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

from omni import API, AclValue, OmniError, Status
from omni import role

from .base import build_mock

if TYPE_CHECKING:
    from omni.role import RolePayload


class RoleTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_roles(self) -> None:
        result = self.api.list_roles(object={"find_s": "Stock", "limit": 5})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/roles.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=0, number_records=5, filter_string="Stock")
        )

    def test_create_role(self) -> None:
        payload: RolePayload = {
            "role": {"name": "Stock Viewer", "description": "Stock consultation"}
        }
        result = self.api.create_role(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/roles.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_role(self) -> None:
        result = self.api.get_role(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/roles/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_role(self) -> None:
        payload: RolePayload = {"role": {"name": "Stock Auditor"}}
        result = self.api.update_role(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(url, "http://localhost:8080/omni/roles/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_list_acl_entries_role(self) -> None:
        result = self.api.list_acl_entries_role(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/roles/1/acl_entries.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_add_acl_entry_role(self) -> None:
        result = self.api.add_acl_entry_role(1, "transfer.list")

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/roles/1/acl_entries/add.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=dict(name="transfer.list")))

        self.api.add_acl_entry_role(1, "product.cost", value=AclValue.DENY)

        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/roles/1/acl_entries/add.json")
        self.assertEqual(kwargs, dict(data_j=dict(name="product.cost", value=30)))

    def test_remove_acl_entry_role(self) -> None:
        result = self.api.remove_acl_entry_role(1, "transfer.list")

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/roles/1/acl_entries/remove.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=dict(name="transfer.list")))

        self.api.remove_acl_entry_role(1, "transfer.create", value=AclValue.VALIDATE)

        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/roles/1/acl_entries/remove.json"
        )
        self.assertEqual(kwargs, dict(data_j=dict(name="transfer.create", value=20)))

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = splitext(role.__file__)[0] + ".pyi"
        with open(path) as file:
            names = findall(r"^class (\w+)\(\w+\):", file.read(), M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(role).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 4)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(role, name)(), {})


class RoleLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        name = "omni_api_test_role_%s" % uuid4().hex[:8]
        payload: RolePayload = {"role": {"name": name, "description": "Stock"}}
        created = self.api.create_role(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "Role")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["description"], "Stock")
        self.assertEqual(created["representation"], name)
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_role(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["name"], name)
        self.assertEqual(full["description_long"], "Stock")
        self.assertEqual(full["acl_entries"], [])

        roles = self.api.list_roles(object={"find_s": name})
        self.assertEqual([value["object_id"] for value in roles], [full["object_id"]])

        update: RolePayload = {"role": {"description": "Transfers"}}
        updated = self.api.update_role(created["object_id"], update)
        self.assertEqual(updated["name"], name)
        self.assertEqual(updated["description"], "Transfers")

        with self.assertRaises(OmniError) as context:
            self.api.create_role(payload)
        self.assertEqual(context.exception.name(), "ModelValidationError")
        roles = self.api.list_roles(object={"find_s": name})
        self.assertEqual([value["object_id"] for value in roles], [full["object_id"]])

    def test_acl_entries(self) -> None:
        name = "omni_api_test_role_%s" % uuid4().hex[:8]
        payload: RolePayload = {"role": {"name": name}}
        created = self.api.create_role(payload)
        object_id = created["object_id"]
        self.assertEqual(self.api.list_acl_entries_role(object_id), {})

        entries = self.api.add_acl_entry_role(object_id, "transfer.list")
        self.assertEqual(entries, {"transfer.list": AclValue.ALLOW})

        entries = self.api.add_acl_entry_role(
            object_id, "product.cost", value=AclValue.DENY
        )
        self.assertEqual(
            entries, {"transfer.list": AclValue.ALLOW, "product.cost": AclValue.DENY}
        )
        self.assertEqual(self.api.list_acl_entries_role(object_id), entries)

        full = self.api.get_role(object_id)
        self.assertEqual(
            sorted((value["name"], value["value"]) for value in full["acl_entries"]),
            [("product.cost", AclValue.DENY), ("transfer.list", AclValue.ALLOW)],
        )

        entries = self.api.remove_acl_entry_role(
            object_id, "product.cost", value=AclValue.ALLOW
        )
        self.assertEqual(
            entries, {"transfer.list": AclValue.ALLOW, "product.cost": AclValue.DENY}
        )

        entries = self.api.remove_acl_entry_role(object_id, "product.cost")
        self.assertEqual(entries, {"transfer.list": AclValue.ALLOW})
        self.assertEqual(self.api.list_acl_entries_role(object_id), entries)
