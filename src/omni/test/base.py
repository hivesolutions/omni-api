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

from unittest import TestCase
from unittest.mock import MagicMock, patch
from typing import Any

from omni import API, OmniError


class MockAPI(API):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        API.__init__(self, *args, **kwargs)
        self.requests: list[tuple[str, str, dict[str, Any]]] = []

    def get(self, url: str, *args: Any, **kwargs: Any) -> Any:
        self.requests.append(("GET", url, kwargs))
        return dict()

    def post(self, url: str, *args: Any, **kwargs: Any) -> Any:
        self.requests.append(("POST", url, kwargs))
        return dict()

    def put(self, url: str, *args: Any, **kwargs: Any) -> Any:
        self.requests.append(("PUT", url, kwargs))
        return dict()

    def delete(self, url: str, *args: Any, **kwargs: Any) -> Any:
        self.requests.append(("DELETE", url, kwargs))
        return dict()


def build_mock() -> MockAPI:
    return MockAPI(
        base_url="http://localhost:8080/",
        username="username",
        password="password",
    )


def build_api() -> API:
    return API(
        base_url="http://localhost:8080/",
        username="username",
        password="password",
    )


class BaseTest(TestCase):

    def test_basic(self) -> None:
        self.assertEqual(1 + 1, 2)

    def test_mock(self) -> None:
        api = build_mock()
        self.assertEqual(api.base_url, "http://localhost:8080/")
        self.assertEqual(api.requests, [])

    def test_login(self) -> None:
        api = build_api()
        contents = dict(
            username="username",
            object_id=1,
            acl={"*": 10},
            session_id="session",
        )
        with patch.object(api, "get", return_value=contents) as get_mock:
            session_id = api.login()

        self.assertEqual(session_id, "session")
        self.assertEqual(api.session_id, "session")
        self.assertEqual(api.username, "username")
        self.assertEqual(api.object_id, 1)
        self.assertEqual(api.acl, {"*": 10})
        self.assertEqual(list(api.tokens or []), ["*"])
        get_mock.assert_called_once_with(
            "http://localhost:8080/omni/login.json",
            callback=False,
            auth=False,
            token=False,
            username="username",
            password="password",
        )

    def test_session_caching(self) -> None:
        api = build_api()
        contents = dict(
            username="username",
            object_id=1,
            acl={"*": 10},
            session_id="session",
        )
        with patch.object(api, "get", return_value=contents) as get_mock:
            api.get_session_id()
            api.get_session_id()

        self.assertEqual(get_mock.call_count, 1)

    def test_handle_error(self) -> None:
        api = build_api()
        error = MagicMock(code=500)
        error.read_json.return_value = dict(
            exception=dict(exception_name="ValidationError", message="invalid")
        )

        with self.assertRaises(OmniError) as context:
            api.handle_error(error)

        self.assertEqual(context.exception.name(), "ValidationError")
        self.assertEqual(context.exception.description(), "invalid")
        self.assertEqual(str(context.exception), "ValidationError - invalid")

    def test_digest_identifier_document(self) -> None:
        api = build_api()
        contents = dict(digest_identifier="FT INVMST/000001")
        with patch.object(api, "get", return_value=contents) as get_mock:
            digest_identifier = api.digest_identifier_document(1)

        self.assertEqual(digest_identifier, "FT INVMST/000001")
        get_mock.assert_called_once_with(
            "http://localhost:8080/omni/signed_documents/1/digest_identifier.json"
        )
