#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import appier

from omni import web
from omni import sale
from omni import user
from omni import store
from omni import errors
from omni import entity
from omni import return_
from omni import invoice
from omni import customer
from omni import supplier
from omni import document
from omni import employee
from omni import merchandise
from omni import system_company
from omni import money_sale_slip
from omni import signed_document

DIRECT_MODE = 1
""" The direct mode where a complete access is allowed
to the client by providing the "normal" credentials to
it and ensuring a complete authentication """

OAUTH_MODE = 2
""" The oauth client mode where the set of permissions
(scope) is authorized on behalf on an already authenticated
user using a web agent (recommended mode) """

UNSET_MODE = 3
""" The unset client mode for situations where the client
exists but not enough information is provided to it so that
it knows how to interact with the server side (detached client) """

BASE_URL = "https://ldj.frontdoorhd.com/"
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
""" The list of permission to be used to create the
scope string for the oauth value """

class Api(
    appier.Api,
    web.WebApi,
    sale.SaleApi,
    user.UserApi,
    store.StoreApi,
    entity.EntityApi,
    return_.ReturnApi,
    invoice.InvoiceApi,
    customer.CustomerApi,
    supplier.SupplierApi,
    document.DocumentApi,
    employee.EmployeeApi,
    merchandise.MerchandiseApi,
    system_company.SystemCompanyApi,
    money_sale_slip.MoneySaleSlipApi,
    signed_document.SignedDocumentApi
):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.prefix = kwargs.get("prefix", "adm/")
        self.client_id = kwargs.get("client_id", CLIENT_ID)
        self.client_secret = kwargs.get("client_secret", CLIENT_SECRET)
        self.redirect_url = kwargs.get("redirect_url", REDIRECT_URL)
        self.scope = kwargs.get("scope", SCOPE)
        self.access_token = kwargs.get("access_token", None)
        self.session_id = kwargs.get("session_id", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.acl = kwargs.get("acl", None)
        self.tokens = kwargs.get("tokens", None)
        self.company = kwargs.get("company", None)
        self.wrap_exception = kwargs.get("wrap_exception", True)
        self.mode = kwargs.get("mode", None) or self._get_mode()

    def request(self, method, *args, **kwargs):
        try:
            result = method(*args, **kwargs)
        except appier.exceptions.HTTPError as exception:
            if self.mode == DIRECT_MODE: self.handle_error(exception)
            elif self.mode == OAUTH_MODE: raise errors.OAuthAccessError(
                "Problems using access token found must re-authorize"
            )
            raise

        return result

    def handle_error(self, error):
        if not self.wrap_exception: raise
        data = error.read_json()
        if not data: raise
        exception = data.get("exception", {})
        error = errors.OmniError(error, exception)
        raise error

    def build_kwargs(self, kwargs, auth = True, token = False):
        if auth: kwargs["session_id"] = self.get_session_id()
        if token: kwargs["access_token"] = self.get_access_token()

    def get(self, url, auth = True, token = False, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.get,
            url,
            params = kwargs,
            auth_callback = self.auth_callback
        )

    def post(self, url, auth = True, token = False, data = None, data_j = None, data_m = None, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.post,
            url,
            params = kwargs,
            data = data,
            data_j = data_j,
            data_m = data_m,
            auth_callback = self.auth_callback
        )

    def put(self, url, auth = True, token = False, data = None, data_j = None, data_m = None, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.put,
            url,
            params = kwargs,
            data = data,
            data_j = data_j,
            data_m = data_m,
            auth_callback = self.auth_callback
        )

    def delete(self, url, auth = True, token = False, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.delete,
            url,
            params = kwargs,
            auth_callback = self.auth_callback
        )

    def get_session_id(self):
        if self.session_id: return self.session_id
        if self.mode == DIRECT_MODE: return self.login()
        elif self.mode == OAUTH_MODE: return self.oauth_session()

    def get_access_token(self):
        if self.access_token: return self.access_token
        if self.mode == DIRECT_MODE: return None
        raise errors.OAuthAccessError(
            "No access token found must re-authorize"
        )

    def auth_callback(self, params):
        if not self._has_mode(): raise errors.AccessError(
            "Session expired or authentication issues"
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
            auth = False,
            token = False,
            username = username,
            password = password
        )
        self.username = contents.get("username", None)
        self.acl = contents.get("acl", None)
        self.session_id = contents.get("session_id", None)
        self.tokens = self.acl.keys()
        self.trigger("auth", contents)
        return self.session_id

    def oauth_autorize(self):
        url = self.base_url + self.prefix + "oauth/authorize"
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )

        data = appier.urlencode(values)
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
        contents = self.get(url, auth = False, token = True)
        self.username = contents.get("username", None)
        self.acl = contents.get("acl", None)
        self.session_id = contents.get("session_id", None)
        self.tokens = self.acl.keys()
        self.trigger("auth", contents)
        return self.session_id

    def ping(self):
        return self.self_user()

    def _has_mode(self):
        return self.mode == DIRECT_MODE or self.mode == OAUTH_MODE

    def _get_mode(self):
        if self.username and self.password: return DIRECT_MODE
        elif self.client_id and self.client_secret: return OAUTH_MODE
        return UNSET_MODE
