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
App Handler supplement
"""

from rattail.app import RattailProvider, GenericHandler


class CoreProvider(RattailProvider):
    """
    App provider for CORE-POS integration.
    """

    def get_corepos_handler(self, **kwargs):
        if not hasattr(self, 'corepos_handler'):
            spec = self.config.get('rattail', 'corepos.handler',
                                   default='rattail_corepos.app:CoreHandler')
            factory = self.load_object(spec)
            self.corepos_handler = factory(self.config, **kwargs)
        return self.corepos_handler


class CoreHandler(GenericHandler):
    """
    Handler for CORE-POS integration.
    """

    def get_model_office_op(self, **kwargs):
        from corepos.db.office_op import model
        return model

    def get_model_office_trans(self, **kwargs):
        from corepos.db.office_trans import model
        return model

    def make_session_office_op(self, dbkey='default', **kwargs):
        from corepos.db.office_op import Session
        if 'bind' not in kwargs:
            kwargs['bind'] = self.config.core_office_op_engines[dbkey]
        return Session(**kwargs)

    def make_session_office_trans(self, **kwargs):
        from corepos.db.office_trans import Session
        return Session(**kwargs)

    def get_office_url(
            self,
            require=False,
            **kwargs):
        """
        Returns the base URL for the CORE Office web app.
        """
        getter = self.config.require if require else self.config.get
        url = getter('corepos', 'office.url')
        if url:
            return url.rstrip('/')

    def get_office_member_url(
            self,
            card_number,
            office_url=None,
            require=False,
            **kwargs):
        """
        Returns the CORE Office URL for the customer account with the
        given card number.
        """
        if not office_url:
            office_url = self.get_office_url(require=require)
        if office_url:
            return f'{office_url}/mem/MemberEditor.php?memNum={card_number}'

    # TODO: deprecate / remove this
    get_office_customer_account_url = get_office_member_url

    def get_office_employee_url(
            self,
            employee_number,
            office_url=None,
            require=False,
            **kwargs):
        """
        Returns the CORE Office URL for the employee with the given
        number.
        """
        if not office_url:
            office_url = self.get_office_url(require=require)
        if office_url:
            return f'{office_url}/admin/Cashiers/CashierEditor.php?emp_no={employee_number}'

    def get_office_product_url(
            self,
            upc,
            office_url=None,
            require=False,
            **kwargs):
        """
        Returns the CORE Office URL for the product with the given
        UPC.
        """
        if not office_url:
            office_url = self.get_office_url(require=require)
        if office_url:
            return f'{office_url}/item/ItemEditorPage.php?searchupc={upc}'

    def get_office_vendor_url(
            self,
            id,
            office_url=None,
            require=False,
            **kwargs):
        """
        Returns the CORE Office URL for the vendor with the given ID.
        """
        if not office_url:
            office_url = self.get_office_url(require=require)
        if office_url:
            return f'{office_url}/item/vendors/VendorIndexPage.php?vid={id}'

    def make_webapi(self):
        """
        Make and return a new CORE-POS API client object.
        """

        spec = self.config.get('corepos.api', 'factory',
                               default='corepos.api:CoreWebAPI')
        factory = self.app.load_object(spec)

        url = self.config.require('corepos.api', 'url')

        kwargs = {}
        username = self.config.get('corepos.api', 'htdigest.username')
        password = self.config.get('corepos.api', 'htdigest.password')
        if username and password:
            kwargs['htdigest_username'] = username
            kwargs['htdigest_password'] = password

        return factory(url, **kwargs)
