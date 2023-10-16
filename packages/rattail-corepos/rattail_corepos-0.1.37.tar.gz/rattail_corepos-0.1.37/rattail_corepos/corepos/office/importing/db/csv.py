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
CSV -> CORE data import
"""

from corepos.db.office_op import model as corepos, Session as CoreSession

from rattail.importing.handlers import FromFileHandler
from rattail.importing.csv import FromCSVToSQLAlchemyMixin
from rattail_corepos.corepos.office.importing.db.model import ToCoreHandler, ToCore


class FromCSVToCore(FromCSVToSQLAlchemyMixin, FromFileHandler, ToCoreHandler):
    """
    Handler for CSV -> CORE data import
    """
    host_title = "CSV"
    ToParent = ToCore

    def get_model(self):
        return corepos

    def make_session(self):
        return CoreSession(bind=self.config.corepos_engines[self.dbkey])

    def get_default_keys(self):
        keys = super().get_default_keys()

        # error will occur for any missing files, when running for all
        # default models.  so make sure some of these are not default.
        if 'Change' in keys:
            keys.remove('Change')

        return keys
