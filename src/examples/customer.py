#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys

import omni

import base

ATTRIBUTES = (
    "name",
    "tax_number",
    "birth_date",
    "primary_contact_information.email",
    "primary_address.street_name",
    "primary_address.city",
    "primary_address.zip_code",
    "primary_address.country",
)

NAMES = (
    "name",
    "nif",
    "birth date",
    "email",
    "address",
    "city",
    "zip code",
    "country"
)

TYPE_M = dict(
    birth_date = "date"
)

STEP = 32768

if __name__ == "__main__":
    api = base.get_api()
    file = omni.open_export("customers.csv")
    try:
        omni.export_do(
            file,
            api.list_persons,
            ATTRIBUTES,
            names = NAMES,
            type_m = TYPE_M,
            step = STEP,
            callback = lambda i, v: sys.stdout.write("Imported " + str(i + len(v)) + " items\n")
        )
    finally:
        file.close()
else:
    __path__ = []
