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

from base64 import b64decode
from unittest import TestCase
from typing import TYPE_CHECKING

from .base import build_mock

if TYPE_CHECKING:
    from omni.media import MediaPayload


class MediaTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_media(self) -> None:
        self.api.list_media(number_records=3)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/media.json")
        self.assertEqual(kwargs["number_records"], 3)

    def test_update_media(self) -> None:
        payload: MediaPayload = {
            "data": b"contents",
            "media": {"label": "logo"},
        }
        self.api.update_media(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/media/1/update.json")
        data_j = kwargs["data_j"]
        self.assertEqual("data" in data_j, False)
        self.assertEqual(b64decode(data_j["data_b64"]), b"contents")
        self.assertEqual(data_j["media"], {"label": "logo"})

    def test_delete_media(self) -> None:
        self.api.delete_media(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/media/1/delete.json")

    def test_get_media_url(self) -> None:
        url = self.api.get_media_url("secret")
        self.assertEqual(url, "http://localhost:8080/omni/media/secret")
