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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import util

class MerchandiseAPI(object):

    def list_merchandise(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/merchandise.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def update_merchandise(self, id, payload):
        url = self.base_url + "omni/merchandise/%d/update.json" % id
        contents = self.post(url, data_m = payload)
        return contents

    def list_store_merchandise(self, store_id = None, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/merchandise/store.json"
        contents = self.get(
            url,
            store_id = store_id,
            **kwargs
        )
        return contents

    def prices_merchandise(self, items):
        url = self.base_url + "omni/merchandise/prices.json"
        self.put(url, data_j = items)

    def costs_merchandise(self, items):
        url = self.base_url + "omni/merchandise/costs.json"
        self.put(url, data_j = items)
