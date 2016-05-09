#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
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

from .base import BASE_URL, Api
from .consignment_out import ConsignmentOutApi
from .consignment_slip import ConsignmentSlipApi
from .credit_note import CreditNoteApi
from .customer import CustomerApi
from .document import DocumentApi
from .employee import EmployeeApi
from .entity import EntityApi
from .errors import OmniError
from .export import FUNCS, get_field, open_export
from .invoice import InvoiceApi
from .media import MediaApi
from .merchandise import MerchandiseApi
from .money_sale_slip import MoneySaleSlipApi
from .product import ProductApi
from .return_ import ReturnApi
from .sale_order import SaleOrderApi
from .sale_snapshot import SaleSnapshotApi
from .sale import SaleApi
from .signed_document import SignedDocumentApi
from .stock_adjustment import StockAdjustmentApi
from .store import StoreApi
from .sub_product import SubProductApi
from .supplier import SupplierApi
from .system_company import SystemCompanyApi
from .transfer import TransferApi
from .user import UserApi
from .util import format_places, filter_args
from .web import WebApi

from .export import export as export_do
