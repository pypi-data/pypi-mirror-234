# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2020 Lance Edgar
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


class CoreDepartment(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Department`.
    """
    __tablename__ = 'corepos_department'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['department.uuid'],
                                name='corepos_department_fk_department'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    department = orm.relationship(
        model.Department,
        doc="""
        Reference to the actual department record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this department.
            """))

    corepos_number = sa.Column(sa.Integer(), nullable=False, doc="""
    ``dept_no`` value for the department, within CORE-POS.
    """)

    def __str__(self):
        return str(self.department)

CoreDepartment.make_proxy(model.Department, '_corepos', 'corepos_number')


class CoreSubdepartment(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Subdepartment`.
    """
    __tablename__ = 'corepos_subdepartment'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['subdepartment.uuid'],
                                name='corepos_subdepartment_fk_subdepartment'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    subdepartment = orm.relationship(
        model.Subdepartment,
        doc="""
        Reference to the actual subdepartment record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this subdepartment.
            """))

    corepos_number = sa.Column(sa.Integer(), nullable=False, doc="""
    ``subdept_no`` value for the subdepartment, within CORE-POS.
    """)

    def __str__(self):
        return str(self.subdepartment)

CoreSubdepartment.make_proxy(model.Subdepartment, '_corepos', 'corepos_number')


class CoreVendor(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Vendor`.
    """
    __tablename__ = 'corepos_vendor'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['vendor.uuid'],
                                name='corepos_vendor_fk_vendor'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    vendor = orm.relationship(
        model.Vendor,
        doc="""
        Reference to the actual vendor record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this vendor.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``vendorID`` value for the vendor, within CORE-POS.
    """)

    def __str__(self):
        return str(self.vendor)

CoreVendor.make_proxy(model.Vendor, '_corepos', 'corepos_id')


class CoreProduct(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Product`.
    """
    __tablename__ = 'corepos_product'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['product.uuid'],
                                name='corepos_product_fk_product'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    product = orm.relationship(
        model.Product,
        doc="""
        Reference to the actual product record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this product.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``id`` value for the product, within CORE-POS.
    """)

    def __str__(self):
        return str(self.product)

CoreProduct.make_proxy(model.Product, '_corepos', 'corepos_id')


class CoreProductCost(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.ProductCost`.
    """
    __tablename__ = 'corepos_product_cost'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['product_cost.uuid'],
                                name='corepos_product_cost_fk_cost'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    cost = orm.relationship(
        model.ProductCost,
        doc="""
        Reference to the actual ProductCost record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this product cost.
            """))

    corepos_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``vendorItemID`` value for the corresponding record within CORE-POS.
    """)

    def __str__(self):
        return str(self.cost)

CoreProductCost.make_proxy(model.ProductCost, '_corepos', 'corepos_id')
