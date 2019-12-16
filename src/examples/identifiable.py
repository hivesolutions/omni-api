#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import base

def verify_sequence(identifier_prefix = None, number_records = 10000):
    api = base.get_api()
    kwargs = {}
    if identifier_prefix: kwargs["filters[]"] = "identifier_prefix:equals:%s" % identifier_prefix
    if number_records: kwargs["number_records"] = number_records
    identifiables = api.list_identifiables(**kwargs)
    create_date = None
    identifier_sequence_m = dict()
    for identifiable in identifiables:
        object_id = identifiable["object_id"]
        identifier_prefix = identifiable["identifier_prefix"]
        if create_date:
            appier.verify(
                object_id >= identifiable["object_id"],
                message = "Date is not on the past for the identifiable '%d'" % object_id
            )
        if identifier_prefix in identifier_sequence_m and identifiable["identifier_sequence"]:
            appier.verify(
                identifier_sequence_m[identifier_prefix] == identifiable["identifier_sequence"] + 1,
                message = "Identifier sequence is not sequential for '%d'" % object_id
            )
        object_id = identifiable["object_id"]
        if identifiable["identifier_sequence"]:
            identifier_sequence_m[identifier_prefix] = identifiable["identifier_sequence"]

if __name__ == "__main__":
    verify_sequence()
else:
    __path__ = []
