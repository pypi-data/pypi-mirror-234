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
Auth Handler for use with CORE-POS
"""

from sqlalchemy import orm

from rattail import auth as base


class CoreAuthHandler(base.AuthHandler):
    """
    Custom auth handler for use with CORE-POS.
    """

    def authenticate_user(self, session, username, password):
        model = self.model

        # first try default logic, if it works then great
        user = super().authenticate_user(session, username, password)
        if user:
            return user

        # only if configured, we also check CORE-POS credentials
        if self.config.getbool('rattail.auth', 'corepos.check_cashier_credentials',
                               default=False):
            user = None
            core_session = self.app.get_corepos_handler().make_session_office_op()
            core_employee = self.check_corepos_cashier_credentials(core_session, password)
            if core_employee:
                user = self.get_user_from_corepos_employee(session, core_employee)
            core_session.close()
            if user and user.active:
                return user

    def check_corepos_cashier_credentials(self, core_session, password):
        core_op = self.app.get_corepos_handler().get_model_office_op()

        try:
            core_employee = core_session.query(core_op.Employee)\
                                        .filter(core_op.Employee.cashier_password == password)\
                                        .one()
        except orm.exc.NoResultFound:
            pass
        else:
            if core_employee.active:
                return core_employee

    def get_user_from_corepos_employee(self, session, core_employee):
        model = self.model
        try:
            employee = session.query(model.Employee)\
                              .join(model.CoreEmployee)\
                              .filter(model.CoreEmployee.corepos_number == core_employee.number)\
                              .one()
        except orm.exc.NoResultFound:
            pass
        else:
            return self.app.get_user(employee)
