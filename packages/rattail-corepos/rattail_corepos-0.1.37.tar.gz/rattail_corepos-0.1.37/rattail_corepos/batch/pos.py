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
POS batch handler, for CORE-POS integration
"""

import logging

from rattail.batch import pos as base


log = logging.getLogger(__name__)


class POSBatchHandler(base.POSBatchHandler):
    """
    Handler for POS batches
    """

    def describe_execution(self, batch, **kwargs):
        return ("A new transaction will be created in CORE Office, directly "
                "in `dtransactions`, to mirror this batch.")

    def execute(self, batch, progress=None, **kwargs):
        rows = self.get_effective_rows(batch)
        if not rows:
            return True

        self.corepos_handler = self.app.get_corepos_handler()
        self.coretrans = self.corepos_handler.get_model_office_trans()
        self.maxlen_upc = self.app.maxlen(self.coretrans.TransactionDetail.upc)
        self.maxlen_description = self.app.maxlen(self.coretrans.TransactionDetail.description)

        # convert batch rows to `dtransactions` records
        dtransactions = self.normalize_dtransactions(batch, rows, progress)
        if not dtransactions:
            return True

        # commit all to `dtransactions`
        coretrans_session = self.corepos_handler.make_session_office_trans()
        coretrans_session.add_all(dtransactions)
        coretrans_session.commit()
        coretrans_session.close()
        return True

    def normalize_dtransactions(self, batch, rows, progress=None):
        dtransactions = []

        def add(row, i):

            # TODO: row types ugh

            if row.row_type == 'sell':
                d = self.make_d_item(row)
                dtransactions.append(d)

            elif row.row_type == 'badscan':
                d = self.make_d_badscan(row)
                dtransactions.append(d)

            elif row.row_type in ('set_customer', 'swap_customer'):
                d = self.make_d_customer(row)
                dtransactions.append(d)

            elif row.row_type == 'tender':
                d = self.make_d_tender(row)
                dtransactions.append(d)

        self.progress_loop(add, rows, progress,
                           message="Normalizing items for CORE-POS transaction")

        return dtransactions

    def make_d_basic(self, batch=None, row=None):
        if not batch and not row:
            raise ValueError("must specify either batch or row")
        
        if not batch:
            batch = row.batch

        d = self.coretrans.TransactionDetail()

        d.transaction_number = batch.id

        if row and row.timestamp:
            d.date_time = self.app.localtime(row.timestamp, from_utc=True)
        else:
            # nb. batch.created *should* have a value..if not this would be "now"
            d.date_time = self.app.localtime(batch.created, from_utc=True)

        if batch.terminal_id and batch.terminal_id.isdigit():
            d.register_number = int(batch.terminal_id)

        if batch.customer:
            d.card_number = batch.customer.number

        d.quantity = 0
        d.unit_price = 0
        d.discount = 0
        d.total = 0
        # d.voided = False        # TODO
        return d

    def make_d_badscan(self, row):
        d = self.make_d_basic(row=row)
        d.description = 'BADSCAN'

        d.upc = row.item_entry
        if d.upc and len(d.upc) > self.maxlen_upc:
            log.debug("have to truncate this upc to %s chars (it has %s): %s",
                      self.maxlen_upc, len(d.upc), d.upc)
            d.upc = d.upc[:self.maxlen_upc]
            d.description += " (TRUNCATED)"

        return d

    def make_d_customer(self, row):
        d = self.make_d_basic(row=row)
        d.upc = 'MEMENTRY'
        d.description = 'CARDNO IN NUMFLAG'
        return d

    def make_d_item(self, row):
        batch = row.batch
        d = self.make_d_basic(batch, row)
        d.transaction_type = 'I'
        d.upc = row.product.item_id
        d.department_number = row.department_number

        d.description = row.product.description
        if d.description and len(d.description) > self.maxlen_description:
            log.debug("have to truncate this description to %s chars (it has %s): %s",
                      self.maxlen_description, len(d.description), d.description)
            d.description = d.description[:self.maxlen_description]

        d.quantity = row.quantity
        d.unit_price = row.txn_price
        d.reg_price = row.reg_price
        d.total = row.sales_total
        # d.voided = False        # TODO
        return d

    def make_d_tender(self, row):
        batch = row.batch
        d = self.make_d_basic(batch, row)
        d.transaction_type = 'T'
        d.transaction_subtype = row.item_entry
        d.description = row.description
        d.total = row.tender_total
        return d
