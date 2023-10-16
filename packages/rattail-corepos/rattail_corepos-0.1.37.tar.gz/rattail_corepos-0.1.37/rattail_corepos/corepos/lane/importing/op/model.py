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
"operational" model importers for CORE Lane

.. warning::
   All classes in this module are "direct DB" importers, which will
   write directly to MySQL.  They are meant to be used in dry-run mode
   only, and/or for sample data import to a dev system etc.  They are
   *NOT* meant for production use, as they will completely bypass any
   CORE business rules logic which may exist.
"""

from rattail import importing
from rattail_corepos.corepos.common.importing import ToCore

from corepos.db.lane_op import model as corepos


class DepartmentImporter(ToCore):
    model_class = corepos.Department
    key = 'number'


class ProductImporter(ToCore):
    model_class = corepos.Product
    key = 'id'


class CustomerClassicImporter(ToCore):
    model_class = corepos.CustomerClassic
    key = 'id'
