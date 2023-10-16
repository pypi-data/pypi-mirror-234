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
Handler for CORE equity import batches
"""

import datetime

from corepos.db.office_trans import model as coretrans, Session as CoreTransSession

from rattail.batch import BatchHandler
from rattail_corepos.db.model import CoreEquityImportBatch


class CoreEquityImportBatchHandler(BatchHandler):
    """
    Handler for CORE member batches.
    """
    batch_model_class = CoreEquityImportBatch

    def refresh_row(self, row):
        session = self.app.get_session(row)
        model = self.model

        row.status_code = None
        row.status_text = None

        if not row.card_number:
            row.status_code = row.STATUS_MISSING_VALUES
            row.status_text = "card_number"
            return

        if not row.payment_amount:
            row.status_code = row.STATUS_MISSING_VALUES
            row.status_text = "payment_amount"
            return

        if not row.department_number:
            row.status_code = row.STATUS_MISSING_VALUES
            row.status_text = "department_number"
            return

        if not row.timestamp:
            row.status_code = row.STATUS_MISSING_VALUES
            row.status_text = "timestamp"
            return

        payment = row.payment
        if payment and payment.corepos_transaction_number:
            row.status_code = row.STATUS_ALREADY_IN_CORE
            return

        member = payment.member if payment else None
        row.member = member
        if not member:
            row.status_code = row.STATUS_MEMBER_NOT_FOUND
            return

        memtype = member.membership_type
        row.member_type_id = memtype.number if memtype else None

        if member.person:
            person = member.person
            row.first_name = person.first_name
            row.last_name = person.last_name

        membership = self.app.get_membership_handler()
        row.rattail_equity_total = membership.get_equity_total(member)

        row.status_code = row.STATUS_OK

    def describe_execution(self, batch, **kwargs):
        return "New payment transactions will be added directly to CORE-POS."

    def get_effective_rows(self, batch):
        return [row for row in batch.active_rows()
                if row.status_code not in (row.STATUS_MISSING_VALUES,
                                           row.STATUS_MEMBER_NOT_FOUND,
                                           row.STATUS_ALREADY_IN_CORE)]

    def execute(self, batch, progress=None, **kwargs):
        rows = self.get_effective_rows(batch)
        self.export_payments_to_corepos(rows, progress=progress)
        return True

    def get_store_id(self, row):
        # TODO: what should this be?
        return 1

    def get_register_number(self, row):
        # TODO: what should this be?
        return 1

    def get_employee_number(self, row):
        # TODO: what should this be?
        return 0

    def get_next_transaction_number(self, session):
        # TODO: how should we generate this?
        return self.consume_batch_id(session)

    def get_next_timestamp(self, row):
        dt = self.next_timestamp
        self.next_timestamp += datetime.timedelta(seconds=1)
        return self.app.localtime(dt, tzinfo=False).replace(microsecond=0)

    def get_transaction_status(self, row):
        # TODO: what should this be?
        return 'G'

    def export_payments_to_corepos(self, rows, progress=None):
        coretrans_session = CoreTransSession()
        self.next_timestamp = self.app.localtime()

        def export(row, i):
            session = self.app.get_session(row)

            # will insert 2 records in `core_trans.dtransactions` ...

            # they will have this data in common
            host_data = {
                'store_id': self.get_store_id(row),
                'register_number': self.get_register_number(row),
                'transaction_number': self.get_next_transaction_number(session),
                'employee_number': self.get_employee_number(row),
                'card_number': row.card_number,
                'date_time': self.get_next_timestamp(row),
                'total': row.payment_amount,
                'transaction_status': self.get_transaction_status(row),
            }

            # first a record to ring up the equity item
            detail = coretrans.TransactionDetail(**host_data)
            detail.transaction_id = 1
            detail.upc = 'TEST_ITEM' # TODO: what should this say?
            detail.description = 'TEST_EQUITY_ITEM' # TODO: what should this say?
            detail.department_number = row.department_number
            detail.quantity = 1 # TODO: should this ever be anything else?
            detail.unit_price = row.payment_amount
            coretrans_session.add(detail)

            # then a record to accept tender payment
            detail = coretrans.TransactionDetail(**host_data)
            detail.transaction_id = 2
            detail.upc = 'TEST_TENDER' # TODO: what should this say?
            detail.description = 'TEST_EQUITY_TENDER' # TODO: what should this say?
            coretrans_session.add(detail)

            # update payment in Rattail to indicate presence in CORE
            payment = row.payment
            if payment:
                # nb. these must match exactly to be used later as importer key
                payment.corepos_card_number = row.card_number
                payment.corepos_department_number = row.department_number
                payment.corepos_transaction_number = f"{host_data['employee_number']}-{host_data['register_number']}-{host_data['transaction_number']}"
                payment.corepos_transaction_id = 1
                payment.corepos_datetime = self.app.make_utc(self.app.localtime(host_data['date_time']))
                # TODO: stop setting these, *after* importer stops using for key
                # (or perhaps config should determine whether to set?)
                payment.received = payment.corepos_datetime
                payment.transaction_identifier = payment.corepos_transaction_number

        self.progress_loop(export, rows, progress,
                           message="Exporting payments to CORE-POS")

        coretrans_session.commit()
        coretrans_session.close()
