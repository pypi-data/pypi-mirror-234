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
CORE POS (DB) -> Rattail data importing
"""

import decimal
import logging
from collections import OrderedDict

from sqlalchemy import orm

from corepos.db.office_op import model as corepos, Session as CoreSession
from corepos.db.office_trans import model as coretrans, Session as CoreTransSession

from rattail import importing
from rattail.gpc import GPC
from rattail.db.util import normalize_full_name
from rattail_corepos import importing as corepos_importing


log = logging.getLogger(__name__)


class FromCOREPOSToRattail(importing.FromSQLAlchemyHandler, importing.ToRattailHandler):
    """
    Import handler for data coming from a CORE POS database.
    """
    # TODO: these should be changed, it now allows for "trans" DB too..
    generic_host_title = 'CORE Office (DB "op")'
    host_key = 'corepos_db_office_op'
    corepos_dbkey = 'default'

    @property
    def host_title(self):
        return "CORE-POS (DB/{})".format(self.corepos_dbkey)

    def make_host_session(self):

        # session type depends on the --corepos-dbtype arg
        if self.corepos_dbtype == 'office_trans':
            return CoreTransSession(bind=self.config.coretrans_engines[self.corepos_dbkey])

        # assume office_op by default
        return CoreSession(bind=self.config.corepos_engines[self.corepos_dbkey])

    def get_importers(self):
        importers = OrderedDict()
        importers['Employee'] = EmployeeImporter
        importers['Tax'] = TaxImporter
        importers['Tender'] = TenderImporter
        importers['Vendor'] = VendorImporter
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Product'] = ProductImporter
        importers['MemberEquityPayment'] = MemberEquityPaymentImporter
        return importers

    def get_default_keys(self):
        keys = super().get_default_keys()

        if 'MemberEquityPayment' in keys:
            keys.remove('MemberEquityPayment')

        return keys


class FromCOREPOS(importing.FromSQLAlchemy):
    """
    Base class for all CORE POS data importers.
    """


class EmployeeImporter(FromCOREPOS, corepos_importing.model.EmployeeImporter):
    """
    Importer for employee data from CORE POS.
    """
    host_model_class = corepos.Employee
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'first_name',
        'last_name',
        'full_name',
        'status',
    ]

    def normalize_host_object(self, employee):
        return {
            'corepos_number': employee.number,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'full_name': normalize_full_name(employee.first_name, employee.last_name),
            'status': self.enum.EMPLOYEE_STATUS_CURRENT if employee.active else self.enum.EMPLOYEE_STATUS_FORMER,
        }


class TaxImporter(FromCOREPOS, corepos_importing.model.TaxImporter):
    """
    Importer for tax data from CORE POS.
    """
    host_model_class = corepos.TaxRate
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'code',
        'description',
        'rate',
    ]

    def normalize_host_object(self, tax):
        return {
            'corepos_id': tax.id,
            'code': str(tax.id),
            'description': tax.description,
            'rate': decimal.Decimal(str(tax.rate * 100)),
        }


class TenderImporter(FromCOREPOS, corepos_importing.model.TenderImporter):
    """
    Importer for tender data from CORE POS.
    """
    host_model_class = corepos.Tender
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'code',
        'name',
    ]

    def normalize_host_object(self, tender):
        return {
            'corepos_id': tender.tender_id,
            'code': tender.tender_code,
            'name': tender.tender_name,
        }


class VendorImporter(FromCOREPOS, corepos_importing.model.VendorImporter):
    """
    Importer for vendor data from CORE POS.
    """
    host_model_class = corepos.Vendor
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'name',
        'abbreviation',
        'special_discount',
        'phone_number',
        'fax_number',
        'email_address',
    ]

    def cache_query(self):
        """
        Return the query to be used when caching "local" data.
        """
        # can't just use rattail.db.model b/c the CoreVendor would normally not
        # be in there!  this still requires custom model to be configured though.
        model = self.config.get_model()

        # first get default query
        query = super(VendorImporter, self).cache_query()

        # maybe filter a bit, to ensure only "relevant" records are involved
        if 'corepos_id' in self.key:
            # note, the filter is probably redundant since we INNER JOIN on the
            # extension table, and it doesn't allow null ID values.  but clarity.
            query = query.join(model.CoreVendor)\
                         .filter(model.CoreVendor.corepos_id != None)

        return query

    def normalize_host_object(self, vendor):

        special_discount = None
        if vendor.discount_rate is not None:
            special_discount = decimal.Decimal('{:0.3f}'.format(vendor.discount_rate))

        return {
            'corepos_id': vendor.id,
            'name': vendor.name,
            'abbreviation': vendor.abbreviation or None,
            'special_discount': special_discount,
            'phone_number': vendor.phone or None,
            'fax_number': vendor.fax or None,
            'email_address': vendor.email or None,
        }


class DepartmentImporter(FromCOREPOS, corepos_importing.model.DepartmentImporter):
    """
    Importer for department data from CORE POS.
    """
    host_model_class = corepos.Department
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
    ]

    def normalize_host_object(self, department):
        return {
            'corepos_number': department.number,
            'number': department.number,
            'name': department.name,
        }


class SubdepartmentImporter(FromCOREPOS, corepos_importing.model.SubdepartmentImporter):
    """
    Importer for subdepartment data from CORE POS.
    """
    host_model_class = corepos.Subdepartment
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
        'department_number',
    ]

    def normalize_host_object(self, subdepartment):
        return {
            'corepos_number': subdepartment.number,
            'number': subdepartment.number,
            'name': subdepartment.name,
            'department_number': subdepartment.department_number,
        }


class ProductImporter(FromCOREPOS, corepos_importing.model.ProductImporter):
    """
    Importer for product data from CORE POS.
    """
    host_model_class = corepos.Product
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'item_id',
        'upc',
        'brand_name',
        'description',
        'size',
        'unit_size',
        'unit_of_measure',
        'uom_abbreviation',
        'weighed',
        'department_number',
        'subdepartment_number',
        'regular_price_price',
        'regular_price_multiple',
        'regular_price_type',
        'food_stampable',
        # 'tax1',
        'tax_code',
    ]

    def normalize_host_object(self, product):

        try:
            upc = GPC(product.upc, calc_check_digit='upc')
        except (TypeError, ValueError):
            log.debug("CORE POS product has invalid UPC: %s", product.upc)
            if len(self.key) == 1 and self.key[0] == 'upc':
                return
            upc = None

        price = None
        if product.normal_price is not None:
            price = decimal.Decimal('{:03f}'.format(product.normal_price))

        data = {
            'corepos_id': product.id,
            'item_id': product.upc,
            'upc': upc,
            'brand_name': (product.brand or '').strip() or None,
            'description': (product.description or '').strip(),

            'department_number': product.department_number or None,
            'subdepartment_number': product.subdepartment_number or None,

            'weighed': bool(product.scale),
            'food_stampable': product.foodstamp,
            # 'tax1': bool(product.tax), # TODO: is this right?

            'regular_price_price': price,
            'regular_price_multiple': 1 if price is not None else None,
            'regular_price_type': self.enum.PRICE_TYPE_REGULAR if price is not None else None,

            'tax_code': str(product.tax_rate.id) if product.tax_rate_id else None,
        }

        if self.fields_active(self.size_fields):
            size_info = self.normalize_size_info(product)
            data.update({
                'size': size_info['size'],
                'unit_size': size_info['unit_size'],
                'unit_of_measure': size_info['uom_code'],
                'uom_abbreviation': size_info['uom_abbrev'],
            })

        return data


class MemberEquityPaymentImporter(FromCOREPOS, corepos_importing.model.MemberEquityPaymentImporter):
    """
    Imports equity payment data from CORE-POS
    """
    host_model_class = coretrans.StockPurchase
    key = 'uuid'
    supported_fields = [
        'uuid',
        'member_uuid',
        'amount',
        'received',
        'transaction_identifier',
        'corepos_card_number',
        'corepos_transaction_number',
        'corepos_transaction_id',
        'corepos_department_number',
        'corepos_datetime',
    ]

    def setup(self):
        super().setup()
        model = self.model

        query = self.session.query(model.Member)\
                            .join(model.Customer)\
                            .join(model.CoreCustomer)\
                            .options(orm.joinedload(model.Member.customer)\
                                     .joinedload(model.Customer._corepos))
        self.members_by_card_number = self.cache_model(
            model.Member, query=query,
            key=lambda member, normal: member.customer.corepos_card_number)

        payments = self.session.query(model.MemberEquityPayment)\
                               .join(model.CoreMemberEquityPayment)\
                               .filter(model.CoreMemberEquityPayment.corepos_transaction_number != None)\
                               .filter(model.CoreMemberEquityPayment.corepos_transaction_id != None)\
                               .all()
        self.payments_by_card_number = {}
        def add(payment, i):
            self.payments_by_card_number.setdefault(payment.corepos_card_number, []).append(payment)
        self.progress_loop(add, payments, message="Grouping payments by card number")

    def cache_query(self):
        query = super().cache_query()
        model = self.model

        # ignore existing payments not known to be in CORE
        # TODO: is this in fact a good idea?
        query = query.join(model.CoreMemberEquityPayment)\
                     .filter(model.CoreMemberEquityPayment.corepos_transaction_number != None)

        return query

    def get_member(self, card_number):
        if hasattr(self, 'members_by_card_number'):
            return self.members_by_card_number.get(card_number)

        model = self.model
        try:
            return self.session.query(model.Member)\
                               .join(model.Customer)\
                               .join(model.CoreCustomer)\
                               .filter(model.CoreCustomer.corepos_card_number == card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_payment(self, stock_purchase):
        payments = self.payments_by_card_number.get(stock_purchase.card_number)
        if not payments:
            return

        # first look for exact match
        datetime = self.app.localtime(stock_purchase.datetime)
        match = [payment for payment in payments
                 if payment.corepos_transaction_number == stock_purchase.transaction_number
                 and payment.corepos_transaction_id == stock_purchase.transaction_id
                 and payment.amount == stock_purchase.amount
                 and payment.corepos_department_number == stock_purchase.department_number
                 and self.app.localtime(payment.corepos_datetime, from_utc=True) == datetime]
        if len(match) == 1:
            return match[0]

        # nb. avoid datetime for this one
        matches = [payment for payment in payments
                   if payment.corepos_transaction_number == stock_purchase.transaction_number
                   and payment.corepos_transaction_id == stock_purchase.transaction_id
                   and payment.amount == stock_purchase.amount
                   and payment.corepos_department_number == stock_purchase.department_number]
        if len(matches) == 1:
            return matches[0]

        # TODO: not sure how to handle yet, if last check found more
        # than one match.  presumably if none were found then it is
        # safe to just return none though..
        if matches:
            raise NotImplementedError(f"{len(matches)} payments matched for CORE equity: {stock_purchase}")

    def normalize_host_object(self, stock_purchase):

        card_number = stock_purchase.card_number
        member = self.get_member(card_number)
        if not member:
            log.warning("member not found for card number %s: %s",
                        card_number, stock_purchase)
            return

        dt = stock_purchase.datetime
        if dt:
            dt = self.app.make_utc(self.app.localtime(dt))
        corepos_datetime = dt
        received = dt

        payment = self.get_payment(stock_purchase)
        if payment and payment.source != 'corepos':
            received = payment.received

        return {
            'uuid': payment.uuid if payment else self.app.make_uuid(),
            'member_uuid': member.uuid,
            'amount': stock_purchase.amount,
            'received': received,
            'transaction_identifier': stock_purchase.transaction_number,
            'corepos_card_number': stock_purchase.card_number,
            'corepos_transaction_number': stock_purchase.transaction_number,
            'corepos_transaction_id': stock_purchase.transaction_id,
            'corepos_department_number': stock_purchase.department_number,
            'corepos_datetime': corepos_datetime,
        }

    def create_object(self, key, host_data):
        payment = super().create_object(key, host_data)
        if payment:

            # track where each payment comes from!
            payment.source = 'corepos'

            return payment
