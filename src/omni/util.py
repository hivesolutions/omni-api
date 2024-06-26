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


def format_places(number, places):
    format_s = "%%0.0%df" % places
    return format_s % number


def filter_args(kwargs):
    if not "object" in kwargs:
        return
    object = kwargs["object"]

    filter_def = object.get("find_d", None)
    filter_string = object.get("find_s", "")
    start_record = object.get("skip", 0)
    number_records = object.get("limit", 10)

    kwargs["start_record"] = start_record
    kwargs["number_records"] = number_records
    if filter_def:
        kwargs["filters[]"] = [
            (
                "%s:%s" % (filter_part, filter_string)
                if filter_part.count(":") < 2
                else filter_part
            )
            for filter_part in filter_def
        ]
    else:
        kwargs["filter_string"] = filter_string

    del kwargs["object"]
