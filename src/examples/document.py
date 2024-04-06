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

import appier

from . import base


def verify_sequence(identifier_prefix="MSLDVD", number_records=600):
    api = base.get_api()
    kwargs = {}
    if identifier_prefix:
        kwargs["filters[]"] = "identifier_prefix:equals:%s" % identifier_prefix
    if number_records:
        kwargs["number_records"] = number_records
    documents = api.list_documents(**kwargs)
    create_date = None
    identifier_sequence = None
    for document in documents:
        object_id = document["object_id"]
        if create_date:
            appier.verify(
                create_date >= document["create_date"],
                message="Date is not on the past for the document '%d'" % object_id,
            )
        if identifier_sequence:
            appier.verify(
                identifier_sequence == document["identifier_sequence"] + 1,
                message="Identifier sequence is not sequential for '%d'" % object_id,
            )
        create_date = document["create_date"]
        identifier_sequence = document["identifier_sequence"]


if __name__ == "__main__":
    verify_sequence()
else:
    __path__ = []
