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

class ApiError(RuntimeError):
    pass

class AccessError(ApiError):
    pass

class OAuthAccessError(ApiError):
    pass

class OmniError(ApiError):

    def __init__(self, error, exception = {}):
        ApiError.__init__(self)
        self.error = error
        self.exception = exception

    def __str__(self):
        return self.full_message()

    def __unicode__(self):
        return appier.UNICODE(self.full_message())

    def name(self):
        return self.exception.get("exception_name", "Undefined")

    def message(self):
        return self.exception.get("message", "Undefined message")

    def full_message(self):
        message = self.message()
        name = self.name()
        return "%s - %s" % (name, message) if name else message

    def traceback(self):
        return self.exception.get("traceback", None)
