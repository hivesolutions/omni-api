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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

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

import appier

from . import web
from . import sale
from . import user
from . import store
from . import media
from . import errors
from . import entity
from . import return_
from . import invoice
from . import product
from . import customer
from . import supplier
from . import transfer
from . import document
from . import employee
from . import sale_order
from . import credit_note
from . import sub_product
from . import merchandise
from . import sale_snapshot
from . import system_company
from . import money_sale_slip
from . import signed_document
from . import consignment_out
from . import consignment_slip
from . import stock_adjustment

BASE_URL = "http://localhost:8080/mvc/"
""" The default base url to be used when no other
base url value is provided to the constructor """

CLIENT_ID = None
""" The default value to be used for the client id
in case no client id is provided to the api client """

CLIENT_SECRET = None
""" The secret value to be used for situations where
no client secret has been provided to the client """

REDIRECT_URL = "http://localhost:8080/oauth"
""" The redirect url used as default (fallback) value
in case none is provided to the api (client) """

SCOPE = (
    "base",
    "base.user",
    "base.admin",
    "foundation.store.list",
    "foundation.web.subscribe"
)
""" The list of permissions to be used to create the
scope string for the oauth value """

class Api(
    appier.OAuth2Api,
    web.WebApi,
    sale.SaleApi,
    user.UserApi,
    store.StoreApi,
    media.MediaApi,
    entity.EntityApi,
    return_.ReturnApi,
    invoice.InvoiceApi,
    product.ProductApi,
    customer.CustomerApi,
    supplier.SupplierApi,
    transfer.TransferApi,
    document.DocumentApi,
    employee.EmployeeApi,
    sale_order.SaleOrderApi,
    credit_note.CreditNoteApi,
    sub_product.SubProductApi,
    merchandise.MerchandiseApi,
    sale_snapshot.SaleSnapshotApi,
    system_company.SystemCompanyApi,
    money_sale_slip.MoneySaleSlipApi,
    signed_document.SignedDocumentApi,
    consignment_out.ConsignmentOutApi,
    consignment_slip.ConsignmentSlipApi,
    stock_adjustment.StockAdjustmentApi
):

    def __init__(self, *args, **kwargs):
        appier.OAuth2Api.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("OMNI_BASE_URL", BASE_URL)
        self.open_url = appier.conf("OMNI_OPEN_URL", self.base_url)
        self.prefix = appier.conf("OMNI_PREFIX", "adm/")
        self.client_id = appier.conf("OMNI_ID", CLIENT_ID)
        self.client_secret = appier.conf("OMNI_SECRET", CLIENT_SECRET)
        self.redirect_url = appier.conf("OMNI_REDIRECT_URL", REDIRECT_URL)
        self.scope = appier.conf("OMNI_SCOPE", SCOPE)
        self.username = appier.conf("OMNI_USERNAME", None)
        self.password = appier.conf("OMNI_PASSWORD", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.open_url = kwargs.get("open_url", self.open_url)
        self.prefix = kwargs.get("prefix", self.prefix)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.redirect_url = kwargs.get("redirect_url", self.redirect_url)
        self.scope = kwargs.get("scope", self.scope)
        self.access_token = kwargs.get("access_token", None)
        self.session_id = kwargs.get("session_id", None)
        self.username = kwargs.get("username", self.username)
        self.password = kwargs.get("password", self.password)
        self.object_id = kwargs.get("object_id", None)
        self.acl = kwargs.get("acl", None)
        self.tokens = kwargs.get("tokens", None)
        self.company = kwargs.get("company", None)
        self.wrap_exception = kwargs.get("wrap_exception", True)
        self.mode = kwargs.get("mode", None) or self._get_mode()

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        token = kwargs.pop("token", False)
        if auth: kwargs["session_id"] = self.get_session_id()
        if token: kwargs["access_token"] = self.get_access_token()

    def handle_error(self, error):
        if self.is_direct(): self.handle_direct(error)
        elif self.is_oauth(): raise appier.OAuthAccessError(
            message = "Problems using access token found must re-authorize"
        )
        raise

    def handle_direct(self, error):
        if not self.wrap_exception: raise
        data = error.read_json()
        if not data: raise
        exception = data.get("exception", {})
        error = errors.OmniError(error, exception)
        raise error

    def get_session_id(self):
        if self.session_id: return self.session_id
        if self.is_direct(): return self.login()
        elif self.is_oauth(): return self.oauth_session()

    def get_access_token(self):
        if self.access_token: return self.access_token
        if self.is_direct(): return None
        raise appier.OAuthAccessError(
            message = "No access token found must re-authorize"
        )

    def auth_callback(self, params, headers):
        if not self._has_mode(): raise appier.APIAccessError(
            message = "Session expired or authentication issues"
        )
        self.session_id = None
        session_id = self.get_session_id()
        params["session_id"] = session_id

    def login(self, username = None, password = None):
        username = username or self.username
        password = password or self.password
        url = self.base_url + "omni/login.json"
        contents = self.get(
            url,
            callback = False,
            auth = False,
            token = False,
            username = username,
            password = password
        )
        self.username = contents.get("username", None)
        self.object_id = contents.get("object_id", None)
        self.acl = contents.get("acl", None)
        self.session_id = contents.get("session_id", None)
        self.tokens = self.acl.keys()
        self.trigger("auth", contents)
        return self.session_id

    def oauth_authorize(self, state = None):
        url = self.base_url + self.prefix + "oauth/authorize"
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )
        if state: values["state"] = state
        data = appier.legacy.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code):
        url = self.base_url + "omni/oauth/access_token"
        contents = self.post(
            url,
            auth = False,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "authorization_code",
            redirect_uri = self.redirect_url,
            code = code
        )
        self.access_token = contents["access_token"]
        self.trigger("access_token", self.access_token)
        return self.access_token

    def oauth_session(self):
        url = self.base_url + "omni/oauth/start_session"
        contents = self.get(url, callback = False, auth = False, token = True)
        self.username = contents.get("username", None)
        self.object_id = contents.get("object_id", None)
        self.acl = contents.get("acl", None)
        self.session_id = contents.get("session_id", None)
        self.tokens = self.acl.keys()
        self.trigger("auth", contents)
        return self.session_id

    def ping(self):
        return self.self_user()

    def _has_mode(self):
        return self.is_direct() or self.is_oauth()

    def _get_mode(self):
        if self.username and self.password: return appier.OAuthApi.DIRECT_MODE
        elif self.client_id and self.client_secret: return appier.OAuthApi.OAUTH_MODE
        return appier.OAuthApi.UNSET_MODE
