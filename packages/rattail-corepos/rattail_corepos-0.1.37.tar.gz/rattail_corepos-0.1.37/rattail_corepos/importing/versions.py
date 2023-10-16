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
Rattail -> Rattail "versions" data import
"""

from rattail.importing import versions as base


class CoreposVersionMixin(object):
    """
    Add default registration of custom importers
    """

    def add_corepos_importers(self, importers):
        importers['CorePerson'] = CorePersonImporter
        importers['CoreEmployee'] = CoreEmployeeImporter
        importers['CoreCustomer'] = CoreCustomerImporter
        importers['CoreCustomerShopper'] = CoreCustomerShopperImporter
        importers['CoreMember'] = CoreMemberImporter
        importers['CoreMemberEquityPayment'] = CoreMemberEquityPaymentImporter
        importers['CoreStore'] = CoreStoreImporter
        importers['CoreDepartment'] = CoreDepartmentImporter
        importers['CoreSubdepartment'] = CoreSubdepartmentImporter
        importers['CoreVendor'] = CoreVendorImporter
        importers['CoreProduct'] = CoreProductImporter
        return importers


class CorePersonImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CorePerson


class CoreEmployeeImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreEmployee


class CoreCustomerImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreCustomer


class CoreCustomerShopperImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        return self.model.CoreCustomerShopper


class CoreMemberImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreMember


class CoreMemberEquityPaymentImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreMemberEquityPayment


class CoreStoreImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreStore


class CoreDepartmentImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreDepartment


class CoreSubdepartmentImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreSubdepartment


class CoreVendorImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreVendor


class CoreProductImporter(base.VersionImporter):

    @property
    def host_model_class(self):
        model = self.config.get_model()
        return model.CoreProduct
