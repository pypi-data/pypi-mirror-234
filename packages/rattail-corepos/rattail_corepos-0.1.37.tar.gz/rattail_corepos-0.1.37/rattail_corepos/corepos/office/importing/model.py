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
CORE-POS model importers (webservices API)
"""

from rattail import importing
from rattail.util import data_diffs
from rattail_corepos.corepos.util import get_core_members


class ToCOREAPIHandler(importing.ImportHandler):
    """
    Base class for handlers targeting the CORE API.
    """
    local_key = 'corepos_api'
    generic_local_title = "CORE Office (API)"

    @property
    def local_title(self):
        return "CORE-POS (API)"

    def process_changes(self, changes):

        if 'Member' in changes:
            member_changes = changes['Member']
            member_importer = self.importers['Member']
            created, updated, deleted = changes['Member']
            if updated:

                # explode the 'customers' field so email will show
                # diffs for each subrecord field
                for update in updated:
                    local_object, local_data, host_data = update

                    local_customers = local_data.pop('customers')
                    for i, customer in enumerate(local_customers, 1):
                        for key in customer:
                            local_data[f'customers.{i}.{key}'] = customer[key]

                    host_customers = host_data.pop('customers')
                    for i, customer in enumerate(host_customers, 1):
                        for key in customer:
                            host_data[f'customers.{i}.{key}'] = customer[key]

        # do normal logic for the rest
        super().process_changes(changes)


class ToCoreAPI(importing.Importer):
    """
    Base class for all CORE "operational" model importers, which use the API.
    """
    # TODO: these importers are in a bit of an experimental state at the
    # moment.  we only allow create/update b/c it will use the API instead of
    # direct DB
    allow_delete = False

    caches_local_data = True

    def setup(self):
        self.establish_api()

    def establish_api(self):
        self.api = self.app.get_corepos_handler().make_webapi()

    def ensure_fields(self, data):
        """
        Ensure each of our supported fields are included in the data.  This is
        to handle cases where the API does not return all fields, e.g. when
        some of them are empty.
        """
        for field in self.fields:
            if field not in data:
                data[field] = None

    def fix_empties(self, data, fields):
        """
        Fix "empty" values for the given set of fields.  This just uses an
        empty string instead of ``None`` for each, to add some consistency
        where the API might lack it.

        Main example so far, is the Vendor API, which may not return some
        fields at all (and so our value is ``None``) in some cases, but in
        other cases it *will* return a value, default of which is the empty
        string.  So we want to "pretend" that we get an empty string back even
        when we actually get ``None`` from it.
        """
        for field in fields:
            if data[field] is None:
                data[field] = ''


class MemberImporter(ToCoreAPI):
    """
    Member model importer for CORE-POS
    """
    model_name = 'Member'
    key = 'cardNo'
    supported_fields = [
        'cardNo'
        'customerAccountID',
        'customers',
        # 'memberStatus',
        # 'activeStatus',
        # 'customerTypeID',
        # 'chargeBalance',
        # 'chargeLimit',
        # 'idCardUPC',
        'startDate',
        'endDate',
        'addressFirstLine',
        'addressSecondLine',
        'city',
        'state',
        'zip',
        # 'contactAllowed',
        # 'contactMethod',
        # 'modified',
    ]
    supported_customer_fields = [
        'customerID',
        # 'customerAccountID',
        # 'cardNo',
        'firstName',
        'lastName',
        # 'chargeAllowed',
        # 'checksAllowed',
        # 'discount',
        'accountHolder',
        # 'staff',
        'phone',
        'altPhone',
        'email',
        # 'memberPricingAllowed',
        # 'memberCouponsAllowed',
        # 'lowIncomeBenefits',
        # 'modified',
    ]

    #empty_date_value = '0000-00-00 00:00:00'
    empty_date_value = '1900-01-01 00:00:00'

    def get_local_objects(self, host_data=None):
        return get_core_members(self.config, self.api, progress=self.progress)

    def get_single_local_object(self, key):
        assert len(self.key) == 1
        assert self.key[0] == 'cardNo'
        return self.api.get_member(key[0])

    def normalize_local_object(self, member):
        data = dict(member)
        return data

    def data_diffs(self, local_data, host_data):
        diffs = super(MemberImporter, self).data_diffs(local_data, host_data)

        # the 'customers' field requires a more granular approach, since the
        # data coming from API may have different fields than our local data
        if 'customers' in self.fields and 'customers' in diffs:
            if not self.customer_data_differs(local_data, host_data):
                diffs.remove('customers')

        # # also the start/end dates should be looked at more closely.  if they
        # # contain the special '__omit__' value then we won't ever count as diff
        # if 'startDate' in self.fields and 'startDate' in diffs:
        #     if host_data['startDate'] == '__omit__':
        #         diffs.remove('startDate')
        # if 'endDate' in self.fields and 'endDate' in diffs:
        #     if host_data['endDate'] == '__omit__':
        #         diffs.remove('endDate')

        return diffs

    def customer_data_differs(self, local_data, host_data):
        local_customers = local_data['customers']
        host_customers = host_data['customers']

        # if both are empty, we're good
        if not local_customers and not host_customers:
            return False

        # obviously we differ if record count doesn't match
        if len(local_customers) != len(host_customers):
            return True

        # okay then, let's traverse the "new" list
        for host_customer in host_customers:

            # we differ if can't locate corresponding "old" local record
            local_customer = self.find_local_customer(local_customers, host_customer)
            if not local_customer:
                return True

            # we differ if old and new records differ, but...
            diffs = data_diffs(local_customer, host_customer,
                               fields=self.supported_customer_fields)

            # nb. the customerID field is sometimes int, sometimes str
            # (?)  so we must coerce both sides to str for proper
            # comparison, otherwise false diffs happen
            if diffs and (
                    diffs != ['customerID']
                    or str(local_customer['customerID']) != str(host_customer['customerID'])):
                return True

        # okay, now let's traverse the "old" list
        for local_customer in local_customers:

            # we differ if can't locate corresponding "new" host record
            host_customer = self.find_host_customer(host_customers, local_customer)
            if not host_customer:
                return True

        # guess we don't differ after all
        return False

    def find_local_customer(self, local_customers, host_customer):
        assert 'customerID' in self.supported_customer_fields

        if not host_customer['customerID']:
            return              # new customer

        for local_customer in local_customers:
            if str(local_customer['customerID']) == str(host_customer['customerID']):
                return local_customer

    def find_host_customer(self, host_customers, local_customer):
        assert 'customerID' in self.supported_customer_fields

        for host_customer in host_customers:
            if str(host_customer['customerID']) == str(local_customer['customerID']):
                return host_customer

    def create_object(self, key, data):
        # we can get away with using the same logic for both here
        return self.update_object(None, data)

    def update_object(self, member, data, local_data=None):
        """
        Push an update for the member, via the CORE API.
        """
        if self.dry_run:
            return data

        cardNo = data.pop('cardNo')
        # data = dict(data)
        # if data.get('startDate') == '__omit__':
        #     data.pop('startDate')
        # if data.get('endDate') == '__omit__':
        #     data.pop('endDate')
        member = self.api.set_member(cardNo, **data)
        return member


class DepartmentImporter(ToCoreAPI):
    """
    Department model importer for CORE-POS
    """
    model_name = 'Department'
    key = 'dept_no'
    supported_fields = [
        'dept_no',
        'dept_name',
        # TODO: should enable some of these fields?
        # 'dept_tax',
        # 'dept_fs',
        # 'dept_limit',
        # 'dept_minimum',
        # 'dept_discount',
        # 'dept_see_id',
        # 'modified',
        # 'modifiedby',
        # 'margin',
        # 'salesCode',
        # 'memberOnly',
    ]

    def get_local_objects(self, host_data=None):
        return self.api.get_departments()

    def get_single_local_object(self, key):
        assert len(self.key) == 1
        assert self.key[0] == 'dept_no'
        return self.api.get_department(key[0])

    def normalize_local_object(self, department):
        data = dict(department)
        return data

    def create_object(self, key, data):
        # we can get away with using the same logic for both here
        return self.update_object(None, data)

    def update_object(self, department, data, local_data=None):
        """
        Push an update for the department, via the CORE API.
        """
        if self.dry_run:
            return data

        dept_no = data.pop('dept_no')
        department = self.api.set_department(dept_no, **data)
        return department


class SubdepartmentImporter(ToCoreAPI):
    """
    Subdepartment model importer for CORE-POS
    """
    model_name = 'Subdepartment'
    key = 'subdept_no'
    supported_fields = [
        'subdept_no',
        'subdept_name',
        'dept_ID',
    ]

    def get_local_objects(self, host_data=None):
        return self.api.get_subdepartments()

    def get_single_local_object(self, key):
        assert len(self.key) == 1
        assert self.key[0] == 'subdept_no'
        return self.api.get_subdepartment(key[0])

    def normalize_local_object(self, subdepartment):
        data = dict(subdepartment)
        self.ensure_fields(data)
        return data

    def create_object(self, key, data):
        # we can get away with using the same logic for both here
        return self.update_object(None, data)

    def update_object(self, subdepartment, data, local_data=None):
        """
        Push an update for the subdepartment, via the CORE API.
        """
        if self.dry_run:
            return data

        subdept_no = data.pop('subdept_no')
        subdepartment = self.api.set_subdepartment(subdept_no, **data)
        return subdepartment


class VendorImporter(ToCoreAPI):
    """
    Vendor model importer for CORE-POS
    """
    model_name = 'Vendor'
    key = 'vendorID'
    supported_fields = [
        'vendorID',
        'vendorName',
        'vendorAbbreviation',
        'shippingMarkup',
        'discountRate',
        'phone',
        'fax',
        'email',
        'website',
        'address',
        'city',
        'state',
        'zip',
        'notes',
        'localOriginID',
        'inactive',
        'orderMinimum',
        'halfCases',
    ]

    def get_local_objects(self, host_data=None):
        return self.api.get_vendors()

    def get_single_local_object(self, key):
        assert len(self.key) == 1
        assert self.key[0] == 'vendorID'
        return self.api.get_vendor(key[0])

    def normalize_local_object(self, vendor):
        data = dict(vendor)

        # make sure all fields are present
        self.ensure_fields(data)

        # fix some "empty" values
        self.fix_empties(data, ['phone', 'fax', 'email'])

        # convert some values to native type
        data['discountRate'] = float(data['discountRate'])

        return data

    def create_object(self, key, data):
        # we can get away with using the same logic for both here
        return self.update_object(None, data)

    def update_object(self, vendor, data, local_data=None):
        """
        Push an update for the vendor, via the CORE API.
        """
        if self.dry_run:
            return data

        vendorID = data.pop('vendorID')
        vendor = self.api.set_vendor(vendorID, **data)
        return vendor


class ProductImporter(ToCoreAPI):
    """
    Product model importer for CORE-POS
    """
    model_name = 'Product'
    key = 'upc'
    supported_fields = [
        'upc',
        'brand',
        'description',
        'size',
        'department',
        'normal_price',
        'foodstamp',
        'scale',
        # 'tax',        # TODO!

        # TODO: maybe enable some of these fields?
        # 'formatted_name',
        # 'pricemethod',
        # 'groupprice',
        # 'quantity',
        # 'special_price',
        # 'specialpricemethod',
        # 'specialgroupprice',
        # 'specialquantity',
        # 'start_date',
        # 'end_date',
        # 'scaleprice',
        # 'mixmatchcode',
        # 'modified',
        # 'tareweight',
        # 'discount',
        # 'discounttype',
        # 'line_item_discountable',
        # 'unitofmeasure',
        # 'wicable',
        # 'qttyEnforced',
        # 'idEnforced',
        # 'cost',
        # 'inUse',
        # 'numflag',
        # 'subdept',
        # 'deposit',
        # 'local',
        # 'store_id',
        # 'default_vendor_id',
        # 'current_origin_id',
    ]

    def get_local_objects(self, host_data=None):
        return self.api.get_products()

    def get_single_local_object(self, key):
        assert len(self.key) == 1
        assert self.key[0] == 'upc'
        return self.api.get_product(key[0])

    def normalize_local_object(self, product):
        data = dict(product)

        # make sure all fields are present
        self.ensure_fields(data)

        # fix some "empty" values
        self.fix_empties(data, ['brand'])

        return data

    def create_object(self, key, data):
        # we can get away with using the same logic for both here
        return self.update_object(None, data)

    def update_object(self, product, data, local_data=None):
        """
        Push an update for the product, via the CORE API.
        """
        if self.dry_run:
            return data

        upc = data.pop('upc')
        product = self.api.set_product(upc, **data)
        return product
