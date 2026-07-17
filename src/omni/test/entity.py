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
from os import environ
from unittest import TestCase

from omni import API, MediaVisibility

from .base import build_mock


PNG_DATA = b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    b"AAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)
""" The contents of a minimal (one pixel) PNG image to be
used in the media related test cases """


class EntityTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_sequence_entity(self) -> None:
        self.api.sequence_entity(1)

        method, url, _kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/entities/1/sequence.json")

    def test_update_entity(self) -> None:
        self.api.update_entity(1, {"root_entity": {"description": "test"}})

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/entities/1/update.json")
        self.assertEqual(kwargs["data_j"], {"root_entity": {"description": "test"}})

    def test_set_media_entity(self) -> None:
        self.api.set_media_entity(1, PNG_DATA, position=1, mime_type="image/png")

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/entities/1/media/set.json")
        data_j = kwargs["data_j"]
        self.assertEqual(data_j["position"], 1)
        self.assertEqual(data_j["mime_type"], "image/png")
        self.assertEqual(b64decode(data_j["data_b64"]), PNG_DATA)


class EntityLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_sequence(self) -> None:
        entities = self.api.list_entities(number_records=1)
        if not entities:
            self.skipTest("no entities available")
        sequence = self.api.sequence_entity(entities[0]["object_id"])
        self.assertEqual("next" in sequence, True)
        self.assertEqual("previous" in sequence, True)

    def test_media(self) -> None:
        entities = self.api.list_entities(number_records=1)
        if not entities:
            self.skipTest("no entities available")
        object_id = entities[0]["object_id"]

        media = self.api.set_media_entity(
            object_id, PNG_DATA, position=1, label="logo", mime_type="image/png"
        )
        self.assertEqual(media["mime_type"], "image/png")
        self.assertEqual(media["visibility"], MediaVisibility.CONSTRAINED)

        info = self.api.info_media_entity(object_id)
        self.assertNotEqual(len(info), 0)

        contents = self.api.media_entity(object_id)
        self.assertEqual(contents, PNG_DATA)

        result = self.api.clear_media_entity(object_id)
        self.assertEqual(result["result"], "success")
