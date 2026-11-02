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


class UserAPI(object):

    def list_users(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/users.json"
        contents = self.get(url, **kwargs)
        return contents

    def create_user(self, payload):
        url = self.base_url + "omni/users.json"
        contents = self.post(url, data_j=payload)
        return contents

    def get_user(self, object_id):
        url = self.base_url + "omni/users/%d.json" % object_id
        contents = self.get(url)
        return contents

    def self_user(self):
        url = self.base_url + "omni/users/self.json"
        contents = self.get(url)
        return contents

    def get_acl_user(self, object_id):
        url = self.base_url + "omni/users/%d/acl.json" % object_id
        contents = self.get(url)
        return contents

    def list_acl_entries_user(self, object_id):
        url = self.base_url + "omni/users/%d/acl_entries.json" % object_id
        contents = self.get(url)
        return contents

    def add_acl_entry_user(self, object_id, name, value=None):
        data_j = dict(name=name)
        if not value == None:
            data_j["value"] = value
        url = self.base_url + "omni/users/%d/acl_entries/add.json" % object_id
        contents = self.post(url, data_j=data_j)
        return contents

    def remove_acl_entry_user(self, object_id, name, value=None):
        data_j = dict(name=name)
        if not value == None:
            data_j["value"] = value
        url = self.base_url + "omni/users/%d/acl_entries/remove.json" % object_id
        contents = self.post(url, data_j=data_j)
        return contents

    def list_roles_user(self, object_id):
        url = self.base_url + "omni/users/%d/roles.json" % object_id
        contents = self.get(url)
        return contents

    def add_role_user(self, object_id, role_id):
        url = self.base_url + "omni/users/%d/roles/add.json" % object_id
        contents = self.post(url, data_j=dict(role_id=role_id))
        return contents

    def remove_role_user(self, object_id, role_id):
        url = self.base_url + "omni/users/%d/roles/remove.json" % object_id
        contents = self.post(url, data_j=dict(role_id=role_id))
        return contents


class UserType(object):
    OWNER = 1
    ADMIN = 2
    USER = 3
    ADVANCED = 4
    OBSERVER = 5
    UNDEFINED = 6


class AclValue(object):
    ALLOW = 10
    VALIDATE = 20
    DENY = 30


class BaseUser(dict):
    pass


class User(dict):
    pass


class UserParameters(dict):
    pass


class BaseUserDelta(dict):
    pass


class UserDelta(dict):
    pass


class UserPayload(dict):
    pass
