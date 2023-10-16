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
Problem reports for CORE-POS
"""

from corepos.db.office_op import Session as CoreSession, model as corepos

from rattail.problems import ProblemReport


class InvalidPersonNumbers(ProblemReport):
    """
    Looks for `custdata` records in CORE which have invalid person
    number sequence.
    """
    system_key = 'corepos'
    problem_key = 'invalid_person_numbers'
    problem_title = "Invalid person numbers"

    def find_problems(self, **kwargs):
        problems = []
        core_session = CoreSession()

        core_members = core_session.query(corepos.MemberInfo)\
                                   .order_by(corepos.MemberInfo.card_number)\
                                   .all()

        def inspect(member, i):
            for j, customer in enumerate(member.customers, 1):
                if customer.person_number != j:
                    problems.append((customer, j))

        self.progress_loop(inspect, core_members,
                           message="Looking for invalid person numbers")

        core_session.close()
        return problems


class PhoneNumbersTooLong(ProblemReport):
    """
    Looks for ``meminfo`` records in CORE which have a phone number
    value which is too long to fit into the corresponding
    ``Customers`` table column in CORE.
    """
    system_key = 'corepos'
    problem_key = 'phone_numbers_too_long'
    problem_title = "Phone numbers too long"

    def find_problems(self, **kwargs):
        problems = []
        core_session = CoreSession()

        maxlen = self.app.maxlen(corepos.Customer.phone)
        core_members = core_session.query(corepos.MemberInfo)\
                                   .order_by(corepos.MemberInfo.card_number)\
                                   .all()

        def inspect(member, i):
            if member.phone and len(member.phone) > maxlen:
                problems.append(member)

        self.progress_loop(inspect, core_members,
                           message="Looking for phone numbers too long")
        core_session.close()
        return problems
