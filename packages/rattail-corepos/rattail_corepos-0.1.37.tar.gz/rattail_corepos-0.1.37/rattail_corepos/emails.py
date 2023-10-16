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
Email profiles for Rattail / CORE-POS integration
"""

from rattail.emails import ImporterEmail, ProblemReportEmail


class core_office_export_lane_op_updates(ImporterEmail):
    """
    Sent when a CORE Office -> CORE Lane export involves data changes.
    """
    handler_spec = 'rattail_corepos.corepos.lane.importing.op.office:FromCoreOfficeToCoreLane'
    abstract = False


class core_office_import_csv_updates(ImporterEmail):
    """
    Sent when CSV -> CORE import involves data changes.
    """
    handler_spec = 'rattail_corepos.corepos.office.importing.db.csv:FromCSVToCore'
    abstract = False


class corepos_problems_invalid_person_numbers(ProblemReportEmail):
    """
    Looks for `custdata` records with invalid person number sequence.
    """
    default_subject = "Invalid person numbers"
    abstract = False

    def sample_data(self, request):
        from corepos.db.office_op import model as corepos

        customer = corepos.CustomerClassic(card_number=42,
                                    first_name="Fred",
                                    last_name="Flintstone",
                                    person_number=2)
        return {
            'problems': [(customer, 1)]
        }


class corepos_problems_phone_numbers_too_long(ProblemReportEmail):
    """
    Looks for `meminfo` records with phone number which is too long to
    properly fit in the `Customers` table.
    """
    default_subject = "Phone numbers too long"
    abstract = False

    def sample_data(self, request):
        from corepos.db.office_op import model as corepos

        member = corepos.MemberInfo(card_number=42,
                                    phone='(800) 555-1234 ABCDEFGHIJKLMNOP')
        return {
            'problems': [member]
        }


class rattail_export_corepos_updates(ImporterEmail):
    """
    Sent when a Rattail -> CORE-POS API export involves data changes.
    """
    handler_spec = 'rattail_corepos.corepos.office.importing.rattail:FromRattailToCore'
    abstract = False


class rattail_import_corepos_api_updates(ImporterEmail):
    """
    Sent when a CORE-POS API -> Rattail import involves data changes.
    """
    handler_spec = 'rattail_corepos.importing.corepos.api:FromCOREPOSToRattail'
    abstract = False


class rattail_import_corepos_db_updates(ImporterEmail):
    """
    Sent when a CORE-POS DB -> Rattail import involves data changes.
    """
    handler_spec = 'rattail_corepos.importing.corepos.db:FromCOREPOSToRattail'
    abstract = False
