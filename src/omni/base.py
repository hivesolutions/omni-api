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

BASE_URL = "https://ldj.frontdoorhd.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

CLIENT_ID = None

CLIENT_SECRET = None

REDIRECT_URL = "http://localhost:8080/oauth"

SCOPE = (
    "base",
    "base.user",
    "base.admin"
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
        self.access_token = None

    def get(self, url, authenticate = True, token = False, **kwargs):
        if authenticate: kwargs["session_id"] = self.session_id
        if token: kwargs["access_token"] = self.access_token
        return appier.get(url, **kwargs)

    def post(self, url, authenticate = True, token = False, **kwargs):
        if authenticate: kwargs["session_id"] = self.session_id
        if token: kwargs["access_token"] = self.access_token
        return appier.post(url, data_j = kwargs)

    def put(self, url, authenticate = True, token = False, **kwargs):
        if authenticate: kwargs["session_id"] = self.session_id
        if token: kwargs["access_token"] = self.access_token
        return appier.post(url, **kwargs)

    def delete(self, url, authenticate = True, token = False, **kwargs):
        if authenticate: kwargs["session_id"] = self.session_id
        if token: kwargs["access_token"] = self.access_token
        return appier.delete(url, **kwargs)

    def login(self):
        pass

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
            authenticate = False,
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
        pass
