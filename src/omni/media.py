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

import base64

import appier

from . import util


class MediaAPI(object):

    def list_media(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/media.json"
        contents = self.get(url, **kwargs)
        return contents

    def info_media(self, object_id):
        url = self.base_url + "omni/media/%d/info.json" % object_id
        contents = self.get(url)
        return contents

    def update_media(self, object_id, payload):
        self._wrap_data(payload)
        url = self.base_url + "omni/media/%d/update.json" % object_id
        contents = self.post(url, data_j=payload)
        return contents

    def delete_media(self, object_id):
        url = self.base_url + "omni/media/%d/delete.json" % object_id
        contents = self.post(url)
        return contents

    def get_media_url(self, secret, size="original"):
        return self.open_url + "omni/media/%s" % secret

    def _wrap_data(self, payload):
        if not "data" in payload:
            return
        data = payload["data"]
        data_b64 = base64.b64encode(data)
        data_b64 = appier.legacy.str(data_b64)
        payload["data_b64"] = data_b64
        del payload["data"]
