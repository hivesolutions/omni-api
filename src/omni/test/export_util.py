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
from typing import Any, Mapping, Sequence
import io
import os
import tempfile

from omni import export_util


class ExportUtilTest(TestCase):

    def test_to_string(self) -> None:
        self.assertEqual(export_util.to_string("value"), "value")
        self.assertEqual(export_util.to_string("value", encoding=None), "value")
        self.assertEqual(export_util.to_string(None), None)
        self.assertEqual(export_util.to_string(12), 12)

        # with an encoding the string is encoded into bytes, dropping
        # the characters the encoding cannot represent
        self.assertEqual(
            export_util.to_string("valu\u00e9", encoding="latin-1"), b"valu\xe9"
        )
        self.assertEqual(export_util.to_string("valu\u00e9", encoding="ascii"), b"valu")
        self.assertEqual(export_util.to_string(b"value", encoding="ascii"), b"value")

    def test_to_date(self) -> None:
        self.assertEqual(export_util.to_date(0), "1970-01-01")
        self.assertEqual(export_util.to_date(1790000000), "2026-09-21")
        self.assertEqual(
            export_util.to_date(1790000000.5, encoding="latin-1"), "2026-09-21"
        )

        # a value that is not a timestamp becomes an empty cell rather
        # than failing the export of the whole file
        self.assertEqual(export_util.to_date(None), "")
        self.assertEqual(export_util.to_date("2026-09-21"), "")

    def test_funcs(self) -> None:
        self.assertEqual(export_util.FUNCS["string"], export_util.to_string)
        self.assertEqual(export_util.FUNCS["date"], export_util.to_date)
        self.assertEqual(len(export_util.FUNCS), 2)

    def test_get_field(self) -> None:
        object = dict(
            name="John Doe",
            birth_date=1790000000,
            address=dict(city="Lisbon", street=None),
            phone=None,
            status=1,
        )

        self.assertEqual(export_util.get_field(object, "name"), "John Doe")
        self.assertEqual(export_util.get_field(object, "address.city"), "Lisbon")
        self.assertEqual(export_util.get_field(object, "address.street"), None)
        self.assertEqual(export_util.get_field(object, "phone"), None)
        self.assertEqual(export_util.get_field(object, "status"), 1)

        # the type map converts the field, a null is never converted and
        # an unknown type leaves the value as it is
        type_m = dict(birth_date="date", phone="date", status="integer")
        self.assertEqual(export_util.get_field(object, "birth_date"), 1790000000)
        self.assertEqual(
            export_util.get_field(object, "birth_date", type_m=type_m), "2026-09-21"
        )
        self.assertEqual(export_util.get_field(object, "phone", type_m=type_m), None)
        self.assertEqual(export_util.get_field(object, "status", type_m=type_m), 1)

        # a path through a missing relation stops at it, while a missing
        # attribute of a present object is an error of the caller
        self.assertEqual(export_util.get_field(object, "phone.number"), None)
        self.assertEqual(export_util.get_field(dict(), "name"), dict())
        self.assertRaises(KeyError, export_util.get_field, object, "email")
        self.assertRaises(KeyError, export_util.get_field, object, "address.zip")

    def test_open_export(self) -> None:
        path = os.path.join(tempfile.mkdtemp(), "export.csv")
        file = export_util.open_export(path)
        try:
            self.assertEqual(file.encoding, "latin-1")
            self.assertEqual(file.errors, "ignore")
            file.write("name;city\r\nJo\u00e3o;Lisbon \u20ac\r\n")
        finally:
            file.close()

        # the file is written in latin-1 without newline translation,
        # dropping the characters the encoding cannot represent
        with open(path, "rb") as _file:
            self.assertEqual(_file.read(), b"name;city\r\nJo\xe3o;Lisbon \r\n")

    def test_export(self) -> None:
        objects = [
            dict(name="John Doe", address=dict(city="Lisbon"), birth_date=1790000000),
            dict(name="Jane Doe", address=dict(city="Porto"), birth_date=0),
            dict(name="Jim Doe", address=dict(city=None), birth_date=None),
        ]
        calls: list[dict[str, Any]] = []
        ticks: list[tuple[int, int]] = []

        def caller(object: dict[str, Any]) -> list[dict[str, Any]]:
            calls.append(object)
            return objects[object["skip"] : object["skip"] + object["limit"]]

        def callback(index: int, objects: Sequence[Mapping[str, Any]]) -> None:
            ticks.append((index, len(objects)))

        file = io.StringIO()
        export_util.export(
            file,
            caller,
            ["name", "address.city", "birth_date"],
            names=["Name", "City", "Birth"],
            type_m=dict(birth_date="date"),
            step=2,
            callback=callback,
        )

        # the objects are retrieved page by page until a page comes back
        # short, the header carries the names and the rows the fields
        self.assertEqual(
            file.getvalue(),
            "Name;City;Birth\r\n"
            "John Doe;Lisbon;2026-09-21\r\n"
            "Jane Doe;Porto;1970-01-01\r\n"
            "Jim Doe;;\r\n",
        )
        self.assertEqual(calls, [dict(skip=0, limit=2), dict(skip=2, limit=2)])
        self.assertEqual(ticks, [(0, 2), (2, 1)])

        # a full last page costs one more retrieval, which comes back
        # empty, and the names default to the attributes
        calls[:] = []
        ticks[:] = []
        file = io.StringIO()
        export_util.export(file, caller, ["name"], step=3, callback=callback)

        self.assertEqual(file.getvalue(), "name\r\nJohn Doe\r\nJane Doe\r\nJim Doe\r\n")
        self.assertEqual(calls, [dict(skip=0, limit=3), dict(skip=3, limit=3)])
        self.assertEqual(ticks, [(0, 3)])

        # nothing to export leaves the header alone
        file = io.StringIO()
        export_util.export(file, lambda object: [], ["name"])

        self.assertEqual(file.getvalue(), "name\r\n")
