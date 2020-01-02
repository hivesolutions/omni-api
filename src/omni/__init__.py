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

from . import models
from . import base
from . import consignment_out
from . import consignment_slip
from . import credit_note
from . import customer
from . import document
from . import employee
from . import entity
from . import errors
from . import export
from . import identifiable
from . import inventory_line
from . import invoice
from . import media
from . import merchandise
from . import money_sale_slip
from . import product
from . import return_
from . import sale_order
from . import sale_snapshot
from . import sale
from . import signed_document
from . import stock_adjustment
from . import store
from . import sub_product
from . import supplier
from . import system_company
from . import transfer
from . import user
from . import util
from . import web

from .base import BASE_URL, API
from .consignment_out import ConsignmentOutAPI
from .consignment_slip import ConsignmentSlipAPI
from .credit_note import CreditNoteAPI
from .customer import CustomerAPI
from .document import DocumentAPI
from .employee import EmployeeAPI
from .entity import EntityAPI
from .errors import OmniError
from .export import FUNCS, get_field, open_export
from .identifiable import IdentifiableAPI
from .inventory_line import InventoryLineAPI
from .invoice import InvoiceAPI
from .media import MediaAPI
from .merchandise import MerchandiseAPI
from .money_sale_slip import MoneySaleSlipAPI
from .product import ProductAPI
from .return_ import ReturnAPI
from .sale_order import SaleOrderAPI
from .sale_snapshot import SaleSnapshotAPI
from .sale import SaleAPI
from .signed_document import SignedDocumentAPI
from .stock_adjustment import StockAdjustmentAPI
from .store import StoreAPI
from .sub_product import SubProductAPI
from .supplier import SupplierAPI
from .system_company import SystemCompanyAPI
from .transfer import TransferAPI
from .user import UserAPI
from .util import format_places, filter_args
from .web import WebAPI

from .export import export as export_do
