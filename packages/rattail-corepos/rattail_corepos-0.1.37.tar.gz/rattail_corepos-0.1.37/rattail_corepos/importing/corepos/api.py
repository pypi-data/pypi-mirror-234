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
CORE POS (API) -> Rattail data importing
"""

import datetime
import decimal
import logging
from collections import OrderedDict

from sqlalchemy import orm

from rattail import importing
from rattail.gpc import GPC
from rattail.time import localtime, make_utc
from rattail.core import get_uuid
from rattail.db.util import normalize_full_name
from rattail_corepos import importing as corepos_importing
from rattail_corepos.corepos.util import get_core_members


log = logging.getLogger(__name__)


class FromCOREPOSToRattail(importing.ToRattailHandler):
    """
    Import handler for data coming from a CORE POS API.
    """
    host_key = 'corepos_api'
    generic_host_title = "CORE Office (API)"
    host_title = "CORE-POS (API)"
    safe_for_web_app = True

    def get_importers(self):
        importers = OrderedDict()
        importers['Customer'] = CustomerImporter
        importers['CustomerShopper'] = CustomerShopperImporter
        importers['MembershipType'] = MembershipTypeImporter
        importers['Member'] = MemberImporter
        importers['Store'] = StoreImporter
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Vendor'] = VendorImporter
        importers['Product'] = ProductImporter
        importers['ProductCost'] = ProductCostImporter
        importers['ProductMovement'] = ProductMovementImporter
        return importers

    def get_default_keys(self):
        keys = super(FromCOREPOSToRattail, self).get_default_keys()

        if 'ProductMovement' in keys:
            keys.remove('ProductMovement')
        return keys

    def get_core_members(self, api, progress=None):
        if not hasattr(self, 'cached_core_members'):
            self.cached_core_members = get_core_members(
                self.config, api, progress=progress)
        return self.cached_core_members


class FromCOREPOSAPI(importing.Importer):
    """
    Base class for all CORE POS API data importers.
    """

    def setup(self):
        super().setup()

        self.establish_api()

        self.ignore_new_members = self.should_ignore_new_members()

    def datasync_setup(self):
        super().datasync_setup()

        self.establish_api()

    def establish_api(self):
        self.api = self.app.get_corepos_handler().make_webapi()

    def should_ignore_new_members(self):
        if hasattr(self, 'ignore_new_members'):
            return self.ignore_new_members

        return self.config.getbool('rattail_corepos',
                                   'importing_ignore_new_members',
                                   default=False)

    def get_core_members(self):
        members = self.handler.get_core_members(self.api, progress=self.progress)

        # maybe ignore NEW MEMBER accounts
        if self.should_ignore_new_members():
            members = [member for member in members
                       if not self.is_new_member(member)]

        return members

    def is_new_member(self, member):
        """
        Convenience method to check if the given member represents a
        "NEW MEMBER" record in CORE-POS, and hence it should be
        ignored for the import.
        """
        customers = member['customers']
        if customers:
            customer = customers[0]
            if (not customer['firstName']
                and customer['lastName'] == 'NEW MEMBER'):
                return True
        return False


class CustomerImporter(FromCOREPOSAPI, corepos_importing.model.CustomerImporter):
    """
    Importer for customer data from CORE POS API.
    """
    key = 'corepos_card_number'
    supported_fields = [
        'corepos_card_number',
        'corepos_account_id',
        'number',
        'name',
        'address_street',
        'address_street2',
        'address_city',
        'address_state',
        'address_zipcode',
    ]

    def get_host_objects(self):
        return self.get_core_members()

    def normalize_host_object(self, member):
        card_number = int(member['cardNo'])

        # figure out the "account holder" customer for the member.  note that
        # we only use this to determine the `Customer.name` in Rattail
        customers = member['customers']
        account_holders = [customer for customer in customers
                           if customer['accountHolder']]
        if account_holders:
            if len(account_holders) > 1:
                log.warning("member %s has %s account holders in CORE: %s",
                            member['cardNo'], len(account_holders), member)
            customer = account_holders[0]
        elif customers:
            if len(customers) > 1:
                log.warning("member %s has %s customers but no account holders: %s",
                            member['cardNo'], len(customers), member)
            customer = customers[0]
        else:
            raise NotImplementedError("TODO: how to handle member with no customers?")

        data = {
            'corepos_card_number': card_number,
            'corepos_account_id': int(member['customerAccountID']),
            'number': card_number,
            'name': normalize_full_name(customer['firstName'],
                                        customer['lastName']),

            'address_street': member['addressFirstLine'] or None,
            'address_street2': member['addressSecondLine'] or None,
            'address_city': member['city'] or None,
            'address_state': member['state'] or None,
            'address_zipcode': member['zip'] or None,
        }

        return data


class CustomerShopperImporter(FromCOREPOSAPI, corepos_importing.model.CustomerShopperImporter):
    """
    Importer for customer shopper data from CORE POS API.
    """
    key = ('customer_uuid', 'shopper_number')
    supported_fields = [
        'customer_uuid',
        'shopper_number',
        'corepos_customer_id',
        'first_name',
        'last_name',
        'display_name',
        'active',
        'phone_number',
        'phone_number_2',
        'email_address',
        'account_holder',
    ]

    def setup(self):
        super().setup()
        model = self.model

        self.maxlen_phone_number = self.get_maxlen_phone_number()

        self.customers_by_card_number = self.app.cache_model(
            self.session,
            model.Customer,
            key='corepos_card_number',
            query_options=[orm.joinedload(model.Customer._corepos)])

    def get_maxlen_phone_number(self):
        if hasattr(self, 'maxlen_phone_number'):
            return self.maxlen_phone_number

        model = self.model
        return self.app.maxlen(model.PhoneNumber.number)

    def get_host_objects(self):

        # first get all member data from CORE API
        members = self.get_core_members()
        normalized = []

        # then collect all the "shopper" records
        def normalize(member, i):
            normalized.extend(self.get_shoppers_for_member(member))

        self.progress_loop(normalize, members,
                           message="Collecting Person data from CORE")
        return normalized

    def get_customer_by_card_number(self, card_number):
        if hasattr(self, 'customers_by_card_number'):
            return self.customers_by_card_number.get(card_number)

        model = self.model
        try:
            return self.session.query(model.Customer)\
                               .join(model.CoreCustomer)\
                               .filter(model.CoreCustomer.corepos_card_number == card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_shoppers_for_member(self, member):
        """
        Return a list of shopper info dicts associated with the given
        member info dict (latter having come from the CORE API).
        """
        customers = member['customers']
        shoppers = []

        # make sure account holder is listed first
        account_holder = None
        secondary = False
        mixedup = False
        for customer in customers:
            if customer['accountHolder'] and not secondary:
                account_holder = customer
            elif not customer['accountHolder']:
                secondary = True
            elif customer['accountHolder'] and secondary:
                mixedup = True
        if mixedup:
            raise NotImplementedError("TODO: should re-sort the customers list for member {}".format(member['cardNo']))

        for i, customer in enumerate(customers, 1):
            shopper = dict(customer)
            shopper['card_number'] = member['cardNo']
            shopper['shopper_number'] = i
            shoppers.append(shopper)

        return shoppers

    def normalize_host_object(self, shopper):
        card_number = shopper['card_number']

        customer = self.get_customer_by_card_number(card_number)
        if not customer:
            log.warning("Rattail customer not found for CardNo %s: %s",
                        card_number, shopper)
            return

        data = {
            'customer_uuid': customer.uuid,
            'shopper_number': shopper['shopper_number'],
            'corepos_customer_id': int(shopper['customerID']),

            'first_name': shopper['firstName'],
            'last_name': shopper['lastName'],
            'display_name': normalize_full_name(shopper['firstName'],
                                                shopper['lastName']),

            # TODO: can a CORE shopper be *not* active?
            'active': True,

            'phone_number': shopper['phone'] or None,
            'phone_number_2': shopper['altPhone'] or None,

            'email_address': shopper['email'] or None,
            'account_holder': bool(shopper['accountHolder']),
        }

        # truncate phone number data if needed
        maxlen_phone_number = self.get_maxlen_phone_number()
        if data['phone_number'] and len(data['phone_number']) > maxlen_phone_number:
            log.warning("phone_number is too long (%s chars), "
                        "will truncate to %s chars: %s",
                        len(data['phone_number']),
                        maxlen_phone_number,
                        data['phone_number'])
            data['phone_number'] = data['phone_number'][:maxlen_phone_number]
        if data['phone_number_2'] and len(data['phone_number_2']) > maxlen_phone_number:
            log.warning("phone_number_2 is too long (%s chars), "
                        "will truncate to %s chars: %s",
                        len(data['phone_number_2']),
                        maxlen_phone_number,
                        data['phone_number_2'])
            data['phone_number_2'] = data['phone_number_2'][:maxlen_phone_number]

        # swap 1st and 2nd phone numbers if only latter has value
        self.prioritize_2(data, 'phone_number')

        return data


class StoreImporter(FromCOREPOSAPI, corepos_importing.model.StoreImporter):
    """
    Importer for store data from CORE POS API.
    """
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'id',
        'name',
    ]

    def get_host_objects(self):
        return self.api.get_stores()

    def normalize_host_object(self, store):
        return {
            'corepos_id': int(store['storeID']),
            'id': str(store['storeID']),
            'name': store['description'],
        }


class DepartmentImporter(FromCOREPOSAPI, corepos_importing.model.DepartmentImporter):
    """
    Importer for department data from CORE POS API.
    """
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
    ]

    def get_host_objects(self):
        return self.api.get_departments()

    def normalize_host_object(self, department):
        return {
            'corepos_number': int(department['dept_no']),
            'number': int(department['dept_no']),
            'name': department['dept_name'],
        }


class SubdepartmentImporter(FromCOREPOSAPI, corepos_importing.model.SubdepartmentImporter):
    """
    Importer for subdepartment data from CORE POS API.
    """
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
        'department_number',
    ]

    def get_host_objects(self):
        return self.api.get_subdepartments()

    def normalize_host_object(self, subdepartment):
        department_number = None
        if 'dept_ID' in subdepartment:
            department_number = int(subdepartment['dept_ID'])

        return {
            'corepos_number': int(subdepartment['subdept_no']),
            'number': int(subdepartment['subdept_no']),
            'name': subdepartment['subdept_name'],
            'department_number': department_number,
        }


class VendorImporter(FromCOREPOSAPI, corepos_importing.model.VendorImporter):
    """
    Importer for vendor data from CORE POS API.
    """
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'id',
        'name',
        'abbreviation',
        'special_discount',
        'phone_number',
        'fax_number',
        'email_address',
    ]

    def get_host_objects(self):
        return self.api.get_vendors()

    def normalize_host_object(self, vendor):
        return {
            'corepos_id': int(vendor['vendorID']),
            'id': str(vendor['vendorID']),
            'name': vendor['vendorName'],
            'abbreviation': vendor.get('vendorAbbreviation') or None,
            'special_discount': decimal.Decimal(vendor['discountRate']),
            'phone_number': vendor.get('phone') or None,
            'fax_number': vendor.get('fax') or None,
            'email_address': vendor.get('email') or None,
        }


class ProductImporter(FromCOREPOSAPI, corepos_importing.model.ProductImporter):
    """
    Importer for product data from CORE POS API.
    """
    key = 'uuid'
    supported_fields = [
        'uuid',
        'corepos_id',
        'item_id',
        'upc',
        'brand_name',
        'description',
        'unit_size',
        'unit_of_measure',
        'uom_abbreviation',
        'size',
        'weighed',
        'department_number',
        'subdepartment_number',
        'regular_price_price',
        'regular_price_multiple',
        'regular_price_type',
        'food_stampable',
        # 'tax1',
        # 'tax2',
        'case_size',
    ]

    def setup(self):
        super(ProductImporter, self).setup()
        model = self.model

        query = self.session.query(model.Product)\
                            .join(model.CoreProduct)\
                            .filter(model.CoreProduct.corepos_id != None)\
                            .options(orm.joinedload(model.Product._corepos))
        self.core_existing = self.app.cache_model(self.session,
                                                  model.Product,
                                                  key='corepos_id',
                                                  query=query)

        self.vendor_items_by_upc = {}

        def cache(item, i):
            self.vendor_items_by_upc.setdefault(item['upc'], []).append(item)

        self.progress_loop(cache, self.api.get_vendor_items(),
                           message="Caching CORE Vendor Items")

    def get_host_objects(self):
        return self.api.get_products()

    def identify_product(self, corepos_product):
        model = self.config.get_model()
        corepos_id = int(corepos_product['id'])

        if hasattr(self, 'core_existing'):
            product = self.core_existing.get(corepos_id)
            if product:
                return product

        else:
            try:
                return self.session.query(model.Product)\
                                   .join(model.CoreProduct)\
                                   .filter(model.CoreProduct.corepos_id == corepos_id)\
                                   .one()
            except orm.exc.NoResultFound:
                pass

        # at this point we'll search by `Product.item_id` instead
        return self.session.query(model.Product)\
                           .outerjoin(model.CoreProduct)\
                           .filter(model.CoreProduct.corepos_id == None)\
                           .filter(model.Product.item_id == corepos_product['upc'])\
                           .first()

    def identify_product_uuid(self, corepos_product):
        product = self.identify_product(corepos_product)
        if product:
            return product.uuid
        return get_uuid()

    def get_vendor_items(self, api_product):
        if hasattr(self, 'vendor_items_by_upc'):
            return self.vendor_items_by_upc.get(api_product['upc'])

        return self.api.get_vendor_items(upc=api_product['upc'])

    def normalize_host_object(self, product):
        try:
            upc = GPC(product['upc'], calc_check_digit='upc')
        except (TypeError, ValueError):
            log.debug("CORE POS product has invalid UPC: %s", product['upc'])
            if len(self.key) == 1 and self.key[0] == 'upc':
                return
            upc = None

        department_number = None
        if 'department' in product:
            department_number = int(product['department']) or None

        subdepartment_number = None
        if 'subdept' in product:
            subdepartment_number = int(product['subdept']) or None

        price = None
        if product.get('normal_price') is not None:
            price = decimal.Decimal(product['normal_price'])

        data = {
            'uuid': self.identify_product_uuid(product),
            'corepos_id': int(product['id']),
            'item_id': product['upc'],
            'upc': upc,
            'brand_name': product.get('brand') or None,
            'description': product.get('description') or '',

            'department_number': department_number,
            'subdepartment_number': subdepartment_number,

            'weighed': product.get('scale') == '1',
            'food_stampable': None,
            # 'tax1': product['tax'] == '1', # TODO: is this right?
            # 'tax2': product['tax'] == '2', # TODO: is this right?

            'regular_price_price': price,
            'regular_price_multiple': 1 if price is not None else None,
            'regular_price_type': self.enum.PRICE_TYPE_REGULAR if price is not None else None,
        }

        if 'foodstamp' in product:
            data['food_stampable'] = product['foodstamp'] == '1'

        if self.fields_active(self.size_fields):
            size_info = self.normalize_size_info(product)
            data.update({
                'size': size_info['size'],
                'unit_size': size_info['unit_size'],
                'unit_of_measure': size_info['uom_code'],
                'uom_abbreviation': size_info['uom_abbrev'],
            })

        if 'case_size' in self.fields:
            case_size = None
            items = self.get_vendor_items(product)
            if items:
                # here we sort by `modified DESC` to get the "deterministic
                # pseudo-default" vendorItems record

                def sortkey(item):
                    modified = item.get('modified')
                    if not modified:
                        return datetime.datetime(1900, 1, 1)
                    dt = datetime.datetime.strptime(modified, '%Y-%m-%d %H:%M:%S')
                    return dt

                items = sorted(items, key=sortkey, reverse=True)
                item = items[0]
                case_size = decimal.Decimal(item['units'])

            data['case_size'] = case_size

        return data


class ProductMovementImporter(FromCOREPOSAPI, corepos_importing.model.ProductImporter):
    """
    Importer for product movement data from CORE POS API.
    """
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'last_sold',
    ]
    allow_create = False
    allow_delete = False

    def get_host_objects(self):
        return self.api.get_products()

    def normalize_host_object(self, product):

        last_sold = None
        if 'last_sold' in product:
            last_sold = datetime.datetime.strptime(product['last_sold'], '%Y-%m-%d %H:%M:%S')
            last_sold = localtime(self.config, last_sold)
            last_sold = make_utc(last_sold)

        return {
            'corepos_id': int(product['id']),
            'last_sold': last_sold,
        }


class ProductCostImporter(FromCOREPOSAPI, corepos_importing.model.ProductCostImporter):
    """
    Importer for product cost data from CORE POS API.
    """
    key = ('vendor_uuid', 'code')
    supported_fields = [
        'corepos_id',
        'product_uuid',
        'vendor_uuid',
        'code',
        'case_size',
        'case_cost',
        'unit_cost',
        'preferred',
    ]

    def setup(self):
        super(ProductCostImporter, self).setup()
        model = self.config.get_model()

        query = self.session.query(model.Vendor)\
                            .join(model.CoreVendor)\
                            .filter(model.CoreVendor.corepos_id != None)
        self.vendors = self.app.cache_model(self.session,
                                            model.Vendor,
                                            query=query,
                                            key='corepos_id')

        self.corepos_products = {}

        def cache(product, i):
            self.corepos_products[product['upc']] = product

        self.progress_loop(cache, self.api.get_products(),
                           message="Caching Products from CORE-POS API")

        self.products_by_item_id = self.app.cache_model(self.session,
                                                        model.Product,
                                                        key='item_id')

    def get_host_objects(self):
        return self.api.get_vendor_items()

    def get_vendor(self, item):
        corepos_id = int(item['vendorID'])

        if hasattr(self, 'vendors'):
            return self.vendors.get(corepos_id)

        model = self.config.get_model()
        try:
            return self.session.query(model.Vendor)\
                               .join(model.CoreVendor)\
                               .filter(model.CoreVendor.corepos_id == corepos_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_corepos_product(self, item):
        if hasattr(self, 'corepos_products'):
            return self.corepos_products.get(item['upc'])

        return self.api.get_product(item['upc'])

    def get_product(self, item):
        item_id = item['upc']

        if hasattr(self, 'products_by_item_id'):
            return self.products_by_item_id.get(item_id)

        model = self.model
        try:
            return self.session.query(model.Product)\
                               .filter(model.Product.item_id == item_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def normalize_host_object(self, item):
        vendor = self.get_vendor(item)
        if not vendor:
            log.warning("CORE POS vendor not found for item: %s", item)
            return

        product = self.get_product(item)
        if not product:
            # just debug logging since this is a common scenario; the
            # CORE table is for items "available from vendor" but not
            # necssarily items carried by store
            log.debug("product not found for CORE vendor item: %s", item)
            return

        core_product = self.get_corepos_product(item)
        # if not product:
        #     log.warning("CORE POS product not found for item: %s", item)
        #     return

        preferred = False
        if core_product and core_product['default_vendor_id'] == item['vendorID']:
            preferred = True

        case_size = decimal.Decimal(item['units'])
        unit_cost = item.get('cost')
        if unit_cost is not None:
            unit_cost = decimal.Decimal(unit_cost)
        case_cost = None
        if unit_cost is not None:
            case_cost = unit_cost * case_size

        return {
            'corepos_id': int(item['vendorItemID']),
            'product_uuid': product.uuid,
            'vendor_uuid': vendor.uuid,
            'code': (item['sku'] or '').strip() or None,
            'case_size': case_size,
            'case_cost': case_cost,
            'unit_cost': unit_cost,
            'preferred': preferred,
        }


class MembershipTypeImporter(FromCOREPOSAPI, importing.model.MembershipTypeImporter):
    """
    Imports membership type data from CORE-POS API
    """
    key = 'number'
    supported_fields = [
        'number',
        'name',
    ]

    def get_host_objects(self):
        return self.api.get_member_types()

    def normalize_host_object(self, memtype):
        return {
            'number': int(memtype['memtype']),
            'name': memtype['memDesc'],
        }


class MemberImporter(FromCOREPOSAPI, corepos_importing.model.MemberImporter):
    """
    Importer for member data from CORE POS API.
    """
    key = 'number'
    supported_fields = [
        'number',
        'corepos_account_id',
        'customer_uuid',
        'person_first_name',
        'person_last_name',
        'membership_type_number',
        'joined',
        'withdrew',
        'active',
    ]

    # TODO: should make this configurable
    member_status_codes = [
        'PC',
        'TERM',
    ]

    # TODO: should make this configurable
    non_member_status_codes = [
        'REG',
        'INACT',
    ]

    def setup(self):
        super().setup()
        model = self.model

        self.customers_by_number = self.app.cache_model(
            self.session,
            model.Customer,
            key='number')

    def get_host_objects(self):
        return self.get_core_members()

    def get_customer_by_number(self, number):
        if hasattr(self, 'customers_by_number'):
            return self.customers_by_number.get(number)

        model = self.model
        try:
            return self.session.query(model.Customer)\
                               .filter(model.Customer.number == number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_corepos_customer(self, corepos_member):
        for customer in corepos_member['customers']:
            if customer['accountHolder']:
                return customer

    def normalize_host_object(self, member):
        card_number = member['cardNo']
        customer = self.get_customer_by_number(card_number)

        # TODO: at first i was *skipping* non-member status records,
        # but since CORE sort of assumes all customers are members,
        # probably not worth making the distinction here..?  it is
        # important to import the full member info from CORE, so that
        # we have it to sync back.  therefore can't afford to "skip"
        # any member records here
        if (member['memberStatus'] not in self.member_status_codes
            and member['memberStatus'] not in self.non_member_status_codes):
            log.warning("unexpected status '%s' for member %s: %s",
                        member['memberStatus'], card_number, member)

        joined = None
        if member['startDate'] and member['startDate'] != '0000-00-00 00:00:00':
            joined = datetime.datetime.strptime(member['startDate'],
                                                '%Y-%m-%d %H:%M:%S')
            joined = joined.date()

        withdrew = None
        if (member['endDate']
            and member['endDate'] != '0000-00-00 00:00:00'
            and member['endDate'] != '1900-01-01 00:00:00'):
            withdrew = datetime.datetime.strptime(member['endDate'],
                                                  '%Y-%m-%d %H:%M:%S')
            withdrew = withdrew.date()

        typeno = int(member['customerTypeID']) or None
        if typeno:
            memtype = self.get_membership_type_by_number(typeno)
            if not memtype:
                logger = log.warning if self.get_warn_for_unknown_membership_type() else log.debug
                logger("unknown customerTypeID (membership_type_number) %s for: %s",
                       member['customerTypeID'], member)
                typeno = None

        data = {
            'number': card_number,
            'corepos_account_id': int(member['customerAccountID']),
            'customer_uuid': customer.uuid if customer else None,
            'person_first_name': None,
            'person_last_name': None,
            'membership_type_number': typeno,
            'joined': joined,
            'withdrew': withdrew,
            'active': not bool(withdrew),
        }

        corepos_customer = self.get_corepos_customer(member)
        if corepos_customer:
            data['person_first_name'] = corepos_customer['firstName']
            data['person_last_name'] = corepos_customer['lastName']

        return data
