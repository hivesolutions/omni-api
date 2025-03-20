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

from . import util


class CustomerAPI(object):

    def list_customers(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/customers.json"
        contents = self.get(url, **kwargs)
        return contents

    def list_persons(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/customer_persons.json"
        contents = self.get(url, **kwargs)
        return contents

    def get_person(self, object_id):
        url = self.base_url + "omni/customer_persons/%d.json" % object_id
        contents = self.get(url)
        return contents

    def update_person(self, object_id, payload):
        url = self.base_url + "omni/customer_persons/%d/update.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    @classmethod
    def customer_name(cls, person):
        if not person.get("surname", None):
            return person["name"]
        return "%s %s " % (person["name"], person["surname"])


class Customer(dict):
    pass


class CustomerPerson(dict):
    pass
