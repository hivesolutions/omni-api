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
    from omni.store import StorePayload


class StoreTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_stores(self) -> None:
        self.api.list_stores(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/stores.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_get_store(self) -> None:
        self.api.get_store(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/stores/1.json")

    def test_update_store(self) -> None:
        payload: StorePayload = {"store": {"name": "Store", "observations": "test"}}
        self.api.update_store(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/stores/1/update.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_delete_store(self) -> None:
        self.api.delete_store(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/stores/1/delete.json")
        self.assertEqual("data_j" in kwargs, False)


class StoreLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_update(self) -> None:
        store = self.api.list_stores(number_records=1)[0]
        previous = store["observations"]

        payload: StorePayload = {
            "store": {"name": store["name"], "observations": "updated"}
        }
        updated = self.api.update_store(store["object_id"], payload)
        self.assertEqual(updated["observations"], "updated")
        self.assertEqual(updated["name"], store["name"])
        self.assertEqual(updated["status"], Status.ENABLED)

        full = self.api.get_store(store["object_id"])
        self.assertEqual(full["observations"], "updated")
        self.assertEqual(full["physical"], store["physical"])

        restore: StorePayload = {
            "store": {"name": store["name"], "observations": previous}
        }
        restored = self.api.update_store(store["object_id"], restore)
        self.assertEqual(restored["observations"], previous)
