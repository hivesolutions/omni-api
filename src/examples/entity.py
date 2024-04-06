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


def verify_sequence(number_records=10000):
    api = base.get_api()
    kwargs = {}
    if number_records:
        kwargs["number_records"] = number_records
    entities = api.list_entities(**kwargs)
    current_id = None
    for entity in entities:
        object_id = entity["object_id"]
        if current_id:
            appier.verify(
                current_id > object_id,
                message="No valid identifier sequence found for '%d'" % object_id,
            )
        current_id = entity["object_id"]


if __name__ == "__main__":
    verify_sequence()
else:
    __path__ = []
