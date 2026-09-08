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


class SupplierBillAPI(object):

    def list_supplier_bills(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/supplier_bills.json"
        contents = self.get(url, **kwargs)
        return contents

    def get_permissions_supplier_bill(self):
        url = self.base_url + "omni/supplier_bills/permissions.json"
        contents = self.get(url)
        return contents

    def create_supplier_bill(self, payload):
        url = self.base_url + "omni/supplier_bills.json"
        contents = self.post(url, data_j=payload)
        return contents

    def get_supplier_bill(self, object_id):
        url = self.base_url + "omni/supplier_bills/%d.json" % object_id
        contents = self.get(url)
        return contents

    def update_supplier_bill(self, object_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/update.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def approve_supplier_bill(self, object_id):
        url = self.base_url + "omni/supplier_bills/%d/approve.json" % object_id
        contents = self.put(url)
        return contents

    def request_supplier_bill(self, object_id):
        url = self.base_url + "omni/supplier_bills/%d/request.json" % object_id
        contents = self.post(url)
        return contents

    def cancel_supplier_bill(self, object_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/cancel.json" % object_id
        contents = self.put(url, data_j=payload)
        return contents

    def report_supplier_bills(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/supplier_bills/report.json"
        contents = self.get(url, **kwargs)
        return contents

    def export_supplier_bills(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/supplier_bills/export.csv"
        contents = self.get(url, **kwargs)
        return contents

    def create_payment_supplier_bill(self, object_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/payments.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def request_payment_supplier_bill(self, object_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/payments/request.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def reverse_payment_supplier_bill(self, object_id, payment_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/payments/%d/reverse.json" % (
            object_id,
            payment_id,
        )
        contents = self.put(url, data_j=payload)
        return contents

    def list_messages_supplier_bill(self, object_id):
        url = self.base_url + "omni/supplier_bills/%d/messages.json" % object_id
        contents = self.get(url)
        return contents

    def create_message_supplier_bill(self, object_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/messages.json" % object_id
        options = self._message_payload_options_supplier_bill(payload)
        contents = self.post(url, **options)
        return contents

    def update_message_supplier_bill(self, object_id, message_id, payload):
        url = self.base_url + "omni/supplier_bills/%d/messages/%d/update.json" % (
            object_id,
            message_id,
        )
        options = self._message_payload_options_supplier_bill(payload)
        contents = self.post(url, **options)
        return contents

    def delete_message_supplier_bill(self, object_id, message_id):
        url = self.base_url + "omni/supplier_bills/%d/messages/%d.json" % (
            object_id,
            message_id,
        )
        contents = self.delete(url)
        return contents

    def delete_file_message_supplier_bill(self, object_id, message_id, file_id):
        url = self.base_url + "omni/supplier_bills/%d/messages/%d/files/%d.json" % (
            object_id,
            message_id,
            file_id,
        )
        contents = self.delete(url)
        return contents

    def _message_payload_options_supplier_bill(self, payload):
        payload = dict(payload)
        files = payload.pop("files", None)
        if not files:
            return dict(data_j=payload)
        payload["files"] = files
        return dict(data_m=payload)


class SupplierBill(dict):
    pass


class SupplierBillDelta(dict):
    pass


class SupplierBillPayload(dict):
    pass


class SupplierBillPayment(dict):
    pass


class SupplierBillPaymentDelta(dict):
    pass


class SupplierBillPaymentPayload(dict):
    pass


class SupplierBillReasonPayload(dict):
    pass


class SupplierBillMessagePayload(dict):
    pass


class SupplierBillBalance(dict):
    pass


class SupplierBillReport(dict):
    pass


class SupplierBillState(object):
    PENDING = 1
    APPROVED = 2
    CANCELED = 3


class SupplierBillPaymentType(object):
    PAYMENT = 1
    HISTORICAL = 2
    CREDIT = 3
    REFUND = 4
    TRANSFER = 5
