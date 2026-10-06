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
import json
from os import environ
from unittest import TestCase
from unittest.mock import MagicMock, patch
from uuid import uuid4
from typing import TYPE_CHECKING

from omni import API, OmniError, Status, MerchandiseRuleTarget, merchandise_rule

from .base import build_api, build_mock

if TYPE_CHECKING:
    from omni.brand import BrandPayload
    from omni.merchandise_rule import MerchandiseRuleImport, MerchandiseRulePayload


class MerchandiseRuleTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_list_merchandise_rules(self) -> None:
        result = self.api.list_merchandise_rules(
            object={"find_s": "Laptops", "skip": 10, "limit": 5}
        )

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise_rules.json")
        self.assertEqual(result, {})
        self.assertEqual(
            kwargs, dict(start_record=10, number_records=5, filter_string="Laptops")
        )

    def test_create_merchandise_rule(self) -> None:
        payload: MerchandiseRulePayload = {
            "merchandise_rule": {
                "name": "ThinkBook Laptops",
                "priority": 10,
                "target": MerchandiseRuleTarget.CODE,
                "pattern": "^THINKBOOK-",
                "group_": {"object_id": 2},
                "brand": {"object_id": 3},
                "categories": [{"object_id": 4}, {"object_id": 5}],
            }
        }
        result = self.api.create_merchandise_rule(payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise_rules.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_get_merchandise_rule(self) -> None:
        result = self.api.get_merchandise_rule(1)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise_rules/1.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_update_merchandise_rule(self) -> None:
        payload: MerchandiseRulePayload = {
            "merchandise_rule": {"target": MerchandiseRuleTarget.NAME, "categories": []}
        }
        result = self.api.update_merchandise_rule(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/merchandise_rules/1/update.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_import_merchandise_rules(self) -> None:
        items: list[MerchandiseRuleImport] = [
            {"name": "ThinkBook Laptops", "target": "code", "pattern": "^THINKBOOK-"},
            {"name": "Refurbished", "priority": 20, "brand": None, "categories": []},
        ]
        result = self.api.import_merchandise_rules(items)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            url, "http://localhost:8080/omni/merchandise_rules/import.json"
        )
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=items))

    def test_import_merchandise_rules_request(self) -> None:
        # the rules are sent as a (bare) JSON list, that the server reads
        # as its root field, and the counts of the rules are decoded
        api = build_api()
        api.session_id = "session"
        response = MagicMock()
        response.read.return_value = b'{"created": 1, "updated": 1}'
        response.getcode.return_value = 200
        response.info.return_value = {"Content-Type": "application/json"}
        items: list[MerchandiseRuleImport] = [
            {"name": "ThinkBook Laptops", "target": MerchandiseRuleTarget.CODE},
            {"name": "Refurbished", "target": "name", "group": ""},
        ]
        with patch("appier.http._resolve", return_value=response) as resolve:
            result = api.import_merchandise_rules(items)

        url, method, headers, data = resolve.call_args[0][:4]
        self.assertEqual(
            url,
            "http://localhost:8080/omni/merchandise_rules/import.json?session_id=session",
        )
        self.assertEqual(method, "POST")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(data), items)
        self.assertEqual(result["created"], 1)
        self.assertEqual(result["updated"], 1)

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well
        path = os.path.splitext(merchandise_rule.__file__)[0] + ".pyi"
        with open(path) as file:
            names = re.findall(r"^class (\w+)\(\w+\):", file.read(), re.M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(merchandise_rule).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 5)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(merchandise_rule, name)(), {})


class MerchandiseRuleLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_crud(self) -> None:
        suffix = uuid4().hex[:8]
        brand: BrandPayload = {"brand": {"name": "omni_api_test_brand_%s" % suffix}}
        brand_id = self.api.create_brand(brand)["object_id"]

        name = "omni_api_test_rule_%s" % suffix
        payload: MerchandiseRulePayload = {
            "merchandise_rule": {
                "name": name,
                "priority": 10,
                "target": MerchandiseRuleTarget.NAME,
                "pattern": "^omni_api_%s" % suffix,
                "brand": {"object_id": brand_id},
            }
        }
        created = self.api.create_merchandise_rule(payload)
        self.assertNotEqual(created["object_id"], None)
        self.assertEqual(created["_class"], "MerchandiseRule")
        self.assertEqual(created["name"], name)
        self.assertEqual(created["priority"], 10)
        self.assertEqual(created["target"], MerchandiseRuleTarget.NAME)
        self.assertEqual(created["pattern"], "^omni_api_%s" % suffix)
        self.assertEqual(created["status"], Status.ENABLED)

        full = self.api.get_merchandise_rule(created["object_id"])
        self.assertEqual(full["object_id"], created["object_id"])
        self.assertEqual(full["target_string"], "name")
        self.assertEqual("group_" in full, True)
        self.assertEqual(full.get("group_"), None)
        self.assertEqual((full.get("brand") or {}).get("object_id"), brand_id)
        self.assertEqual(full.get("categories"), [])

        merchandise_rules = self.api.list_merchandise_rules(object={"find_s": name})
        self.assertEqual(len(merchandise_rules), 1)
        self.assertEqual(merchandise_rules[0]["object_id"], created["object_id"])
        self.assertEqual(merchandise_rules[0]["target_string"], "name")
        self.assertEqual("brand" in merchandise_rules[0], False)

        update: MerchandiseRulePayload = {
            "merchandise_rule": {"target": MerchandiseRuleTarget.CODE}
        }
        updated = self.api.update_merchandise_rule(created["object_id"], update)
        self.assertEqual(updated["target"], MerchandiseRuleTarget.CODE)
        self.assertEqual(updated["name"], name)

        full = self.api.get_merchandise_rule(created["object_id"])
        self.assertEqual(full["target_string"], "code")
        self.assertEqual((full.get("brand") or {}).get("object_id"), brand_id)

    def test_import(self) -> None:
        suffix = uuid4().hex[:8]
        brand_name = "omni_api_test_brand_%s" % suffix
        items: list[MerchandiseRuleImport] = [
            {
                "name": "omni_api_test_rule_%s" % suffix,
                "target": "code",
                "pattern": "^omni_api_%s" % suffix,
                "brand": brand_name,
            },
            {
                "name": "omni_api_test_other_rule_%s" % suffix,
                "priority": 20,
                "target": MerchandiseRuleTarget.NAME,
                "pattern": "^omni_api_%s" % suffix,
                "categories": [],
            },
        ]
        result = self.api.import_merchandise_rules(items)
        self.assertEqual(result, dict(created=2, updated=0))

        brands = self.api.list_brands(object={"find_s": brand_name})
        self.assertEqual([value["name"] for value in brands], [brand_name])

        merchandise_rules = self.api.list_merchandise_rules(
            object={"find_s": "omni_api_test_rule_%s" % suffix}
        )
        self.assertEqual(len(merchandise_rules), 1)
        full = self.api.get_merchandise_rule(merchandise_rules[0]["object_id"])
        self.assertEqual(full["target"], MerchandiseRuleTarget.CODE)
        self.assertEqual((full.get("brand") or {}).get("name"), brand_name)

        update: list[MerchandiseRuleImport] = [
            {"name": "omni_api_test_rule_%s" % suffix, "priority": 5, "brand": None}
        ]
        result = self.api.import_merchandise_rules(update)
        self.assertEqual(result, dict(created=0, updated=1))

        full = self.api.get_merchandise_rule(merchandise_rules[0]["object_id"])
        self.assertEqual(full["priority"], 5)
        self.assertEqual("brand" in full, True)
        self.assertEqual(full.get("brand"), None)
        self.assertEqual(full["pattern"], "^omni_api_%s" % suffix)

        invalid: list[MerchandiseRuleImport] = [
            {"name": "omni_api_test_invalid_rule_%s" % suffix, "pattern": "("}
        ]
        with self.assertRaises(OmniError) as context:
            self.api.import_merchandise_rules(invalid)
        self.assertEqual(context.exception.name(), "ModelValidationError")
        self.assertEqual(
            self.api.list_merchandise_rules(
                object={"find_s": "omni_api_test_invalid_rule_%s" % suffix}
            ),
            [],
        )
