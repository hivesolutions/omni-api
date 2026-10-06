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
import importlib
from os import environ
from unittest import TestCase
from unittest.mock import MagicMock, patch
from uuid import uuid4
from typing import TYPE_CHECKING

from omni import API, MerchandiseRuleTarget

from .base import build_api, build_mock

if TYPE_CHECKING:
    from omni.brand import BrandPayload
    from omni.merchandise import (
        MerchandiseGroup,
        MerchandiseIdentifier,
        MerchandisePayload,
    )
    from omni.merchandise_rule import MerchandiseRulePayload


class MerchandiseTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        self.api = build_mock()

    def test_update_merchandise(self) -> None:
        payload: MerchandisePayload = {
            "transactional_merchandise": {
                "description": "Laptop",
                "brand": {"object_id": 2},
            }
        }
        result = self.api.update_merchandise(1, payload)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise/1/update.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=payload))

    def test_update_merchandise_request(self) -> None:
        # the (wrapped) payload is sent as JSON, as its nested values
        # can't be encoded as the fields of a multipart form
        api = build_api()
        api.session_id = "session"
        response = MagicMock()
        response.read.return_value = b'{"object_id": 1, "brand": null}'
        response.getcode.return_value = 200
        response.info.return_value = {"Content-Type": "application/json"}
        payload: MerchandisePayload = {
            "transactional_merchandise": {"brand": {"object_id": 2}}
        }
        with patch("appier.http._resolve", return_value=response) as resolve:
            result = api.update_merchandise(1, payload)

        url, method, headers, data = resolve.call_args[0][:4]
        self.assertEqual(
            url,
            "http://localhost:8080/omni/merchandise/1/update.json?session_id=session",
        )
        self.assertEqual(method, "POST")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(data), payload)
        self.assertEqual(result["object_id"], 1)
        self.assertEqual(result.get("brand"), None)

    def test_groups_merchandise(self) -> None:
        items: list[MerchandiseGroup] = [
            {"company_product_code": "THINKBOOK-14-G6", "group": 2, "categories": [3]},
            {"object_id": 4, "group": None, "categories": None, "brand": 5},
        ]
        result = self.api.groups_merchandise(items)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise/groups.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=items))

    def test_rules_merchandise(self) -> None:
        items: list[MerchandiseIdentifier] = [
            {"company_product_code": "THINKBOOK-14-G6"},
            {"object_id": 4},
        ]
        result = self.api.rules_merchandise(items)

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise/rules.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, dict(data_j=dict(root=items)))

    def test_rules_merchandise_options(self) -> None:
        # the unset force flag (false) is sent, as only the options
        # that are not provided are left for the server defaults
        items: list[MerchandiseIdentifier] = [{"object_id": 4}]
        self.api.rules_merchandise(items, force=False)
        self.api.rules_merchandise(items, fields=["brand"])
        self.api.rules_merchandise(items, force=True, fields=[])

        bodies = [kwargs["data_j"] for _method, _url, kwargs in self.api.requests]
        self.assertEqual(
            bodies,
            [
                dict(root=items, force=False),
                dict(root=items, fields=["brand"]),
                dict(root=items, force=True, fields=[]),
            ],
        )

    def test_qualifiers_merchandise(self) -> None:
        result = self.api.qualifiers_merchandise()

        method, url, kwargs = self.api.requests[0]
        self.assertEqual(method, "PUT")
        self.assertEqual(url, "http://localhost:8080/omni/merchandise/qualifiers.json")
        self.assertEqual(result, {})
        self.assertEqual(kwargs, {})

    def test_markers(self) -> None:
        # every type the stub declares has a marker in the module and
        # nothing else does, so that a name the checker accepts from the
        # module may be imported at runtime as well (the module is imported
        # by its full name as the models package shadows its name in omni)
        merchandise = importlib.import_module("omni.merchandise")
        path = os.path.splitext(str(merchandise.__file__))[0] + ".pyi"
        with open(path) as file:
            names = re.findall(r"^class (\w+)\(\w+\):", file.read(), re.M)
        names = [name for name in names if not name.endswith("API")]
        markers = [
            name
            for name, value in vars(merchandise).items()
            if isinstance(value, type) and issubclass(value, dict)
        ]

        self.assertEqual(len(names), 11)
        self.assertEqual(markers, names)
        for name in names:
            self.assertEqual(getattr(merchandise, name)(), {})


class MerchandiseLiveTest(TestCase):

    def setUp(self) -> None:
        TestCase.setUp(self)
        if not environ.get("OMNI_TEST_LIVE"):
            self.skipTest("no live omni instance configured")
        self.api = API()

    def test_update(self) -> None:
        product = [
            value
            for value in self.api.list_store_merchandise(number_records=10)
            if value["_class"] == "Product"
        ][0]
        brand: BrandPayload = {
            "brand": {"name": "omni_api_test_brand_%s" % uuid4().hex[:8]}
        }
        brand_id = self.api.create_brand(brand)["object_id"]

        payload: MerchandisePayload = {
            "transactional_merchandise": {"brand": {"object_id": brand_id}}
        }
        self.api.update_merchandise(product["object_id"], payload)
        full = self.api.get_merchandise(product["object_id"])
        self.assertEqual((full.get("brand") or {}).get("object_id"), brand_id)

        items: list[MerchandiseGroup] = [
            {"object_id": product["object_id"], "brand": None}
        ]
        result = self.api.groups_merchandise(items)
        self.assertEqual(result, dict(result="success"))
        full = self.api.get_merchandise(product["object_id"])
        self.assertEqual(full.get("brand"), None)

    def test_rules(self) -> None:
        product = [
            value
            for value in self.api.list_store_merchandise(number_records=10)
            if value["_class"] == "Product"
        ][0]
        code = product["company_product_code"]
        previous = self.api.get_merchandise(product["object_id"]).get("brand") or {}
        suffix = uuid4().hex[:8]
        brand: BrandPayload = {"brand": {"name": "omni_api_test_brand_%s" % suffix}}
        brand_id = self.api.create_brand(brand)["object_id"]
        payload: MerchandiseRulePayload = {
            "merchandise_rule": {
                "name": "omni_api_test_rule_%s" % suffix,
                "priority": -1,
                "target": MerchandiseRuleTarget.CODE,
                "pattern": "^%s$" % re.escape(code),
                "brand": {"object_id": brand_id},
            }
        }
        rule = self.api.create_merchandise_rule(payload)

        items: list[MerchandiseIdentifier] = [{"company_product_code": code}]
        result = self.api.rules_merchandise(items, fields=["brand"])
        self.assertEqual(result, dict(changed=1))
        full = self.api.get_merchandise(product["object_id"])
        self.assertEqual((full.get("brand") or {}).get("object_id"), brand_id)

        result = self.api.rules_merchandise(items, fields=["brand"])
        self.assertEqual(result, dict(changed=0))
        result = self.api.rules_merchandise(items, force=False, fields=["brand"])
        self.assertEqual(result, dict(changed=0))

        update: MerchandiseRulePayload = {
            "merchandise_rule": {"pattern": "^omni_api_%s$" % suffix}
        }
        self.api.update_merchandise_rule(rule["object_id"], update)
        restore: list[MerchandiseGroup] = [
            {"company_product_code": code, "brand": previous.get("object_id")}
        ]
        self.api.groups_merchandise(restore)

    def test_qualifiers(self) -> None:
        result = self.api.qualifiers_merchandise()
        self.assertEqual(isinstance(result["changed"], int), True)

        result = self.api.qualifiers_merchandise()
        self.assertEqual(result, dict(changed=0))
