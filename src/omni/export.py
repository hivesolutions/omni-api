#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import csv
import datetime

import appier

STEP = 256
""" The default step value to be used in the iteration
around the values retrieved from the server side, a large
value on this field may create some memory problems in the
server and a large latency """

def to_string(value, encoding = None):
    if encoding and appier.is_unicode(value):
        value = value.encode(encoding, errors = "ignore")
    return value

def to_date(value, encoding = None):
    try: value_d = datetime.datetime.utcfromtimestamp(value)
    except: return ""
    return value_d.strftime("%Y-%m-%d")

FUNCS = dict(
    string = to_string,
    date = to_date
)

def get_field(object, name, encoding = "latin-1", type_m = dict()):
    if appier.PYTHON_3: encoding = None
    name_l = name.split(".")

    for key in name_l:
        if not object: break
        object = object[key]

    _type = type_m.get(name, "string")
    func = FUNCS.get(_type, None)
    object = func(object, encoding = encoding) if func and not object == None else object

    return object

def open_export(path):
    if appier.PYTHON_3: return open(
        path,
        "w",
        newline = "",
        encoding = "latin-1",
        errors = "ignore"
    )
    else: return open(path, "wb")

def export(
    file,
    caller,
    attributes,
    names = None,
    type_m = None,
    step = STEP,
    output = True
):
    names = names or attributes
    type_m = type_m or dict()

    csv_f = csv.writer(file, delimiter = ";")
    csv_f.writerow(names)

    index = 0

    while True:
        object = dict(skip = index, limit = step)
        objects = caller(object = object)
        if not objects: break

        for object in objects:
            values = [get_field(object, key, type_m = type_m) for key in attributes]
            csv_f.writerow(values)

        index += step

        if output: print(index)
