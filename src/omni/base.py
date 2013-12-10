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

import urllib

import appier

import errors

BASE_URL = "https://ldj.frontdoorhd.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

CLIENT_ID = None

CLIENT_SECRET = None

REDIRECT_URL = "http://localhost:8080/oauth"

SCOPE = (
    "base",
    "base.user",
    "base.admin",
    "foundation.store.list"
)
""" The list of permission to be used to create the
scope string for the oauth value """

class Api(object):

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.prefix = kwargs.get("prefix", "adm/")
        self.client_id = kwargs.get("client_id", CLIENT_ID)
        self.client_secret = kwargs.get("client_secret", CLIENT_SECRET)
        self.redirect_url = kwargs.get("redirect_url", REDIRECT_URL)
        self.scope = kwargs.get("scope", SCOPE)
        self.access_token = kwargs.get("access_token", None)
        self.session_id = kwargs.get("session_id", None)
        self.username = kwargs.get("username", None)
        self.acl = kwargs.get("acl", None)
        self.tokens = kwargs.get("tokens", None)

    def request(self, method, *args, **kwargs):
        try:
            result = method(*args, **kwargs)
        except appier.HTTPError, exception:
            print exception.read_json()
            raise errors.OAuthAccessError(
                "Problems using access token found must re-authorize"
            )

        return result

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

    def post(self, url, auth = True, token = False, data = None, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.post,
            url,
            params = kwargs,
            data = data,
            auth_callback = self.auth_callback
        )

    def put(self, url, auth = True, token = False, data = None, **kwargs):
        self.build_kwargs(kwargs, auth = auth, token = token)
        return self.request(
            appier.put,
            url,
            params = kwargs,
            data = data,
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
        return self.oauth_session()

    def get_access_token(self):
        if self.access_token: return self.access_token
        raise errors.OAuthAccessError(
            "No access token found must re-authorize"
        )

    def auth_callback(self, params):
        session_id = self.oauth_session()
        params["session_id"] = session_id

    def login(self):
        pass

    def list_stores(self, filter = "", start = 0, count = 10):
        url = self.base_url + "omni/stores.json"
        contents_s = self.get(
            url,
            filter_string = filter,
            start_record = start,
            number_records = count
        )
        return contents_s

    def oauth_autorize(self):
        url = self.base_url + self.prefix + "oauth/authorize"
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )

        data = urllib.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code):
        url = self.base_url + "omni/oauth/access_token"
        contents_s = self.post(
            url,
            auth = False,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "authorization_code",
            redirect_uri = self.redirect_url,
            code = code
        )
        self.access_token = contents_s["access_token"]
        return self.access_token

    def oauth_session(self):
        url = self.base_url + "omni/oauth/start_session"
        contents_s = self.get(url, auth = False, token = True)
        self.username = contents_s.get("username", None)
        self.acl = contents_s.get("acl", None)
        self.session_id = contents_s.get("session_id", None)
        self.tokens = self.acl.keys()
        return self.session_id
