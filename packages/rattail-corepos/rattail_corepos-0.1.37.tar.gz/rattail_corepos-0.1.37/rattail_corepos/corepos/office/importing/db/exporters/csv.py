# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE-POS Data Export
"""

from corepos.db.office_op import model as corepos

from rattail.importing.handlers import ToCSVHandler
from rattail.importing.exporters import FromSQLAlchemyToCSVMixin
from rattail_corepos.corepos.office.importing.db.corepos import FromCoreHandler, FromCore


class FromCoreToCSV(FromSQLAlchemyToCSVMixin, FromCoreHandler, ToCSVHandler):
    """
    Handler for CORE -> CSV data export.
    """
    direction = 'export'
    local_title = "CSV"
    FromParent = FromCore
    ignored_model_names = ['Change'] # omit the datasync change model

    @property
    def host_title(self):
        return self.config.node_title(default="CORE")

    def get_model(self):
        return corepos
