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

import omni


def run():
    # creates the API client instance using the currently available
    # environment configuration (eg: OMNI_BASE_URL, OMNI_USERNAME and
    # OMNI_PASSWORD) as the basis for the connection
    api = omni.API()

    # retrieves the merchandise available in the current (session) store
    # and filters it so that only the items with both stock and a valid
    # retail price are considered sellable for the checkout
    merchandise = api.list_store_merchandise(number_records=30)
    sellable = [
        item
        for item in merchandise
        if (item.get("stock_on_hand") or 0) > 0 and item.get("retail_price")
    ]
    item = sellable[0]
    retail_price = item["retail_price"] or 0.0

    # creates the sale using the minimal creation payload, the financial
    # values are calculated on the server side using the inventory line
    # prices and the payment must match the price with VAT of the sale
    sale = api.create_sale(
        {
            "transaction": {
                "sale_lines": [
                    {"merchandise": {"object_id": item["object_id"]}, "quantity": 1}
                ],
                "primary_payment": {
                    "payment_lines": [
                        {
                            "amount": {"value": retail_price},
                            "payment_method": {"_class": "CashPayment"},
                        }
                    ]
                },
            },
            "customer": {"_parameters": {"type": "anonymous"}},
        }
    )
    print("created sale %s" % sale["extended_identifier"])
    print("paid %s" % (sale["payment_state"] == omni.PaymentState.PAID))

    # issues the invoice for the sale and then ensures that the proper
    # receipt exists for it, both documents are signed at issue time
    invoice = api.issue_invoice_sale(sale["object_id"])
    print("issued invoice %s" % invoice["extended_identifier"])
    print("signed %s" % (invoice["signed"] == omni.Flag.YES))
    receipt = api.ensure_receipt_sale(sale["object_id"])
    print("ensured receipt %s" % receipt["extended_identifier"])

    # retrieves the VAT list of the sale, note that the value may be
    # unset in case the VAT table could not be calculated
    vat = api.vat_sale(sale["object_id"])
    for vat_item in vat["vat_list"] or []:
        print("vat rate %.2f -> %.2f" % (vat_item["vat_rate"], vat_item["vat"]))

    # retrieves the sales statistics for the current time frame, the
    # returned map is keyed by the store object id ("-1" for the global
    # aggregate when requested)
    stats = api.stats_sales(has_global=True)
    for store_id, store_stats in stats.items():
        totals = store_stats["totals"]
        print(
            "store %s (%s) -> %d sales"
            % (store_id, store_stats["name"], totals["number_sales"]["value"])
        )


if __name__ == "__main__":
    run()
