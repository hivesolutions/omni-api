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

class ConsignmentOutAPI(object):

    def list_consignments_out(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/consignments_out.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def create_consignment_out(self, payload):
        url = self.base_url + "omni/consignments_out.json"
        contents = self.post(url, data_j = payload)
        return contents

    def get_consignment_out(self, object_id):
        url = self.base_url + "omni/consignments_out/%d.json" % object_id
        contents = self.get(url)
        return contents

    def issue_consignment_slip_consignment_out(self, object_id, metadata = {}):
        url = self.base_url + "omni/consignments_out/%d/issue_consignment_slip.json" % object_id
        contents = self.post(url, data_j = dict(metadata = metadata))
        return contents

    def self_consignments_out(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/consignments_out/self.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents
