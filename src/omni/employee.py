#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from . import util

class EmployeeApi(object):

    def list_employees(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/employees.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def get_employee(self, object_id):
        url = self.base_url + "omni/employees/%d.json" % object_id
        contents = self.get(url)
        return contents

    def self_employee(self):
        url = self.base_url + "omni/employees/self.json"
        contents = self.get(url)
        return contents

    def stats_employee(
        self,
        date = None,
        unit = "month",
        span = 7,
        store_id = None,
        employee_id = None,
        has_global = None,
        output = "simple"
    ):
        url = self.base_url + "omni/employee_snapshots/stats.json"
        contents = self.get(
            url,
            date = date,
            unit = unit,
            span = span,
            store_id = store_id,
            employee_id = employee_id,
            has_global = has_global,
            output = output
        )
        return contents
