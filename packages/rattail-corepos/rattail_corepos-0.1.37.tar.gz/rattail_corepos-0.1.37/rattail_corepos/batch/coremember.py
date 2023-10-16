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
Handler for CORE member batches
"""

import csv
import logging

from corepos.db.office_op import Session as CoreSession, model as corepos

from rattail.batch import BatchHandler
from rattail.db.util import maxlen
from rattail_corepos.db.model import CoreMemberBatch, CoreMemberBatchRow


log = logging.getLogger(__name__)


class CoreMemberBatchHandler(BatchHandler):
    """
    Handler for CORE member batches.
    """
    batch_model_class = CoreMemberBatch

    def should_populate(self, batch):
        if batch.input_file:
            return True
        return False

    def setup(self, batch, progress=None):
        self.core_session = CoreSession()

    setup_populate = setup
    setup_refresh = setup

    def teardown(self, batch, progress=None):
        self.core_session.close()
        del self.core_session

    teardown_populate = teardown
    teardown_refresh = teardown

    def populate(self, batch, progress=None):
        if batch.input_file:
            return self.populate_from_file(batch, progress=progress)
        raise NotImplementedError("do not know how to populate this batch")

    def populate_from_file(self, batch, progress=None):
        """
        Populate member batch from input data file.
        """
        # TODO: how should we detect what type of input file we have?
        # this way is pretty lame but sort of works for testing
        if 'member-status' in batch.input_file:
            return self.populate_from_member_file(batch, progress=progress)

        return self.populate_from_contact_file(batch, progress=progress)

    def populate_from_contact_file(self, batch, progress=None):
        """
        Populate member batch from "contact" CSV input data file.
        """
        input_path = batch.filepath(self.config, batch.input_file)
        input_file = open(input_path, 'rt')
        reader = csv.DictReader(input_file)
        data = list(reader)
        input_file.close()

        fields = [
            'first_name',
            'last_name',
            'street',
            'city',
            'state',
            'zipcode',
            'phone',
            'email1',
        ]

        batch.set_param('fields', fields)

        maxlens = {}
        for field in fields:
            maxlens[field] = maxlen(getattr(CoreMemberBatchRow, field))

        def append(csvrow, i):
            row = self.make_row()
            row.card_number_raw = csvrow['external_id']
            if csvrow['external_id'].isdigit():
                row.card_number = int(csvrow['external_id'])
            row.first_name = csvrow['first_name']
            row.last_name = csvrow['last_name']
            row.street = csvrow['primary_address1']
            row.city = csvrow['primary_city']
            row.state = csvrow['primary_state']
            row.zipcode = csvrow['primary_zip']
            row.phone = csvrow['phone_number']
            # TODO: this seems useful, but maybe in another step?
            # row.phone = self.app.format_phone_number(csvrow['phone_number'])
            row.email1 = csvrow['email']

            for field in fields:
                if len(getattr(row, field)) > maxlens[field]:
                    log.warning("%s field is %s and will be truncated to %s "
                                "for row #%s in CSV data: %s",
                                field,
                                len(getattr(row, field)),
                                maxlens[field],
                                i + 1,
                                csvrow)
                    value = getattr(row, field)
                    setattr(row, field, value[:maxlens[field]])

            self.add_row(batch, row)

        self.progress_loop(append, data, progress,
                           message="Adding initial rows to batch")

    def populate_from_member_file(self, batch, progress=None):
        """
        Populate member batch from "member" CSV input data file.
        """
        input_path = batch.filepath(self.config, batch.input_file)
        input_file = open(input_path, 'rt')
        reader = csv.DictReader(input_file)
        data = list(reader)
        input_file.close()

        fields = [
            'first_name',
            'last_name',
            'member_type_id',
        ]

        batch.set_param('fields', fields)

        def append(csvrow, i):
            row = self.make_row()
            row.card_number = int(csvrow['signup_external_id'])
            row.first_name = csvrow['signup_first_name']
            row.last_name = csvrow['signup_last_name']
            row.member_type_id = int(csvrow['member_type'])
            self.add_row(batch, row)

        self.progress_loop(append, data, progress,
                           message="Adding initial rows to batch")

    def refresh_row(self, row):
        batch = row.batch

        # clear these first in case they are set
        row.first_name_old = None
        row.last_name_old = None
        row.street_old = None
        row.city_old = None
        row.state_old = None
        row.zipcode_old = None
        row.phone_old = None
        row.email1_old = None
        row.email2_old = None
        row.member_type_id_old = None
        row.status_text = None

        if not row.card_number:
            row.status_code = row.STATUS_MEMBER_NOT_FOUND
            row.status_text = "row has no card number"
            return

        core_member = self.core_session.get(corepos.MemberInfo, row.card_number)
        if not core_member:
            row.status_code = row.STATUS_MEMBER_NOT_FOUND
            row.status_text = "matching record not found in CORE"
            return

        core_customer = core_member.customers[0] if core_member.customers else None

        row.street_old = core_member.street
        row.city_old = core_member.city
        row.state_old = core_member.state
        row.zipcode_old = core_member.zip
        row.phone_old = core_member.phone
        row.email1_old = core_member.email
        row.email2_old = core_member.email2

        if core_customer:
            row.first_name_old = core_customer.first_name
            row.last_name_old = core_customer.last_name
            row.member_type_id_old = core_customer.member_type_id

        diffs = []
        fields = batch.get_param('fields')
        for field in fields:
            if getattr(row, field) != getattr(row, '{}_old'.format(field)):
                diffs.append(field)

        if diffs:
            row.status_code = row.STATUS_FIELDS_CHANGED
            row.status_text = ', '.join(diffs)
        else:
            row.status_code = row.STATUS_NO_CHANGE

    def describe_execution(self, batch, **kwargs):
        return ("CORE will be updated, by writing SQL directly to its DB, "
                "for each row indicating a change.  Note that this will "
                "affect one or both of the following tables:\n\n"
                "- `custdata`\n"
                "- `meminfo`")

    def execute(self, batch, progress=None, **kwargs):
        """
        Update the CORE DB with changes from the batch.
        """
        # we only want to process "update member" (changed) rows
        rows = [row for row in batch.active_rows()
                if row.status_code in (row.STATUS_FIELDS_CHANGED,)]
        if not rows:
            return True

        self.update_corepos(batch, rows, progress=progress)
        return True

    def update_corepos(self, batch, rows, progress=None):
        """
        For each of the given batch rows, this will update the CORE DB
        directly via SQL, for the fields which are specified in the
        batch params.
        """
        core_session = CoreSession()
        fields = batch.get_param('fields')

        def update(row, i):
            core_member = core_session.get(corepos.MemberInfo, row.card_number)
            if not core_member:
                log.warning("CORE member not found for row %s with card number: %s",
                            row.uuid, row.card_number)
                return

            if 'street' in fields:
                core_member.street = row.street
            if 'city' in fields:
                core_member.city = row.city
            if 'state' in fields:
                core_member.state = row.state
            if 'zipcode' in fields:
                core_member.zip = row.zipcode
            if 'phone' in fields:
                core_member.phone = row.phone
            if 'email1' in fields:
                core_member.email = row.email1

            core_customer = core_member.customers[0] if core_member.customers else None
            if core_customer:

                if 'first_name' in fields:
                    core_customer.first_name = row.first_name
                if 'last_name' in fields:
                    core_customer.last_name = row.last_name

            if 'member_type_id' in fields:
                for core_customer in core_member.customers:
                    core_customer.member_type_id = row.member_type_id

        self.progress_loop(update, rows, progress,
                           message="Updating members in CORE-POS")

        core_session.commit()
        core_session.close()
