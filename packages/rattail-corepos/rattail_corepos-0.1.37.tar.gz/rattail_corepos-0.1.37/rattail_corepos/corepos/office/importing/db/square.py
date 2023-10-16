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
Square -> CORE-POS data importing
"""

import re
import datetime
import decimal
from collections import OrderedDict

import sqlalchemy as sa

from corepos.db.office_trans import Session as CoreTransSession, model as coretrans

from rattail import importing
from rattail_corepos.corepos.office.importing import db as corepos_importing


class FromSquareToCoreTrans(importing.ToSQLAlchemyHandler):
    """
    Square -> CORE-POS import handler.
    """
    host_title = "Square"
    local_title = "CORE-POS"

    def make_session(self):
        return CoreTransSession()

    def get_importers(self):
        importers = OrderedDict()
        importers['TransactionDetail'] = TransactionDetailImporter
        return importers


class FromSquare(importing.FromCSV):
    """
    Base class for Square -> CORE-POS importers.
    """


class TransactionDetailImporter(FromSquare, corepos_importing.model.TransactionDetailImporter):
    """
    Transaction detail importer.
    """
    key = 'store_row_id'
    supported_fields = [
        'store_row_id',
        'date_time',
        'card_number',
        'upc',
        'description',
        'quantity',
        'unit_price',
        'discount',
        'tax',
        'total',
    ]

    batches_supported = True

    def setup(self):
        super(TransactionDetailImporter, self).setup()

        # cache existing transactions by ID
        self.transaction_details = self.cache_model(coretrans.TransactionDetail,
                                                    key=self.transaction_detail_key)

        # keep track of new IDs
        self.new_ids = {}
        self.last_new_id = self.get_last_new_id()

    def transaction_detail_key(self, detail, normal):
        return (
            detail.store_id,
            detail.register_number,
            detail.date_time,
            detail.upc,
        )

    def get_last_new_id(self):
        # TODO: pretty sure there is a better way to do this...
        return self.session.query(sa.func.max(coretrans.TransactionDetail.store_row_id))\
                           .scalar() or 0

    currency_pattern = re.compile(r'^\$(?P<amount>\d+\.\d\d)$')
    currency_pattern_negative = re.compile(r'^\(\$(?P<amount>\d+\.\d\d)\)$')

    def parse_currency(self, value):
        value = (value or '').strip() or None
        if value:

            # first check for positive amount
            match = self.currency_pattern.match(value)
            if match:
                return float(match.group('amount'))

            # okay then, check for negative amount
            match = self.currency_pattern_negative.match(value)
            if match:
                return 0 - float(match.group('amount'))

    def normalize_host_object(self, csvrow):

        # date_time
        date = datetime.datetime.strptime(csvrow['Date'], '%m/%d/%Y').date()
        time = datetime.datetime.strptime(csvrow['Time'], '%H:%M:%S').time()
        date_time = datetime.datetime.combine(date, time)

        # upc
        upc = csvrow['SKU']

        # store_row_id
        key = (
            0,                  # store_id
            None,               # register_number
            date_time,
            upc,
        )
        if key in self.transaction_details:
            store_row_id = self.transaction_details[key].store_row_id
        else:
            store_row_id = self.last_new_id + 1
            self.new_ids[store_row_id] = csvrow
            self.last_new_id = store_row_id

        # card_number
        card_number = csvrow['Customer Reference ID'] or None
        if card_number:
            card_number = int(card_number)

        # description
        description = csvrow['Item']

        # quantity
        quantity = float(csvrow['Qty'])

        # unit_price
        unit_price = self.parse_currency(csvrow['Gross Sales'])
        if unit_price is not None:
            unit_price /= quantity
            unit_price = decimal.Decimal('{:0.2f}'.format(unit_price))
        elif csvrow['Gross Sales']:
            log.warning("cannot parse 'unit_price' from: %s", csvrow['Gross Sales'])

        # discount
        discount = self.parse_currency(csvrow['Discounts'])
        if discount is not None:
            discount = decimal.Decimal('{:0.2f}'.format(discount))
        elif csvrow['Discounts']:
            log.warning("cannot parse 'discount' from: %s", csvrow['Discounts'])

        # tax
        tax = self.parse_currency(csvrow['Tax'])
        if csvrow['Tax'] and tax is None:
            log.warning("cannot parse 'tax' from: %s", csvrow['Tax'])
        tax = bool(tax)

        # total
        total = self.parse_currency(csvrow['Net Sales'])
        if total is not None:
            total = decimal.Decimal('{:0.2f}'.format(total))
        elif csvrow['Net Sales']:
            log.warning("cannot parse 'total' from: %s", csvrow['Net Sales'])

        return {
            '_object_str': "({}) {}".format(upc, description),
            'store_row_id': store_row_id,
            'date_time': date_time,
            'card_number': card_number,
            'upc': upc,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount': discount,
            'tax': tax,
            'total': total,
        }
