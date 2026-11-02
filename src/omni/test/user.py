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
from uuid import uuid4

from omni import API, AclValue, Status, UserType

from .base import build_mock

if TYPE_CHECKING:
    from omni.role import RolePayload
    from omni.user import UserPayload


class UserTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_users(self) -> None:
        self.api.list_users(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_create_user(self) -> None:
        payload: UserPayload = {
            "system_user": {
                "username": "username",
                "email": "username@acmecorp.com",
                "_parameters": {
                    "password": "password",
                    "confirm_password": "password",
                    "type": UserType.USER,
                    "employee": {"object_id": 1},
                },
            }
        }
        self.api.create_user(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/users.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_get_user(self) -> None:
        self.api.get_user(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users/1.json")

    def test_self_user(self) -> None:
        self.api.self_user()

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users/self.json")

    def test_get_acl_user(self) -> None:
        self.api.get_acl_user(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/acl.json")
        self.assertEqual(kwargs, {})

    def test_list_acl_entries_user(self) -> None:
        self.api.list_acl_entries_user(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/acl_entries.json")
        self.assertEqual(kwargs, {})

    def test_add_acl_entry_user(self) -> None:
        self.api.add_acl_entry_user(1, "transfer.list")

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/acl_entries/add.json")
        self.assertEqual(kwargs["data_j"], dict(name="transfer.list"))

        self.api.add_acl_entry_user(1, "sale_transaction.delete", value=AclValue.DENY)

        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/acl_entries/add.json")
        self.assertEqual(
            kwargs["data_j"], dict(name="sale_transaction.delete", value=30)
        )

    def test_remove_acl_entry_user(self) -> None:
        self.api.remove_acl_entry_user(1, "transfer.list")

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/users/1/acl_entries/remove.json"
        )
        self.assertEqual(kwargs["data_j"], dict(name="transfer.list"))

        self.api.remove_acl_entry_user(1, "transfer.create", value=AclValue.VALIDATE)

        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/users/1/acl_entries/remove.json"
        )
        self.assertEqual(kwargs["data_j"], dict(name="transfer.create", value=20))

    def test_list_roles_user(self) -> None:
        self.api.list_roles_user(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/roles.json")
        self.assertEqual(kwargs, {})

    def test_add_role_user(self) -> None:
        self.api.add_role_user(1, 2)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/roles/add.json")
        self.assertEqual(kwargs["data_j"], dict(role_id=2))

    def test_remove_role_user(self) -> None:
        self.api.remove_role_user(1, 2)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/users/1/roles/remove.json")
        self.assertEqual(kwargs["data_j"], dict(role_id=2))

    def test_acl_value(self) -> None:
        self.assertEqual(AclValue.ALLOW, 10)
        self.assertEqual(AclValue.VALIDATE, 20)
        self.assertEqual(AclValue.DENY, 30)


class UserLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_create_user(self) -> None:
        employees = self.api.list_employees(number_records=1)
        if not employees:
            self.skipTest("no employees available")
        username = "typed_%s" % uuid4().hex[:8]
        email = "%s@acmecorp.com" % username
        password = "Typed@12345"

        payload: UserPayload = {
            "system_user": {
                "username": username,
                "email": email,
                "_parameters": {
                    "password": password,
                    "confirm_password": password,
                    "type": UserType.USER,
                    "employee": {"object_id": employees[0]["object_id"]},
                },
            }
        }
        user = self.api.create_user(payload)
        self.assertEqual(user["username"], username)
        self.assertEqual(user["email"], email)
        self.assertEqual(user["type"], UserType.USER)
        self.assertEqual(user["status"], Status.ENABLED)
        self.assertNotEqual(user["object_id"], None)
        self.assertNotEqual(user["password_hash"], None)
        self.assertNotEqual(user["password_hash"], password)

        created = API(username=username, password=password)
        logged = created.self_user()
        self.assertEqual(logged["username"], username)
        self.assertEqual(logged["email"], email)
        self.assertEqual(logged["object_id"], user["object_id"])
        self.assertEqual(logged["type"], UserType.USER)

        employee = created.self_employee()
        self.assertEqual(employee["object_id"], employees[0]["object_id"])

    def test_acl_entries_roles(self) -> None:
        employees = self.api.list_employees(number_records=1)
        if not employees:
            self.skipTest("no employees available")
        username = "typed_%s" % uuid4().hex[:8]
        password = "Typed@12345"

        payload: UserPayload = {
            "system_user": {
                "username": username,
                "email": "%s@acmecorp.com" % username,
                "_parameters": {
                    "password": password,
                    "confirm_password": password,
                    "type": UserType.USER,
                    "employee": {"object_id": employees[0]["object_id"]},
                },
            }
        }
        user = self.api.create_user(payload)
        object_id = user["object_id"]
        self.assertEqual(self.api.list_acl_entries_user(object_id), {})
        self.assertEqual(self.api.list_roles_user(object_id), [])

        entries = self.api.add_acl_entry_user(object_id, "transfer.list")
        self.assertEqual(entries, {"transfer.list": AclValue.ALLOW})

        entries = self.api.add_acl_entry_user(
            object_id, "sale_transaction.delete", value=AclValue.DENY
        )
        self.assertEqual(
            entries,
            {"transfer.list": AclValue.ALLOW, "sale_transaction.delete": AclValue.DENY},
        )
        self.assertEqual(self.api.list_acl_entries_user(object_id), entries)

        acl = self.api.get_acl_user(object_id)
        self.assertEqual(acl["transfer.list"], AclValue.ALLOW)
        self.assertEqual(acl["sale_transaction.delete"], AclValue.DENY)

        entries = self.api.remove_acl_entry_user(
            object_id, "sale_transaction.delete", value=AclValue.ALLOW
        )
        self.assertEqual(
            entries,
            {"transfer.list": AclValue.ALLOW, "sale_transaction.delete": AclValue.DENY},
        )

        entries = self.api.remove_acl_entry_user(object_id, "sale_transaction.delete")
        self.assertEqual(entries, {"transfer.list": AclValue.ALLOW})
        self.assertEqual(self.api.list_acl_entries_user(object_id), entries)

        name = "omni_api_test_role_%s" % uuid4().hex[:8]
        role_payload: RolePayload = {"role": {"name": name}}
        role = self.api.create_role(role_payload)
        self.api.add_acl_entry_role(role["object_id"], "report.sale_stats")

        roles = self.api.add_role_user(object_id, role["object_id"])
        self.assertEqual([value["object_id"] for value in roles], [role["object_id"]])
        self.assertEqual(self.api.list_roles_user(object_id), roles)

        acl = self.api.get_acl_user(object_id)
        self.assertEqual(acl["report.sale_stats"], AclValue.ALLOW)

        roles = self.api.remove_role_user(object_id, role["object_id"])
        self.assertEqual(roles, [])
        self.assertEqual(self.api.list_roles_user(object_id), [])
