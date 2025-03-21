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


class SaleAPI(object):

    def list_sales(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/sales.json"
        contents = self.get(url, **kwargs)
        return contents

    def create_sale(self, payload):
        url = self.base_url + "omni/sales.json"
        contents = self.post(url, data_j=payload)
        return contents

    def get_sale(self, object_id):
        url = self.base_url + "omni/sales/%d.json" % object_id
        contents = self.get(url)
        return contents

    def vat_sale(self, object_id):
        url = self.base_url + "omni/sales/%d/vat.json" % object_id
        contents = self.get(url)
        return contents

    def issue_money_sale_slip_sale(self, object_id, metadata={}):
        url = self.base_url + "omni/sales/%d/issue_money_sale_slip.json" % object_id
        contents = self.post(url, data_j=dict(metadata=metadata))
        return contents

    def issue_invoice_sale(self, object_id, metadata=None):
        url = self.base_url + "omni/sales/%d/issue_invoice.json" % object_id
        contents = self.post(url, data_j=dict(metadata=metadata))
        return contents

    def issue_receipt_sale(self, object_id, metadata=None):
        url = self.base_url + "omni/sales/%d/issue_receipt.json" % object_id
        contents = self.post(url, data_j=dict(metadata=metadata))
        return contents

    def ensure_receipt_sale(self, object_id, metadata=None):
        url = self.base_url + "omni/sales/%d/ensure_receipt.json" % object_id
        contents = self.post(url, data_j=dict(metadata=metadata))
        return contents

    def self_sales(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/sales/self.json"
        contents = self.get(url, **kwargs)
        return contents

    def stats_sales(
        self,
        date=None,
        unit="day",
        span=7,
        store_id=None,
        has_global=None,
        output="simple",
    ):
        url = self.base_url + "omni/sale_snapshots/stats.json"
        contents = self.get(
            url,
            date=date,
            unit=unit,
            span=span,
            store_id=store_id,
            has_global=has_global,
            output=output,
        )
        return contents


class Sale(dict):
    pass
