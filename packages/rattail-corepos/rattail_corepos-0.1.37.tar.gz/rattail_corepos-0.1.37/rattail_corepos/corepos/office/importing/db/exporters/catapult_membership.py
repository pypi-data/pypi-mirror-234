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
CORE-POS -> Catapult Membership Workbook
"""

import decimal
import logging
from collections import OrderedDict

from sqlalchemy import orm

from corepos.db.office_op import model as corepos

from rattail.importing.handlers import ToFileHandler
from rattail.time import localtime
from rattail.excel import ExcelReader
from rattail_corepos.corepos.importing.db.corepos import FromCoreHandler, FromCore
from rattail_onager.catapult.importing import membership as catapult_importing


log = logging.getLogger(__name__)


class FromCoreToCatapult(FromCoreHandler, ToFileHandler):
    """
    Handler for CORE -> Catapult (Membership Workbook)
    """
    host_title = "CORE-POS"
    local_title = "Catapult (Membership Workbook)"
    direction = 'export'

    def get_importers(self):
        importers = OrderedDict()
        importers['Member'] = MemberImporter
        return importers


class MemberImporter(FromCore, catapult_importing.model.MemberImporter):
    """
    Member data importer.
    """
    host_model_class = corepos.CustomerClassic
    supported_fields = [
        'member_id',
        'first_name',
        'last_name',
        'address_1',
        'address_2',
        'city',
        'state',
        'zip_code',
        'phone_number',
        'email',
        'member_notes',
        'member_join_date',
        'family_affiliation',
        'account_number',
        'membership_profile_name',
    ]

    def setup(self):
        super(MemberImporter, self).setup()

        self.warn_truncated_field = self.config.getbool(
            'corepos', 'exporting.catapult_membership.warn_truncated_field',
            default=True)

        self.cache_membership_profiles()

    def cache_membership_profiles(self):
        self.membership_profiles = {}
        sheet_name = self.config.get('catapult', 'membership_profiles_worksheet_name',
                                     default="Membership Profile details")
        reader = ExcelReader(self.workbook_template_path, sheet_name=sheet_name)
        for profile in reader.read_rows(progress=self.progress):
            if profile['Equity Paid in Full Amount']:
                profile['Equity Paid in Full Amount'] = decimal.Decimal(profile['Equity Paid in Full Amount'])
            self.membership_profiles[profile['Membership Profile Name']] = profile

        # also figure out which profile is default
        self.default_membership_profile = None
        for profile in self.membership_profiles.values():
            if profile['Please indicate Default Profile'] == 'X':
                self.default_membership_profile = profile
                break
        if not self.default_membership_profile:
            raise RuntimeError("cannot determine default membership profile")

    def query(self):
        return self.host_session.query(corepos.CustomerClassic)\
                                .order_by(corepos.CustomerClassic.card_number,
                                          corepos.CustomerClassic.person_number,
                                          corepos.CustomerClassic.id)\
                                .options(orm.joinedload(corepos.CustomerClassic.member_type))\
                                .options(orm.joinedload(corepos.CustomerClassic.member_info)\
                                         .joinedload(corepos.MemberInfo.dates))\
                                .options(orm.joinedload(corepos.CustomerClassic.member_info)\
                                         .joinedload(corepos.MemberInfo.notes))

    def normalize_host_object(self, custdata):

        if custdata.person_number == 1:
            family_affiliation = False
        elif custdata.person_number > 1:
            family_affiliation = True
        else:
            log.warning("member #%s has unexpected person_number (%s): %s",
                        custdata.card_number, custdata.person_number, custdata)
            family_affiliation = False

        if custdata.member_type:
            membership_profile_name = custdata.member_type.description
        else:
            log.warning("member #%s has no member type: %s",
                        custdata.card_number, custdata)
            membership_profile_name = self.default_membership_profile['Membership Profile Name']

        data = {
            'member_id': str(custdata.id),
            'first_name': custdata.first_name,
            'last_name': custdata.last_name,

            # these will be blank unless we have an associated `meminfo` record
            'phone_number': None,
            'email': None,
            'address_1': None,
            'address_2': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'member_join_date': None,
            'member_notes': None,

            'family_affiliation': family_affiliation,
            'account_number': str(custdata.card_number),
            'membership_profile_name': membership_profile_name,
        }

        info = custdata.member_info
        if info:
            data['phone_number'] = info.phone
            data['email'] = info.email
            data['address_1'], data['address_2'] = info.split_street()
            data['city'] = info.city
            data['state'] = info.state
            data['zip_code'] = info.zip

            if info.dates:
                if len(info.dates) > 1:
                    log.warning("member #%s has multiple (%s) `memDates` records: %s",
                                custdata.card_number, len(info.dates), custdata)
                dates = info.dates[0]
                if dates.start_date:
                    start_date = localtime(self.config, dates.start_date).date()
                    data['member_join_date'] = start_date.strftime('%Y-%m-%d')

            if info.notes:
                notes = []
                for note in reversed(info.notes): # show most recent first
                    text = str(note.note or '').strip() or None
                    if text:
                        notes.append(text)
                if notes:
                    data['member_notes'] = '\n'.join(notes)

        return data
