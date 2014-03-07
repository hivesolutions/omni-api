#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

def format_places(number, places):
    format_s = "%%0.0%df" % places
    return format_s % number

def filter_args(kwargs):
    if not "object" in kwargs: return
    object = kwargs["object"]

    filter_def = object.get("find_d", None)
    filter_string = object.get("find_s", "")
    start_record = object.get("skip", 0)
    number_records = object.get("limit", 10)

    kwargs["start_record"] = start_record
    kwargs["number_records"] = number_records
    if filter_def: kwargs["filters[]"] = [
        "%s:%s" % (filter_part, filter_string) for filter_part in filter_def
    ]
    else: kwargs["filter_string"] = filter_string

    del kwargs["object"]
