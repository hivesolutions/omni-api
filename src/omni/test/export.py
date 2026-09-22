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
from unittest import TestCase
from unittest.mock import MagicMock, patch

from omni import export

from .base import build_api, build_mock


class ExportAPITest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_export_schema(self) -> None:
        result = self.api.export_schema()
        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/schema.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_export_changes(self) -> None:
        result = self.api.export_changes(
            after_mtime=1790000000.5, after_id=42, limit=500, lag=120.0
        )
        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/changes.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(after_mtime=1790000000.5, after_id=42, limit=500, lag=120.0)
        )

    def test_export_digests(self) -> None:
        result = self.api.export_digests(start_id=0, end_id=100000, size=1000)
        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/digests.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(start_id=0, end_id=100000, size=1000))

        result = self.api.export_digests(start_id=0, end_id=1000, pairs=True)
        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/digests.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(start_id=0, end_id=1000, pairs=True))

    def test_export_digests_response(self) -> None:
        api = build_api()
        api.session_id = "session"
        response = MagicMock()
        response.read.return_value = (
            b'{"start_id": 0, "end_id": 1000, '
            b'"pairs": [[1, 1790000000.5], [2, 1790000001.0]]}'
        )
        response.getcode.return_value = 200
        response.info.return_value = {"Content-Type": "application/json"}
        with patch("appier.http._resolve", return_value=response):
            result = api.export_digests(start_id=0, end_id=1000, pairs=True)

        if not "pairs" in result:
            self.fail("pairs expected")
        self.assertEqual(len(result["pairs"]), 2)
        pair: tuple[int, float] = result["pairs"][0]
        object_id, mtime = pair
        self.assertEqual(object_id, 1)
        self.assertEqual(mtime, 1790000000.5)
        self.assertIsInstance(object_id, int)
        self.assertIsInstance(mtime, float)

    def test_export_entities(self) -> None:
        result = self.api.export_entities("sale_transaction", ids="1,2,3")
        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/sale_transaction.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(ids="1,2,3"))

        result = self.api.export_entities("sale_transaction", after_id=10, limit=2)
        method, url, kwargs = self.api.requests[1]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/export/sale_transaction.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(after_id=10, limit=2))

    def test_export_totals(self) -> None:
        result = self.api.export_totals("sale_transaction", until_mtime=1790000000.0)
        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(
            url, "http://localhost:8080/omni/export/sale_transaction/totals.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(until_mtime=1790000000.0))

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = os.path.splitext(export.__file__)[0] + ".pyi"
        with open(path) as file:
            names = re.findall(r"^class (\w+)\(TypedDict\):", file.read(), re.M)
        markers = [
            name
            for name, value in vars(export).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 13)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(export, name)(), {})
