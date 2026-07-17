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

from omni import API, UserType

from .base import build_mock

if TYPE_CHECKING:
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

        payload: UserPayload = {
            "system_user": {
                "username": username,
                "email": "%s@acmecorp.com" % username,
                "_parameters": {
                    "password": "Typed@12345",
                    "confirm_password": "Typed@12345",
                    "type": UserType.USER,
                    "employee": {"object_id": employees[0]["object_id"]},
                },
            }
        }
        user = self.api.create_user(payload)
        self.assertEqual(user["username"], username)
        self.assertEqual(user["type"], UserType.USER)
        self.assertNotEqual(user["object_id"], None)

        created = API(username=username, password="Typed@12345")
        logged = created.self_user()
        self.assertEqual(logged["username"], username)
