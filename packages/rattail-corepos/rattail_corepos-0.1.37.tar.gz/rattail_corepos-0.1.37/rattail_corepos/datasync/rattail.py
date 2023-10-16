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
DataSync for Rattail DB
"""

from sqlalchemy import orm

from corepos.db.office_op import Session as CoreSession, model as corepos

from rattail.datasync import DataSyncImportConsumer


class FromCOREAPIToRattail(DataSyncImportConsumer):
    """
    Consumer for CORE POS (API) -> Rattail datasync
    """
    handler_spec = 'rattail_corepos.importing.corepos.api:FromCOREPOSToRattail'
    model_map = {
        'VendorItem': 'ProductCost',
    }

    def setup(self):
        super().setup()
        self.establish_api()

    def establish_api(self):
        self.api = self.app.get_corepos_handler().make_webapi()

    def pre_process_changes(self, session, changes):

        # declare user responsible
        if self.runas_username:
            session.set_continuum_user(self.runas_username)

        # update all importers with current Rattail session
        for importer in self.importers.values():
            importer.session = session
            importer.datasync_setup()

    def process_changes_proper(self, session, changes):

        # sync all Customer-related changes
        types = [
            'Member',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            if change.deletion:
                # normal logic works fine for this (maybe?)
                self.invoke_importer(session, change)
            else:
                # import member data from API, into various Rattail tables
                member = self.get_host_object(session, change)
                self.process_change(session, self.importers['Customer'],
                                    host_object=member)
                shoppers = self.importers['CustomerShopper'].get_shoppers_for_member(member)
                for shopper in shoppers:
                    self.process_change(session, self.importers['CustomerShopper'],
                                        host_object=shopper)
                self.process_change(session, self.importers['Member'],
                                    host_object=member)

        # sync all "product meta" changes
        types = [
            'Department',
            'Subdepartment',
            'Vendor',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            # normal logic works fine here
            self.invoke_importer(session, change)

        # sync all Product-related changes
        types = [
            'Product',
            'VendorItem',
        ]
        for change in [c for c in changes if c.payload_type in types]:

            # process deletion per usual logic
            if change.deletion:
                self.invoke_importer(session, change)
                if change.payload_type == 'Product':
                    continue # stop here if we just deleted a Product

            # try to process change for Product
            product = self.get_product(change)
            if product:
                self.process_change(session, self.importers['Product'],
                                    host_object=product)

        # sync all ProductCost-related changes
        types = [
            'VendorItem',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            # normal logic works fine here
            self.invoke_importer(session, change)

    def get_host_object(self, session, change):
        if change.payload_type == 'Member':
            return self.api.get_member(change.payload_key)
        if change.payload_type == 'Department':
            return self.api.get_department(change.payload_key)
        if change.payload_type == 'Subdepartment':
            return self.api.get_subdepartment(change.payload_key)
        if change.payload_type == 'Vendor':
            return self.api.get_vendor(change.payload_key)
        if change.payload_type == 'Product':
            return self.api.get_product(change.payload_key)
        if change.payload_type == 'VendorItem':
            fields = change.payload_key.split('|')
            if len(fields) == 2:
                sku, vendorID = fields
                if vendorID.isdigit():
                    return self.api.get_vendor_item(sku, int(vendorID))

    def get_product(self, change):
        if change.payload_type == 'Product':
            return self.api.get_product(change.payload_key)
        if change.payload_type == 'VendorItem':
            fields = change.payload_key.split('|')
            if len(fields) == 2:
                sku, vendorID = fields
                vendor_item = self.api.get_vendor_item(sku, vendorID)
                if vendor_item:
                    return self.api.get_product(vendor_item['upc'])


class FromCOREPOSToRattailBase(DataSyncImportConsumer):
    """
    Base class for CORE POS -> Rattail data sync consumers.
    """
    handler_spec = 'rattail_corepos.importing.corepos.db:FromCOREPOSToRattail'

    def begin_transaction(self):
        self.corepos_session = CoreSession()

    def rollback_transaction(self):
        self.corepos_session.rollback()
        self.corepos_session.close()

    def commit_transaction(self):
        # always rollback here, we don't want any accidents in CORE POS
        self.corepos_session.rollback()
        self.corepos_session.close()


class FromCOREPOSToRattailProducts(FromCOREPOSToRattailBase):
    """
    Handles CORE POS -> Rattail sync for product data.
    """

    def get_host_object(self, session, change):

        if change.payload_type == 'Product':
            try:
                return self.corepos_session.query(corepos.Product)\
                                           .filter(corepos.Product.upc == change.payload_key)\
                                           .one()
            except orm.exc.NoResultFound:
                pass

        else:
            # try to fetch CORE POS object via typical method
            Model = getattr(corepos, change.payload_type)
            return self.corepos_session.get(Model, int(change.payload_key))
