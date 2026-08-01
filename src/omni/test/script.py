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

from omni import API, Flag, Status, TaskState

from .base import build_mock

if TYPE_CHECKING:
    from omni.script import ScriptPayload


class ScriptTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_scripts(self) -> None:
        self.api.list_scripts(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/scripts.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_create_script(self) -> None:
        payload: ScriptPayload = {
            "script": {
                "identifier": "hello_script",
                "code": "print(1)",
                "is_transaction": Flag.NO,
            }
        }
        self.api.create_script(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/scripts.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_get_script(self) -> None:
        self.api.get_script(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/scripts/1.json")

    def test_update_script(self) -> None:
        payload: ScriptPayload = {"script": {"code": "print(2)"}}
        self.api.update_script(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/scripts/1/update.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_delete_script(self) -> None:
        self.api.delete_script(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/scripts/1/delete.json")

    def test_execute_script(self) -> None:
        self.api.execute_script(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/scripts/1/execute.json")


class ScriptLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        payload: ScriptPayload = {
            "script": {
                "identifier": "omni_api_test_script",
                "code": "value = 1",
                "is_transaction": Flag.NO,
            }
        }
        script = self.api.create_script(payload)
        self.assertNotEqual(script["object_id"], None)
        self.assertEqual(script["identifier"], "omni_api_test_script")
        self.assertEqual(script["code"], "value = 1")
        self.assertEqual(script["is_transaction"], Flag.NO)

        full = self.api.get_script(script["object_id"])
        self.assertEqual(full["object_id"], script["object_id"])
        self.assertEqual(full["identifier"], "omni_api_test_script")
        self.assertEqual(full["status"], Status.ENABLED)

        update: ScriptPayload = {"script": {"code": "value = 2"}}
        updated = self.api.update_script(script["object_id"], update)
        self.assertEqual(updated["code"], "value = 2")

        self.api.delete_script(script["object_id"])

    def test_execute(self) -> None:
        payload: ScriptPayload = {
            "script": {
                "identifier": "omni_api_execute_script",
                "code": "value = 1",
                "is_transaction": Flag.NO,
            }
        }
        script = self.api.create_script(payload)

        script_task = self.api.execute_script(script["object_id"])
        self.assertNotEqual(script_task["object_id"], None)
        self.assertEqual(script_task["script_id"], script["object_id"])
        self.assertEqual(script_task["task_state"], TaskState.SCHEDULED)

        self.api.delete_script(script["object_id"])
