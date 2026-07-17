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

from omni import API

from .base import build_mock


class StatusTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_get_status(self) -> None:
        self.api.get_status()

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/status.json")


class StatusLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_status(self) -> None:
        status = self.api.get_status()
        self.assertNotEqual(status["hostname"], "")
        self.assertEqual("." in status["system"]["version"], True)
        self.assertNotEqual(status["system"]["run_mode"], "")
        self.assertEqual(status["database"]["engine"] in ("sqlite", "mysql"), True)
        self.assertEqual(status["database"]["database_size"] > 0, True)
        self.assertNotEqual(status["database"]["database_size_string"], "")
        self.assertEqual("." in status["info"]["version"], True)
        self.assertNotEqual(len(status["libraries"]), 0)
        for library in status["libraries"]:
            self.assertNotEqual(library["name"], "")
