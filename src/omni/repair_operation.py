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


class RepairOperationAPI(object):

    def list_repair_operations(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/repair_operations.json"
        contents = self.get(url, **kwargs)
        return contents

    def create_repair_operation(self, payload):
        url = self.base_url + "omni/repair_operations.json"
        contents = self.post(url, data_j=payload)
        return contents

    def get_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d.json" % object_id
        contents = self.get(url)
        return contents

    def update_repair_operation(self, object_id, payload):
        url = self.base_url + "omni/repair_operations/%d/update.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def approve_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/approve.json" % object_id
        contents = self.put(url)
        return contents

    def reject_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/reject.json" % object_id
        contents = self.put(url)
        return contents

    def quote_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/quote.json" % object_id
        contents = self.put(url)
        return contents

    def receive_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/receive.json" % object_id
        contents = self.put(url)
        return contents

    def send_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/send.json" % object_id
        contents = self.put(url)
        return contents

    def close_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/close.json" % object_id
        contents = self.put(url)
        return contents

    def issue_repair_slip_repair_operation(self, object_id):
        url = (
            self.base_url
            + "omni/repair_operations/%d/issue_repair_slip.json" % object_id
        )
        contents = self.post(url)
        return contents

    def list_messages_repair_operation(self, object_id):
        url = self.base_url + "omni/repair_operations/%d/messages.json" % object_id
        contents = self.get(url)
        return contents

    def create_message_repair_operation(self, object_id, payload):
        url = self.base_url + "omni/repair_operations/%d/messages.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def update_message_repair_operation(self, object_id, message_id, payload):
        url = self.base_url + "omni/repair_operations/%d/messages/%d/update.json" % (
            object_id,
            message_id,
        )
        contents = self.post(url, data_j=payload)
        return contents

    def delete_message_repair_operation(self, object_id, message_id):
        url = self.base_url + "omni/repair_operations/%d/messages/%d.json" % (
            object_id,
            message_id,
        )
        contents = self.delete(url)
        return contents


class RepairOperationState(object):
    UNSET = 1
    OPENED = 2
    APPROVED = 3
    REJECTED = 4
    QUOTATION = 5
    RECEIVED = 6
    SENT = 7
    CLOSED = 8


class RepairType(object):
    WARRANTY = 1
    QUOTATION = 2


class RepairPriority(object):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class RepairOperation(dict):
    pass


class RepairOperationDelta(dict):
    pass


class RepairOperationPayload(dict):
    pass
