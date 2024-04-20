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

from typing import Sequence

from .base import Base, BaseDelta

class SaftPtReport(Base):
    _version: str
    fiscal_year: int
    start_date: float
    end_date: float

class SaftPtReportDelta(BaseDelta):
    _version: str
    fiscal_year: int
    start_date: float
    end_date: float

class SaftPtReportPayload(BaseDelta):
    saft_pt_report: SaftPtReportDelta

class SaftPtAPI(object):
    def list_saft_pt(self, *args, **kwargs) -> Sequence[SaftPtReport]: ...
    def create_saft_pt(self, payload: SaftPtReportPayload) -> SaftPtReport: ...
    def get_saft_pt(self, object_id: int) -> SaftPtReport: ...
    def file_saft_pt(self, object_id: int) -> bytes: ...
    def file_decompressed_saft_pt(self, object_id: int) -> bytes: ...
