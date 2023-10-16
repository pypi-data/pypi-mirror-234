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
Rattail model importer extensions, for CORE-POS integration
"""

import decimal

from rattail import importing
from rattail.util import pretty_quantity


##############################
# core importer overrides
##############################

class PersonImporter(importing.model.PersonImporter):

    extensions = {
        '_corepos': [
            'corepos_customer_id',
        ],
    }

    def cache_query(self):
        query = super(PersonImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore people with no CORE ID, if that's (part of) our key
        if 'corepos_customer_id' in self.key:
            query = query.join(model.CorePerson)\
                         .filter(model.CorePerson.corepos_customer_id != None)

        return query


class EmployeeImporter(importing.model.EmployeeImporter):

    extensions = {
        '_corepos': [
            'corepos_number',
        ],
    }


class CustomerImporter(importing.model.CustomerImporter):

    extensions = {
        '_corepos': [
            'corepos_account_id',
            'corepos_card_number',
        ],
    }


class CustomerShopperImporter(importing.model.CustomerShopperImporter):

    extensions = {
        '_corepos': [
            'corepos_customer_id',
        ],
    }


class MemberImporter(importing.model.MemberImporter):

    extensions = {
        '_corepos': [
            'corepos_account_id',
        ],
    }


class MemberEquityPaymentImporter(importing.model.MemberEquityPaymentImporter):

    extensions = {
        '_corepos': [
            'corepos_card_number',
            'corepos_transaction_number',
            'corepos_transaction_id',
            'corepos_department_number',
            'corepos_datetime',
        ],
    }


class StoreImporter(importing.model.StoreImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }


class DepartmentImporter(importing.model.DepartmentImporter):

    extensions = {
        '_corepos': [
            'corepos_number',
        ],
    }


class SubdepartmentImporter(importing.model.SubdepartmentImporter):

    extensions = {
        '_corepos': [
            'corepos_number',
        ],
    }


class TaxImporter(importing.model.TaxImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }


class TenderImporter(importing.model.TenderImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }


class VendorImporter(importing.model.VendorImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }


class ProductImporter(importing.model.ProductImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }

    def setup(self):
        super(ProductImporter, self).setup()

        if self.fields_active(self.size_fields):
            app = self.config.get_app()
            handler = app.get_products_handler()
            self.uoms = handler.get_uom_sil_codes(self.session, uppercase=True)

    def cache_query(self):
        query = super(ProductImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore products with no CORE ID, if that's (part of) our key
        if 'corepos_id' in self.key:
            query = query.join(model.CoreProduct)\
                         .filter(model.CoreProduct.corepos_id != None)

        return query

    def get_uom_code(self, uom):
        if hasattr(self, 'uoms'):
            return self.uoms.get(uom.upper())

        app = self.config.get_app()
        handler = app.get_products_handler()
        return handler.get_uom_sil_code(self.session, uom.upper())

    def normalize_size_info(self, core_product):

        # convert product to dict if needed
        if isinstance(core_product, dict):
            core_data = core_product
        else:
            core_data = {
                'size': core_product.size,
                'unitofmeasure': core_product.unit_of_measure,
            }

        unit_size = None
        if 'size' in core_data and core_data['size'] is not None:
            try:
                unit_size = decimal.Decimal(core_data['size'])
            except decimal.InvalidOperation:
                pass

        uom_abbrev = core_data.get('unitofmeasure')

        uom_code = self.enum.UNIT_OF_MEASURE_NONE
        if uom_abbrev is not None:
            uom_code = self.get_uom_code(uom_abbrev) or self.enum.UNIT_OF_MEASURE_NONE

        if unit_size is not None and uom_abbrev is not None:
            size = "{} {}".format(pretty_quantity(unit_size), uom_abbrev)
        elif unit_size is not None:
            size = pretty_quantity(unit_size)
        elif uom_abbrev is not None:
            size = uom_abbrev
        else:
            size = None

        return {
            'size': size,
            'unit_size': unit_size,
            'uom_abbrev': uom_abbrev,
            'uom_code': uom_code,
        }


class ProductCostImporter(importing.model.ProductCostImporter):

    extensions = {
        '_corepos': [
            'corepos_id',
        ],
    }

    def cache_query(self):
        query = super(ProductCostImporter, self).cache_query()
        model = self.config.get_model()

        # we want to ignore items with no CORE ID, if that's (part of) our key
        if 'corepos_id' in self.key:
            query = query.join(model.CoreProductCost)\
                         .filter(model.CoreProductCost.corepos_id != None)

        return query
