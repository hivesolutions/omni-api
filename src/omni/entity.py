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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

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

import base64

import appier

from . import util

class EntityAPI(object):

    def list_entities(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/entities.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def get_entity(self, object_id):
        url = self.base_url + "omni/entities/%d.json" % object_id
        contents = self.get(url)
        return contents

    def update_entity(self, id, payload):
        url = self.base_url + "omni/entities/%d/update.json" % id
        contents = self.post(url, data_j = payload)
        return contents

    def sequence_entity(self, object_id):
        url = self.base_url + "omni/entities/%d/sequence.json" % object_id
        contents = self.get(url)
        return contents

    def media_entity(
        self,
        object_id,
        position = None,
        dimensions = None,
        label = None
    ):
        url = self.base_url + "omni/entities/%d/media.json" % object_id
        contents = self.get(
            url,
            position = position,
            dimensions = dimensions,
            label = label
        )
        return contents

    def public_media_entity(
        self,
        object_id,
        position = None,
        dimensions = None,
        label = None
    ):
        url = self.base_url + "omni/entities/%d/media/public.json" % object_id
        contents = self.get(
            url,
            position = position,
            dimensions = dimensions,
            label = label
        )
        return contents

    def info_media_entity(
        self,
        object_id,
        position = None,
        dimensions = None,
        label = None
    ):
        url = self.base_url + "omni/entities/%d/media/info.json" % object_id
        contents = self.get(
            url,
            position = position,
            dimensions = dimensions,
            label = label
        )
        return contents

    def set_media_entity(
        self,
        object_id,
        data,
        position = None,
        label = None,
        mime_type = None,
        width = None,
        height = None,
        dimensions = None,
        url = None,
        visibility = None,
        description = None,
        engine = None,
        thumbnails = None
    ):
        data_b64 = base64.b64encode(data)
        data_b64 = appier.legacy.str(data_b64)
        data_j = dict(
            data_b64 = data_b64,
            label = label,
            mime_type = mime_type,
            width = width,
            height = height,
            dimensions = dimensions,
            url = url,
            visibility = visibility,
            description = description
        )
        if not position == None: data_j["position"] = position
        if not engine == None: data_j["engine"] = engine
        if not thumbnails == None: data_j["thumbnails"] = thumbnails
        url = self.base_url + "omni/entities/%d/media/set.json" % object_id
        contents = self.post(url, data_j = data_j)
        return contents

    def clear_media_entity(self, object_id):
        url = self.base_url + "omni/entities/%d/media/clear.json" % object_id
        contents = self.post(url)
        return contents
