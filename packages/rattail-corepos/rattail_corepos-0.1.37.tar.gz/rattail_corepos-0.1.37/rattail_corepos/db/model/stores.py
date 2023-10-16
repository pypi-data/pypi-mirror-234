# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
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
Database schema extensions for CORE-POS integration
"""

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model


class CoreStore(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Store`.
    """
    __tablename__ = 'corepos_store'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['store.uuid'],
                                name='corepos_store_fk_store'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    store = orm.relationship(
        model.Store,
        doc="""
        Reference to the actual store record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this store.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``Stores.storeID`` value for this store, within CORE-POS.
    """)

    def __str__(self):
        return str(self.store)

CoreStore.make_proxy(model.Store, '_corepos', 'corepos_id')


class CoreTax(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Tax`.
    """
    __tablename__ = 'corepos_tax'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['tax.uuid'],
                                name='corepos_tax_fk_tax'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    tax = orm.relationship(
        model.Tax,
        doc="""
        Reference to the actual tax record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this tax.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``taxrates.id`` value for this tax, within CORE-POS.
    """)

    def __str__(self):
        return str(self.tax)

CoreTax.make_proxy(model.Tax, '_corepos', 'corepos_id')


class CoreTender(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Tender`.
    """
    __tablename__ = 'corepos_tender'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['tender.uuid'],
                                name='corepos_tender_fk_tender'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    tender = orm.relationship(
        model.Tender,
        doc="""
        Reference to the actual tender record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this tender.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``tenders.TenderID`` value for this tender, within CORE-POS.
    """)

    def __str__(self):
        return str(self.tender)

CoreTender.make_proxy(model.Tender, '_corepos', 'corepos_id')
