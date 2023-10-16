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
CORE-POS model importers (direct DB)

.. warning::
   All classes in this module are "direct DB" importers, which will write
   directly to MySQL.  They are meant to be used in dry-run mode only, and/or
   for sample data import to a dev system etc.  They are *NOT* meant for
   production use, as they will completely bypass any CORE business rules logic
   which may exist.
"""

import logging

from corepos.db.office_op import model as corepos, Session as CoreSession
from corepos.db.office_trans import model as coretrans, Session as CoreTransSession

from rattail import importing
from rattail.importing.handlers import ToSQLAlchemyHandler


log = logging.getLogger(__name__)


class ToCoreHandler(ToSQLAlchemyHandler):
    """
    Base class for import handlers which target a CORE database on the local side.
    """
    # TODO: should change local_key in all apps! since dbtype can vary now
    local_key = 'corepos_db_office_op'
    generic_local_title = "CORE Office (DB)"
    corepos_dbtype = 'office_op'
    corepos_dbkey = 'default'

    @property
    def local_title(self):
        dbtype = 'op'
        if self.corepos_dbtype == 'office_trans':
            dbtype = 'trans'
        return f"CORE Office (DB '{dbtype}')"

    def make_session(self):

        # session type depends on the --corepos-dbtype arg
        if self.corepos_dbtype == 'office_trans':
            return CoreTransSession(bind=self.config.coretrans_engines[self.corepos_dbkey])

        # assume office_op by default
        return CoreSession(bind=self.config.corepos_engines[self.corepos_dbkey])


class ToCore(importing.ToSQLAlchemy):
    """
    Base class for all CORE "operational" model importers.
    """

    def create_object(self, key, host_data):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return host_data

        return super(ToCore, self).create_object(key, host_data)

    def update_object(self, obj, host_data, **kwargs):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return obj

        return super(ToCore, self).update_object(obj, host_data, **kwargs)

    def delete_object(self, obj):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return True

        return super(ToCore, self).delete_object(obj)


class ToCoreTrans(importing.ToSQLAlchemy):
    """
    Base class for all CORE "transaction" model importers
    """


########################################
# CORE Operational
########################################

class DepartmentImporter(ToCore):
    model_class = corepos.Department
    key = 'number'


class SubdepartmentImporter(ToCore):
    model_class = corepos.Subdepartment
    key = 'number'


class VendorImporter(ToCore):
    model_class = corepos.Vendor
    key = 'id'


class VendorContactImporter(ToCore):
    model_class = corepos.VendorContact
    key = 'vendor_id'


class ProductImporter(ToCore):
    model_class = corepos.Product
    key = 'id'


class ProductFlagImporter(ToCore):
    model_class = corepos.ProductFlag
    key = 'bit_number'


class VendorItemImporter(ToCore):
    model_class = corepos.VendorItem
    key = ('sku', 'vendor_id')


class EmployeeImporter(ToCore):
    model_class = corepos.Employee
    key = 'number'


class CustomerClassicImporter(ToCore):
    model_class = corepos.CustomerClassic
    key = 'id'


class MemberTypeImporter(ToCore):
    model_class = corepos.MemberType
    key = 'id'


class MemberInfoImporter(ToCore):
    model_class = corepos.MemberInfo
    key = 'card_number'

    # default is to read first/last name directly from `meminfo`
    # table, but if this flag is set then names will be read from
    # `custdata` instead (where `personNum = 1`) although `meminfo`
    # will still be used as fallback in that case.
    prefer_local_names_from_custdata = False

    # default is to compare street address "as-is" between systems.
    # but CORE can be inconsistent with presence or lack of newline
    # suffix, when address is just one line (which is the typical
    # scenario).  so if this flag is set then importer will strip
    # whitespace automatically when reading this field value.
    strip_address_street = False

    # similar to previous flag, this one makes the importer strip
    # whitespace from *all* address fields when reading.
    strip_address_all = False

    # somewhat akin to the address flags, this one if set will cause
    # the importer to "normalize" phone numbers read from CORE.  the
    # assumption would be that the host/source side of the import
    # would also be presenting normalized phone data for comparison to
    # work correctly.  cf. AppHandler.normalize_phone_number()
    normalize_phone_numbers = False

    @property
    def supported_fields(self):
        fields = list(super(MemberInfoImporter, self).supported_fields)

        fields.append('member_type_id')

        return fields

    def normalize_local_object(self, member):
        data = super(MemberInfoImporter, self).normalize_local_object(member)

        if self.prefer_local_names_from_custdata and member.customers:
            customer = member.customers[0]
            data['first_name'] = customer.first_name
            data['last_name'] = customer.last_name

        if self.normalize_phone_numbers and 'phone' in self.fields:
            data['phone'] = self.app.normalize_phone_number(data['phone'])

        if ((self.strip_address_street or self.strip_address_all)
            and 'street' in self.fields):
            data['street'] = (data['street'] or '').strip()
        if self.strip_address_all and self.fields_active(['city', 'state', 'zip']):
            data['city'] = (data['city'] or '').strip()
            data['state'] = (data['state'] or '').strip()
            data['zip'] = (data['zip'] or '').strip()

        if 'member_type_id' in self.fields:
            data['member_type_id'] = None
            customer = member.customers[0] if member.customers else None
            if customer:
                data['member_type_id'] = customer.member_type_id

        return data

    def update_object(self, member, host_data, local_data=None, **kwargs):
        member = super(MemberInfoImporter, self).update_object(
            member, host_data, local_data=local_data, **kwargs)

        if 'first_name' in self.fields:
            if member.customers:
                customer = member.customers[0]
                first_name = host_data['first_name']
                if customer.first_name != first_name:
                    customer.first_name = first_name

        if 'last_name' in self.fields:
            if member.customers:
                customer = member.customers[0]
                last_name = host_data['last_name']
                if customer.last_name != last_name:
                    customer.last_name = last_name

        if 'member_type_id' in self.fields:
            member_type_id = host_data['member_type_id']
            for customer in member.customers:
                if customer.member_type_id != member_type_id:
                    if member_type_id is None:
                        log.warning("will not blank out member_type_id for "
                                    "member #%s: %s %s",
                                    member.card_number,
                                    customer.first_name,
                                    customer.last_name)
                    else:
                        customer.member_type_id = member_type_id

        return member


class MemberDateImporter(ToCore):
    model_class = corepos.MemberDate
    key = 'card_number'


class MemberContactImporter(ToCore):
    model_class = corepos.MemberContact
    key = 'card_number'


class HouseCouponImporter(ToCore):
    model_class = corepos.HouseCoupon
    key = 'coupon_id'


########################################
# CORE Transactions
########################################

class StockPurchaseImporter(ToCoreTrans):
    """
    CORE-POS stock purchase data importer.
    """
    model_class = coretrans.StockPurchase


class TransactionDetailImporter(ToCoreTrans):
    """
    CORE-POS transaction data importer.
    """
    model_class = coretrans.TransactionDetail
