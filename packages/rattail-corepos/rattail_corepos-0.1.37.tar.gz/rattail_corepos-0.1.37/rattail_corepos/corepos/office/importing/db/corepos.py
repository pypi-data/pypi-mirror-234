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
CORE-POS -> CORE-POS data import
"""

from collections import OrderedDict

from corepos.db.office_op import Session as CoreSession

from rattail.importing.handlers import FromSQLAlchemyHandler
from rattail.importing.sqlalchemy import FromSQLAlchemySameToSame
from rattail_corepos.corepos.office.importing import db as corepos_importing


class FromCoreHandler(FromSQLAlchemyHandler):
    """
    Base class for import handlers which use a CORE database as the host / source.
    """
    host_title = "CORE"
    host_key = 'corepos_db_office_op'

    def make_host_session(self):
        return CoreSession()


# TODO: deprecate / remove this
ToCoreHandler = corepos_importing.model.ToCoreHandler


class FromCoreToCoreBase(object):
    """
    Common base class for Core -> Core data import/export handlers.
    """

    def get_importers(self):
        importers = OrderedDict()
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Vendor'] = VendorImporter
        importers['VendorContact'] = VendorContactImporter
        importers['Product'] = ProductImporter
        importers['ProductFlag'] = ProductFlagImporter
        importers['VendorItem'] = VendorItemImporter
        importers['Employee'] = EmployeeImporter
        importers['CustomerClassic'] = CustomerClassicImporter
        importers['MemberType'] = MemberTypeImporter
        importers['MemberInfo'] = MemberInfoImporter
        importers['HouseCoupon'] = HouseCouponImporter
        return importers


class FromCoreToCoreImport(FromCoreToCoreBase, FromCoreHandler, corepos_importing.model.ToCoreHandler):
    """
    Handler for CORE (other) -> CORE (local) data import.

    .. attribute:: direction

       Value is ``'import'`` - see also
       :attr:`rattail.importing.handlers.ImportHandler.direction`.
    """
    dbkey = 'host'
    local_title = "CORE (default)"

    @property
    def host_title(self):
        return "CORE ({})".format(self.dbkey)

    def make_host_session(self):
        return CoreSession(bind=self.config.corepos_engines[self.dbkey])


class FromCoreToCoreExport(FromCoreToCoreBase, FromCoreHandler, corepos_importing.model.ToCoreHandler):
    """
    Handler for CORE (local) -> CORE (other) data export.

    .. attribute:: direction

       Value is ``'export'`` - see also
       :attr:`rattail.importing.handlers.ImportHandler.direction`.
    """
    direction = 'export'
    host_title = "CORE (default)"

    @property
    def local_title(self):
        return "CORE ({})".format(self.dbkey)

    def make_session(self):
        return CoreSession(bind=self.config.corepos_engines[self.dbkey])


class FromCore(FromSQLAlchemySameToSame):
    """
    Base class for CORE -> CORE data importers.
    """


class DepartmentImporter(FromCore, corepos_importing.model.DepartmentImporter):
    pass

class SubdepartmentImporter(FromCore, corepos_importing.model.SubdepartmentImporter):
    pass

class VendorImporter(FromCore, corepos_importing.model.VendorImporter):
    pass

class VendorContactImporter(FromCore, corepos_importing.model.VendorContactImporter):
    pass

class ProductImporter(FromCore, corepos_importing.model.ProductImporter):
    pass

class ProductFlagImporter(FromCore, corepos_importing.model.ProductFlagImporter):
    pass

class VendorItemImporter(FromCore, corepos_importing.model.VendorItemImporter):
    pass

class EmployeeImporter(FromCore, corepos_importing.model.EmployeeImporter):
    pass

class CustomerClassicImporter(FromCore, corepos_importing.model.CustomerClassicImporter):
    pass

class MemberTypeImporter(FromCore, corepos_importing.model.MemberTypeImporter):
    pass

class MemberInfoImporter(FromCore, corepos_importing.model.MemberInfoImporter):
    pass

class HouseCouponImporter(FromCore, corepos_importing.model.HouseCouponImporter):
    pass
