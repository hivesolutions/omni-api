#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import util

class InvoiceApi(object):

    @classmethod
    def normalize_invoice(cls, invoice):
        payload = invoice.get("payload", {})
        operation = payload.get("operation", {})

        type = operation.get("type", 1)

        if type == 1:
            operation["subtotal"] = operation["price_vat"] + operation["discount_vat"]
        elif type == 2:
            operation["subtotal"] = operation["price"]["value"]

        operation["vat_s"] = util.format_places(operation["vat"], 2)
        operation["subtotal_s"] = util.format_places(operation["subtotal"], 2)
        operation["discount_s"] = util.format_places(operation["discount"], 2)
        operation["discount_vat_s"] = util.format_places(operation["discount_vat"], 2)
        operation["price_vat_s"] = util.format_places(operation["price_vat"], 2)

        for item in operation["vat_list"]:
            item["vat_rate_s"] = util.format_places(item["vat_rate"], 2)
            item["vat_s"] = util.format_places(item["vat"], 2)

        for sale_line in operation["sale_lines"]:
            merchandise = sale_line["merchandise"]
            sale_line["vat_rate_s"] = util.format_places(sale_line["vat_rate"], 2)
            sale_line["quantity_s"] = util.format_places(
                sale_line["quantity"],
                sale_line.get("quantity_places", 0),
            )
            sale_line["unit_discount_s"] = util.format_places(sale_line["unit_discount"], 2)
            sale_line["unit_discount_vat_s"] = util.format_places(sale_line["unit_discount_vat"], 2)
            sale_line["unit_price_s"] = util.format_places(sale_line["unit_price"]["value"], 2)
            sale_line["unit_price_vat_s"] = util.format_places(sale_line["unit_price_vat"], 2)
            sale_line["price_s"] = util.format_places(sale_line["price"], 2)
            sale_line["price_vat_s"] = util.format_places(sale_line["price_vat"], 2)
            sale_line["weight_s"] = util.format_places(
                (merchandise["weight"] or 0.0) * sale_line["quantity"], 3
            )

        operation["lines"] = operation["sale_lines"]

    def list_invoices(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/invoices.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def get_invoice(self, object_id):
        url = self.base_url + "omni/invoices/%d.json" % object_id
        contents = self.get(url)
        return contents
