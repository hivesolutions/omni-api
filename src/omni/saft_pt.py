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


class SaftPtAPI(object):

    def list_saft_pt(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/saft_pt.json"
        contents = self.get(url, **kwargs)
        return contents

    def create_saft_pt(self, payload):
        url = self.base_url + "omni/saft_pt.json"
        contents = self.post(url, data_j=payload)
        return contents

    def get_saft_pt(self, object_id):
        url = self.base_url + "omni/saft_pt/%d.json" % object_id
        contents = self.get(url)
        return contents

    def file_saft_pt(self, object_id):
        url = self.base_url + "omni/saft_pt/%d/file" % object_id
        contents = self.get(url)
        return contents

    def file_decompressed_saft_pt(self, object_id):
        url = self.base_url + "omni/saft_pt/%d/file_decompressed" % object_id
        contents = self.get(url)
        return contents


class SaftPtReport(dict):
    pass


class SaftPtReportDelta(dict):
    pass


class SaftPtReportPayload(dict):
    pass
