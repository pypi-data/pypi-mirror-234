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
CORE Office -> CORE Lane import
"""

from collections import OrderedDict

from corepos.db.office_op import Session as CoreOfficeSession, model as coreoffice
from corepos.db.lane_op import Session as CoreLaneSession

from rattail import importing
from rattail.importing.handlers import FromSQLAlchemyHandler, ToSQLAlchemyHandler
from rattail_corepos.corepos.lane.importing import op as corepos_importing


# TODO: this surely belongs in some other/common place? (is not lane-specific)
class FromCoreOfficeHandler(FromSQLAlchemyHandler):
    """
    Base class for import handlers which use CORE Office as the host.
    """
    host_key = 'corepos_db_office_op'
    generic_host_title = 'CORE Office (DB "op")'
    host_title = "CORE Office"

    def make_host_session(self):
        return CoreOfficeSession()


# TODO: this surely belongs in some other/common place? (is not office-specific)
class ToCoreLaneHandler(ToSQLAlchemyHandler):
    """
    Base class for import handlers which target CORE Lane on the local side.
    """
    local_title = "CORE Lane"
    local_key = 'corepos_db_lane_op'
    generic_local_title = 'CORE Lane (DB "op")'

    def make_session(self):
        return CoreLaneSession()


class FromCoreOfficeToCoreLane(FromCoreOfficeHandler, ToCoreLaneHandler):
    """
    Handler for CORE Office -> CORE Lane data export.
    """
    direction = 'export'
    dbkey = 'default'

    @property
    def local_title(self):
        return "CORE Lane ({})".format(self.dbkey)

    def make_session(self):
        return CoreLaneSession(bind=self.config.core_lane_op_engines[self.dbkey])

    def get_importers(self):
        importers = OrderedDict()
        importers['Department'] = DepartmentImporter
        importers['Product'] = ProductImporter
        importers['CustomerClassic'] = CustomerClassicImporter
        return importers


class FromCore(importing.FromSQLAlchemy):
    """
    Base class for CORE Office -> CORE Lane data importers.
    """


class DepartmentImporter(FromCore, corepos_importing.model.DepartmentImporter):
    host_model_class = coreoffice.Department

    # these fields are held in common, between Office and Lane tables
    common_fields = [
        'number',
        'name',
        'tax',
        'food_stampable',
        'limit',
        'minimum',
        'discount',
        'see_id',
        'modified',
        'modified_by_id',
        'margin',
        'sales_code',
        'member_only',
        # TODO: these seem to be newer additions?
        # 'line_item_discount',
        # 'wicable',
    ]

    @property
    def supported_fields(self):
        return self.common_fields

    def normalize_host_object(self, department):
        data = dict([(field, getattr(department, field))
                     for field in self.common_fields])
        return data


class ProductImporter(FromCore, corepos_importing.model.ProductImporter):
    host_model_class = coreoffice.Product

    # these fields are held in common, between Office and Lane tables
    common_fields = [
        'id',
        'upc',
        'description',
        'brand',
        'formatted_name',
        'normal_price',
        'price_method',
        'group_price',
        'quantity',
        'special_price',
        'special_price_method',
        'special_group_price',
        'special_quantity',
        # 'special_limit',
        'start_date',
        'end_date',
        'department_number',
        'size',
        'tax_rate_id',
        'foodstamp',
        'scale',
        'scale_price',
        'mix_match_code',
        # 'created',
        # 'modified',

        # TODO: what to do about this 'replaces' thing?
        # 'batchID'=>array('type'=>'TINYINT', 'replaces'=>'advertised'),
        # batch_id = sa.Column('batchID', sa.SmallInteger(), nullable=True)
        # advertised = sa.Column(sa.Boolean(), nullable=True)

        'tare_weight',
        'discount',
        'discount_type',
        'line_item_discountable',
        'unit_of_measure',
        'wicable',
        'quantity_enforced',
        'id_enforced',
        'cost',
        # 'special_cost',
        # 'received_cost',
        'in_use',
        'flags',
        'subdepartment_number',
        'deposit',
        'local',
        'store_id',
        'default_vendor_id',
        'current_origin_id',
        # 'auto_par',
        # 'price_rule_id',
        'last_sold',
    ]

    @property
    def supported_fields(self):
        return self.common_fields

    def normalize_host_object(self, product):
        data = dict([(field, getattr(product, field))
                     for field in self.common_fields])
        return data


class CustomerClassicImporter(FromCore, corepos_importing.model.CustomerClassicImporter):
    host_model_class = coreoffice.CustomerClassic

    # these fields are held in common, between Office and Lane tables
    common_fields = [
        'id',
        'card_number',
        'person_number',
        'first_name',
        'last_name',
        'cash_back',
        'balance',
        'discount',
        'member_discount_limit',
        'charge_limit',
        'charge_ok',
        'write_checks',
        'store_coupons',
        'type',
        'member_type_id',
        'staff',
        'ssi',
        'purchases',
        'number_of_checks',
        'member_coupons',
        'blue_line',
        'shown',
        'last_change',
    ]

    @property
    def supported_fields(self):
        return self.common_fields

    def normalize_host_object(self, custdata):
        data = dict([(field, getattr(custdata, field))
                     for field in self.common_fields])
        return data
