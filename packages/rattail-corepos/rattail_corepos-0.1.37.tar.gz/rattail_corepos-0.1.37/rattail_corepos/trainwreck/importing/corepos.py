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
CORE-POS -> Trainwreck data importing
"""

from collections import OrderedDict

from corepos.db.office_trans import Session as CoreTransSession, model as coretrans
from corepos.db.office_op import Session as CoreSession, model as corepos

from rattail import importing
from rattail.time import localtime, make_utc
from rattail.trainwreck import importing as trainwreck_importing


class FromCoreToTrainwreck(importing.FromSQLAlchemyHandler, trainwreck_importing.ToTrainwreckHandler):
    """
    Import data from CORE-POS into Trainwreck
    """
    host_key = 'corepos_db_office_trans'
    host_title = "CORE-POS"
    generic_host_title = 'CORE Office (DB "trans")'
    corepos_dbkey = 'default'

    def make_host_session(self):
        return CoreTransSession(bind=self.config.coretrans_engines[self.corepos_dbkey])

    def get_importer_kwargs(self, key, **kwargs):
        kwargs = super(FromCoreToTrainwreck, self).get_importer_kwargs(key, **kwargs)
        kwargs.setdefault('core_op_session', self.core_op_session)
        return kwargs

    def begin_host_transaction(self):
        super(FromCoreToTrainwreck, self).begin_host_transaction()

        self.core_op_session = CoreSession(bind=self.config.corepos_engines[self.corepos_dbkey])

    def rollback_host_transaction(self):
        super(FromCoreToTrainwreck, self).rollback_host_transaction()

        self.core_op_session.rollback()
        self.core_op_session.close()
        self.core_op_session = None

    def commit_host_transaction(self):
        super(FromCoreToTrainwreck, self).commit_host_transaction()

        self.core_op_session.commit()
        self.core_op_session.close()
        self.core_op_session = None

    def get_importers(self):
        importers = OrderedDict()
        importers['Transaction'] = TransactionImporter
        importers['TransactionItem'] = TransactionItemImporter
        return importers


class FromCore(importing.Importer):
    """
    Base class for CORE importers.
    """

    def fetch_details(self):
        # TODO: should figure out "which" txns apply to our date range first,
        # w/ a rather "loose" query, to avoid issues when a txn spans multiple
        # dates..?
        return self.host_session.query(coretrans.TransactionDetail)\
                                .filter(coretrans.TransactionDetail.date_time >= self.start_time)\
                                .filter(coretrans.TransactionDetail.date_time < self.end_time)\
                                .order_by(coretrans.TransactionDetail.register_number,
                                          coretrans.TransactionDetail.transaction_number,
                                          coretrans.TransactionDetail.store_row_id)\
                                .all()

    def make_system_id(self, detail):
        assert detail.employee_number
        core_id = '-'.join([
            str(detail.employee_number),
            str(detail.register_number),
            str(detail.transaction_number),
        ])
        return '|'.join([
            str(detail.store_id),
            core_id,
        ])


class TransactionImporter(FromCore, trainwreck_importing.model.TransactionImporter):
    """
    Import transaction data from CORE-POS
    """
    key = ('system', 'system_id')
    importing_from_system = 'corepos'
    supported_fields = [
        'system',
        'system_id',
        'terminal_id',
        'receipt_number',
        'start_time',
        'end_time',
        'cashier_id',
        'cashier_name',
        'customer_id',
        'customer_name',
        'subtotal',
        'total',
    ]

    def setup(self):
        super(TransactionImporter, self).setup()

        app = self.config.get_app()
        self.people_handler = app.get_people_handler()

        if 'cashier_name' in self.fields:
            self.corepos_employees = self.cache_model(corepos.Employee,
                                                      session=self.core_op_session,
                                                      key='number')

        if 'customer_name' in self.fields:
            query = self.core_op_session.query(corepos.CustomerClassic)\
                                        .filter(corepos.CustomerClassic.person_number == 1)
            self.corepos_customers = self.cache_model(corepos.CustomerClassic,
                                                      session=self.core_op_session,
                                                      query=query,
                                                      key='card_number')

    def get_host_objects(self):
        details = self.fetch_details()
        transactions = []
        current = {}

        def collect(detail, i):

            system_id = self.make_system_id(detail)
            if current and current['system_id'] != system_id:
                transactions.append(dict(current))
                current.clear()

            date_time = detail.date_time
            if date_time:
                date_time = localtime(self.config, date_time)
                date_time = make_utc(date_time)

            if not current:
                current.update({
                    'system': self.enum.TRAINWRECK_SYSTEM_COREPOS,
                    'system_id': system_id,
                    'terminal_id': str(detail.register_number),
                    'receipt_number': str(detail.transaction_number),
                    'cashier_id': str(detail.employee_number) if detail.employee_number else None,
                    'customer_id': str(detail.card_number) if detail.card_number else None,
                    'start_time': date_time,
                    'end_time': date_time,
                })

            if detail.transaction_type == 'C':
                if 'Subtotal' in detail.description:
                    current['subtotal'] = detail.unit_price
                    current['total'] = detail.unit_price

            if date_time:
                current['end_time'] = date_time

        self.progress_loop(collect, details,
                           message="Collecting transaction data")

        # don't forget to add the last one!
        if current:
            transactions.append(current)
        return transactions

    def normalize_host_object(self, txn):

        if 'cashier_name' in self.fields:
            txn['cashier_name'] = None
            if txn['cashier_id']:
                employee = self.corepos_employees.get(int(txn['cashier_id']))
                if employee:
                    txn['cashier_name'] = self.people_handler.normalize_full_name(
                        employee.first_name, employee.last_name)

        if 'customer_name' in self.fields:
            txn['customer_name'] = None
            if txn['customer_id']:
                custdata = self.corepos_customers.get(int(txn['customer_id']))
                if custdata:
                    txn['customer_name'] = self.people_handler.normalize_full_name(
                        custdata.first_name, custdata.last_name)

        return txn


class TransactionItemImporter(FromCore, trainwreck_importing.model.TransactionItemImporter):
    """
    Import transaction item data from CORE-POS
    """
    key = ('transaction_system_id', 'sequence')
    importing_from_system = 'corepos'
    supported_fields = [
        'transaction_system_id',
        'sequence',
        'item_scancode',
        'department_number',
        'description',
        'unit_price',
        'unit_quantity',
        'total',
        'void',
    ]

    def get_host_objects(self):
        return self.fetch_details()

    def normalize_host_object(self, detail):

        # TODO: this needs to be a lot smarter.  for now this "works" i guess
        if detail.transaction_type != 'I':
            return

        return {
            'transaction_system_id': self.make_system_id(detail),
            'sequence': detail.transaction_id,
            'item_scancode': detail.upc,
            'department_number': detail.department_number,
            'description': detail.description,
            'unit_price': detail.unit_price,
            'unit_quantity': detail.quantity,
            'total': detail.total,
            'void': bool(detail.voided),
        }
