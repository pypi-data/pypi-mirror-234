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
DataSync for CORE POS
"""

import sqlalchemy as sa

from corepos.db.office_op import Session as CoreSession, model as corepos

from rattail.db import model
from rattail.datasync import DataSyncWatcher, DataSyncImportConsumer


class CoreOfficeOpWatcher(DataSyncWatcher):
    """
    DataSync watcher for the CORE ``office_op`` database.
    """
    prunes_changes = True

    def __init__(self, *args, **kwargs):
        super(CoreOfficeOpWatcher, self).__init__(*args, **kwargs)

        self.changes_table_name = kwargs.get('changes_table_name',
                                             'datasync_changes')

        self.corepos_metadata = sa.MetaData()
        self.corepos_changes = sa.Table(
            self.changes_table_name, self.corepos_metadata,
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('object_type', sa.String(length=255), nullable=False),
            sa.Column('object_key', sa.String(length=255), nullable=False),
            sa.Column('deleted', sa.Boolean(), nullable=False, default=False))

    def get_changes(self, lastrun):
        session = CoreSession()
        result = session.execute(self.corepos_changes.select())
        changes = result.fetchall()
        session.close()
        if changes:
            return [
                (c.id,
                 model.DataSyncChange(
                     payload_type=c.object_type,
                     payload_key=c.object_key,
                     deletion=c.deleted))
                for c in changes]

    def prune_changes(self, keys):
        deleted = 0
        session = CoreSession()
        for key in keys:
            result = session.execute(self.corepos_changes.select()\
                                     .where(self.corepos_changes.c.id == key))
            if result.fetchall():
                session.execute(self.corepos_changes.delete()\
                                .where(self.corepos_changes.c.id == key))
                deleted += 1
        session.commit()
        session.close()
        return deleted


class COREPOSProductWatcher(DataSyncWatcher):
    """
    DataSync watcher for the CORE POS database.
    """

    def get_changes(self, lastrun):
        if not lastrun:
            return

        changes = []
        session = CoreSession()
        lastrun = self.localize_lastrun(session, lastrun)

        # Department
        departments = session.query(corepos.Department)\
                             .filter(corepos.Department.modified >= lastrun)\
                             .all()
        if departments:
            changes.extend([
                (None,
                 model.DataSyncChange(
                     payload_type='Department',
                     payload_key=str(dept.number)))
                for dept in departments])

        # TODO: subdepartment table doesn't have a modified flag?
        # # Subdepartment
        # subdepartments = session.query(corepos.Subdepartment)\
        #                         .filter(corepos.Subdepartment.modified >= lastrun)\
        #                         .all()
        # if subdepartments:
        #     changes.extend([
        #         (None,
        #          model.DataSyncChange(
        #              payload_type='Subdepartment',
        #              payload_key=six.text_type(subdept.subdept_no)))
        #         for subdept in subdepartments])

        # TODO: vendor table doesn't have a modified flag?
        # # Vendor
        # vendors = session.query(corepos.Vendor)\
        #                  .filter(corepos.Vendor.modified >= lastrun)\
        #                  .all()
        # if vendors:
        #     changes.extend([
        #         (None,
        #          model.DataSyncChange(
        #              payload_type='Vendor',
        #              payload_key=six.text_type(vendor.vendorID)))
        #         for vendor in vendors])

        # Product
        products = session.query(corepos.Product)\
                          .filter(corepos.Product.modified >= lastrun)\
                          .all()
        if products:
            changes.extend([
                (None,
                 model.DataSyncChange(
                     payload_type='Product',
                     payload_key=product.upc))
                for product in products
                if product.upc])

        session.close()
        return changes


class FromRattailToCore(DataSyncImportConsumer):
    """
    Rattail -> CORE POS datasync consumer
    """
    handler_spec = 'rattail_corepos.corepos.importing.rattail:FromRattailToCore'

    def process_changes(self, session, changes):
        """
        Process all the given changes, coming from Rattail.
        """
        # TODO: this probably doesn't accomplish anything here?
        if self.runas_username:
            session.set_continuum_user(self.runas_username)

        # update all importers with current session
        for importer in self.importers.values():
            importer.host_session = session
            # also establish the API client for each!
            importer.establish_api()

        # sync all Member changes
        types = [
            'Customer',
            'CustomerShopper',
            'Person',
            'CustomerPerson',
            'CustomerMailingAddress',
            'PersonPhoneNumber',
            'PersonEmailAddress',
            'Member',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            if change.payload_type == 'Customer' and change.deletion:
                # # just do default logic for this one
                # self.invoke_importer(session, change)
                # TODO: we have no way to delete a CORE customer via API, right?
                pass
            else: # we consider this an "add/update"
                customers = self.get_customers(session, change)
                for customer in customers:
                    self.process_change(session, self.importers['Member'],
                                        host_object=customer)

        # sync all Vendor changes
        types = [
            'Vendor',
            'VendorPhoneNumber',
            'VendorEmailAddress',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            if change.payload_type == 'Vendor' and change.deletion:
                # # just do default logic for this one
                # self.invoke_importer(session, change)
                # TODO: we have no way to delete a CORE vendor via API, right?
                pass
            else: # we consider this an "add/update"
                vendor = self.get_vendor(session, change)
                if vendor:
                    self.process_change(session, self.importers['Vendor'],
                                        host_object=vendor)

        # sync all Product changes
        types = [
            'Product',
            'ProductPrice',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            if change.payload_type == 'Product' and change.deletion:
                # # just do default logic for this one
                # self.invoke_importer(session, change)
                # TODO: we have no way to delete a CORE product via API, right?
                pass
            else: # we consider this an "add/update"
                product = self.get_product(session, change)
                if product:
                    self.process_change(session, self.importers['Product'],
                                        host_object=product)

        # process all remaining supported models with typical logic
        types = [
            'Department',
            'Subdepartment',
        ]
        for change in [c for c in changes if c.payload_type in types]:
            self.invoke_importer(session, change)

    def get_host_object(self, session, change):
        return session.get(getattr(model, change.payload_type), change.payload_key)

    def get_customers(self, session, change):
        clientele = self.app.get_clientele_handler()

        if change.payload_type == 'Customer':
            customer = session.get(model.Customer, change.payload_key)
            if customer:
                return [customer]

        elif change.payload_type == 'CustomerShopper':
            shopper = session.get(model.CustomerShopper, change.payload_key)
            if shopper:
                return [shopper.customer]

        elif change.payload_type == 'CustomerPerson':
            cp = session.get(model.CustomerPerson, change.payload_key)
            if cp:
                return [cp.customer]

        elif change.payload_type == 'Person':
            person = session.get(model.Person, change.payload_key)
            if person:
                return clientele.get_customers_for_account_holder(person)

        elif change.payload_type == 'CustomerMailingAddress':
            address = session.get(model.CustomerMailingAddress, change.payload_key)
            if address:
                return [address.customer]

        elif change.payload_type == 'PersonPhoneNumber':
            phone = session.get(model.PersonPhoneNumber, change.payload_key)
            if phone:
                return clientele.get_customers_for_account_holder(phone.person)

        elif change.payload_type == 'PersonEmailAddress':
            email = session.get(model.PersonEmailAddress, change.payload_key)
            if email:
                return clientele.get_customers_for_account_holder(email.person)

        elif change.payload_type == 'Member':
            member = session.get(model.Member, change.payload_key)
            if member:
                return [member.customer]

        return []

    def get_vendor(self, session, change):

        if change.payload_type == 'Vendor':
            return session.get(model.Vendor, change.payload_key)

        if change.payload_type == 'VendorPhoneNumber':
            phone = session.get(model.VendorPhoneNumber, change.payload_key)
            if phone:
                return phone.vendor

        if change.payload_type == 'VendorEmailAddress':
            email = session.get(model.VendorEmailAddress, change.payload_key)
            if email:
                return email.vendor

    def get_product(self, session, change):

        if change.payload_type == 'Product':
            return session.get(model.Product, change.payload_key)

        if change.payload_type == 'ProductPrice':
            price = session.get(model.ProductPrice, change.payload_key)
            if price:
                return price.product
