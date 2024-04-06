#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import base


def verify_signature(identifier_prefix=None, number_records=600):
    api = base.get_api()
    kwargs = {}
    if identifier_prefix:
        kwargs["filters[]"] = "identifier_prefix:equals:%s" % identifier_prefix
    if number_records:
        kwargs["number_records"] = number_records
    documents = api.list_signed_documents(**kwargs)
    for document in documents:
        object_id = document["object_id"]
        result = api.verify_signed_document(object_id)
        status = result.get("result", "failure")
        appier.verify(
            status == "success", "Failure validating document '%d'" % object_id
        )


if __name__ == "__main__":
    verify_signature()
else:
    __path__ = []
