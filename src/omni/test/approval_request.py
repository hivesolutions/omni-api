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

from typing import TYPE_CHECKING
from unittest import TestCase
from unittest.mock import MagicMock

from .base import build_mock

if TYPE_CHECKING:
    from omni.approval_request import ApprovalRequestReasonPayload


class ApprovalRequestTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_approval_requests(self) -> None:
        result = self.api.list_approval_requests(
            filters=["supplier:equals:7"], start_record=10, number_records=5
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/approval_requests.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs,
            dict(filters=["supplier:equals:7"], start_record=10, number_records=5),
        )

    def test_get_approval_request(self) -> None:
        result = self.api.get_approval_request(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/approval_requests/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_approve_approval_request(self) -> None:
        result = self.api.approve_approval_request(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/approval_requests/1/approve.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_reject_approval_request(self) -> None:
        payload: ApprovalRequestReasonPayload = {"reason": "Incorrect reference"}
        result = self.api.reject_approval_request(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/approval_requests/1/reject.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs["data_j"], payload)

    def test_withdraw_approval_request(self) -> None:
        result = self.api.withdraw_approval_request(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/approval_requests/1/withdraw.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_error(self) -> None:
        error = RuntimeError("Permission denied")
        self.api.get = MagicMock(side_effect=error)
        with self.assertRaises(RuntimeError) as context:
            self.api.get_approval_request(1)
        self.assertEqual(context.exception, error)
