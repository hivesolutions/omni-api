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


class ExportAPI(object):

    def export_schema(self):
        url = self.base_url + "omni/export/schema.json"
        contents = self.get(url)
        return contents

    def export_changes(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/export/changes.json"
        contents = self.get(url, **kwargs)
        return contents

    def export_digests(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/export/digests.json"
        contents = self.get(url, **kwargs)
        return contents

    def export_entities(self, entity, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/export/%s.json" % entity
        contents = self.get(url, **kwargs)
        return contents

    def export_totals(self, entity, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/export/%s/totals.json" % entity
        contents = self.get(url, **kwargs)
        return contents


class ExportIdentifier(dict):
    pass


class ExportField(dict):
    pass


class ExportRelation(dict):
    pass


class ExportEntity(dict):
    pass


class ExportSchema(dict):
    pass


class ExportCursor(dict):
    pass


class ExportChanges(dict):
    pass


class ExportRange(dict):
    pass


class ExportDigests(dict):
    pass


class ExportPairs(dict):
    pass


class ExportEntityCursor(dict):
    pass


class ExportEntities(dict):
    pass


class ExportTotals(dict):
    pass
