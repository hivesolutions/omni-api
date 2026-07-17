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

from omni import API, Flag, RepairOperationState, RepairPriority, RepairType
from omni import Status

from .base import build_mock

if TYPE_CHECKING:
    from omni.repair_operation import RepairOperationPayload
    from omni.workflow_message import WorkflowMessagePayload


class RepairOperationTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_create_repair_operation(self) -> None:
        payload: RepairOperationPayload = {
            "repair_operation": {
                "title": "Screen repair",
                "repair_type": RepairType.QUOTATION,
                "customer": {"object_id": 1},
                "item_reference": "SN-0001",
            }
        }
        self.api.create_repair_operation(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/repair_operations.json")
        self.assertEqual(kwargs["data_j"], payload)

    def test_transitions(self) -> None:
        self.api.approve_repair_operation(1)
        self.api.reject_repair_operation(1)
        self.api.quote_repair_operation(1)
        self.api.receive_repair_operation(1)
        self.api.send_repair_operation(1)
        self.api.close_repair_operation(1)

        urls = [url for method, url, _kwargs in self.api.requests]
        methods = [method for method, _url, _kwargs in self.api.requests]
        self.assertEqual(methods, ["PUT"] * 6)
        self.assertEqual(
            urls,
            [
                "http://localhost:8080/omni/repair_operations/1/approve.json",
                "http://localhost:8080/omni/repair_operations/1/reject.json",
                "http://localhost:8080/omni/repair_operations/1/quote.json",
                "http://localhost:8080/omni/repair_operations/1/receive.json",
                "http://localhost:8080/omni/repair_operations/1/send.json",
                "http://localhost:8080/omni/repair_operations/1/close.json",
            ],
        )

    def test_messages(self) -> None:
        payload: WorkflowMessagePayload = {"body": "message"}
        self.api.create_message_repair_operation(1, payload)
        self.api.update_message_repair_operation(1, 2, payload)
        self.api.delete_message_repair_operation(1, 2)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/repair_operations/1/messages.json"
        )
        self.assertEqual(kwargs["data_j"], payload)

        method, url, _kwargs = self.api.requests[1]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url,
            "http://localhost:8080/omni/repair_operations/1/messages/2/update.json",
        )

        method, url, _kwargs = self.api.requests[2]
        self.assertEqual(method, "DELETE")
        self.assertEqual(
            url, "http://localhost:8080/omni/repair_operations/1/messages/2.json"
        )


class RepairOperationLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_lifecycle(self) -> None:
        customers = self.api.list_persons(number_records=1)
        if not customers:
            self.skipTest("no customer available")

        payload: RepairOperationPayload = {
            "repair_operation": {
                "title": "Lifecycle repair",
                "repair_type": RepairType.QUOTATION,
                "priority": RepairPriority.HIGH,
                "customer": {"object_id": customers[0]["object_id"]},
                "item_reference": "SN-LIFECYCLE",
                "problem_description": "does not start",
            }
        }
        operation = self.api.create_repair_operation(payload)
        object_id = operation["object_id"]
        self.assertEqual(operation["workflow_state"], RepairOperationState.OPENED)
        self.assertEqual(operation["title"], "Lifecycle repair")
        self.assertEqual(operation["repair_type"], RepairType.QUOTATION)
        self.assertEqual(operation["priority"], RepairPriority.HIGH)
        self.assertEqual(operation["item_reference"], "SN-LIFECYCLE")
        self.assertEqual(operation["problem_description"], "does not start")
        self.assertEqual(operation["status"], Status.ENABLED)

        operation = self.api.approve_repair_operation(object_id)
        self.assertEqual(operation["workflow_state"], RepairOperationState.APPROVED)
        operation = self.api.quote_repair_operation(object_id)
        self.assertEqual(operation["workflow_state"], RepairOperationState.QUOTATION)
        operation = self.api.receive_repair_operation(object_id)
        self.assertEqual(operation["workflow_state"], RepairOperationState.RECEIVED)
        operation = self.api.send_repair_operation(object_id)
        self.assertEqual(operation["workflow_state"], RepairOperationState.SENT)
        operation = self.api.close_repair_operation(object_id)
        self.assertEqual(operation["workflow_state"], RepairOperationState.CLOSED)

        slip = self.api.issue_repair_slip_repair_operation(object_id)
        self.assertEqual(slip["signed"], Flag.YES)
        self.assertEqual(slip["operation_code"], operation["extended_identifier"])

        message = self.api.create_message_repair_operation(
            object_id, {"body": "lifecycle message"}
        )
        self.assertEqual(message["body"], "lifecycle message")
        self.assertEqual(message["edited_date"], None)

        edited = self.api.update_message_repair_operation(
            object_id, message["object_id"], {"body": "lifecycle message edited"}
        )
        self.assertEqual(edited["body"], "lifecycle message edited")
        self.assertNotEqual(edited["edited_date"], None)

        events = self.api.list_messages_repair_operation(object_id)
        kinds = set(event["kind"] for event in events)
        self.assertEqual("state_change" in kinds, True)
        self.assertEqual("message" in kinds, True)
        bodies = [event.get("body") for event in events if event["kind"] == "message"]
        self.assertEqual("lifecycle message edited" in bodies, True)

        result = self.api.delete_message_repair_operation(
            object_id, message["object_id"]
        )
        self.assertEqual(result["result"], "success")
