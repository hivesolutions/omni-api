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


class ApprovalRequestAPI(object):

    def list_approval_requests(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/approval_requests.json"
        contents = self.get(url, **kwargs)
        return contents

    def get_approval_request(self, object_id):
        url = self.base_url + "omni/approval_requests/%d.json" % object_id
        contents = self.get(url)
        return contents

    def approve_approval_request(self, object_id):
        url = self.base_url + "omni/approval_requests/%d/approve.json" % object_id
        contents = self.post(url)
        return contents

    def reject_approval_request(self, object_id, payload):
        url = self.base_url + "omni/approval_requests/%d/reject.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def withdraw_approval_request(self, object_id):
        url = self.base_url + "omni/approval_requests/%d/withdraw.json" % object_id
        contents = self.post(url)
        return contents


class ApprovalRequest(dict):
    pass


class ApprovalRequestReasonPayload(dict):
    pass
