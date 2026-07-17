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
from typing import Any

from omni import util


class UtilTest(TestCase):

    def test_format_places(self) -> None:
        self.assertEqual(util.format_places(1.005, 2), "1.00")
        self.assertEqual(util.format_places(10, 0), "10")
        self.assertEqual(util.format_places(0.4, 2), "0.40")

    def test_filter_args(self) -> None:
        kwargs: dict[str, Any] = dict(number_records=10)
        util.filter_args(kwargs)
        self.assertEqual(kwargs, dict(number_records=10))

        kwargs = dict(object=dict(find_s="paper", skip=10, limit=5))
        util.filter_args(kwargs)
        self.assertEqual(kwargs["start_record"], 10)
        self.assertEqual(kwargs["number_records"], 5)
        self.assertEqual(kwargs["filter_string"], "paper")
        self.assertEqual("object" in kwargs, False)

        kwargs = dict(object=dict(find_d=["description:paper"], find_s="paper"))
        util.filter_args(kwargs)
        self.assertEqual(kwargs["filters[]"], ["description:paper:paper"])

        kwargs = dict(object=dict(find_d=["identifier_prefix:equals:TRF"]))
        util.filter_args(kwargs)
        self.assertEqual(kwargs["filters[]"], ["identifier_prefix:equals:TRF"])
