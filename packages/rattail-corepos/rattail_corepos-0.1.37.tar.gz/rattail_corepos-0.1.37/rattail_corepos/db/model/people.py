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
Database schema extensions for CORE-POS integration
"""

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model


class CorePerson(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Person`.
    """
    __tablename__ = 'corepos_person'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['person.uuid'],
                                name='corepos_person_fk_person'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    person = orm.relationship(
        model.Person,
        doc="""
        Reference to the actual person record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this person.
            """))

    corepos_customer_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``Customers.customerID`` value for this person, within CORE-POS.
    """)

    def __str__(self):
        return str(self.person)

CorePerson.make_proxy(model.Person, '_corepos', 'corepos_customer_id')


class CoreEmployee(model.Base):
    """
    CORE-specific extensions to :class:`~rattail:rattail.db.model.Employee`
    """
    __tablename__ = 'corepos_employee'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['employee.uuid'],
                                name='corepos_employee_fk_employee'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    employee = orm.relationship(
        model.Employee,
        doc="""
        Reference to the actual employee record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this employee.
            """))

    corepos_number = sa.Column(sa.Integer(), nullable=True, doc="""
    ``employees.emp_no`` value for this employee, within CORE-POS.
    """)

    def __str__(self):
        return str(self.employee)

CoreEmployee.make_proxy(model.Employee, '_corepos', 'corepos_number')


class CoreCustomer(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Customer`.
    """
    __tablename__ = 'corepos_customer'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['customer.uuid'],
                                name='corepos_customer_fk_customer'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    customer = orm.relationship(
        model.Customer,
        doc="""
        Reference to the actual customer record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this customer.
            """))

    corepos_account_id = sa.Column(sa.Integer(), nullable=True, doc="""
    ``CustomerAccounts.customerAccountID`` value for this customer
    account, within CORE-POS.
    """)

    corepos_card_number = sa.Column(sa.Integer(), nullable=True, doc="""
    ``custdata.CardNo`` value for this customer, within CORE-POS.
    """)

    def __str__(self):
        return str(self.customer)

CoreCustomer.make_proxy(model.Customer, '_corepos', 'corepos_account_id')
CoreCustomer.make_proxy(model.Customer, '_corepos', 'corepos_card_number')


class CoreCustomerShopper(model.Base):
    """
    CORE-specific extensions to
    :class:`~rattail:rattail.db.model.CustomerShopper`.
    """
    __tablename__ = 'corepos_customer_shopper'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['customer_shopper.uuid'],
                                name='corepos_customer_shopper_fk_shopper'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    shopper = orm.relationship(
        model.CustomerShopper, doc="""
        Reference to the actual shopper record, which this one extends.
        """,
        cascade_backrefs=False,
        backref=orm.backref(
            '_corepos', doc="""
            Reference to the CORE-POS extension record for this customer.
            """,
            uselist=False,
            cascade='all, delete-orphan',
            cascade_backrefs=False))

    # please note, there is *not* a unique constraint on this field.
    # that is intentional, for now, to give some breathing room for
    # testing etc.
    corepos_customer_id = sa.Column(sa.Integer(), nullable=True, doc="""
    ``Customers.customerID`` value for this shopper, within CORE-POS.
    """)

    def __str__(self):
        return str(self.shopper)

CoreCustomerShopper.make_proxy(model.CustomerShopper, '_corepos', 'corepos_customer_id')


class CoreMember(model.Base):
    """
    CORE-specific extensions to :class:`rattail:rattail.db.model.Member`.
    """
    __tablename__ = 'corepos_member'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['member.uuid'],
                                name='corepos_member_fk_member'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    member = orm.relationship(
        model.Member,
        doc="""
        Reference to the actual member record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this member.
            """))

    corepos_account_id = sa.Column(sa.Integer(), nullable=False, doc="""
    ``Customers.customerAccountID`` value for this member, within CORE-POS.
    """)

    def __str__(self):
        return str(self.member)

CoreMember.make_proxy(model.Member, '_corepos', 'corepos_account_id')


class CoreMemberEquityPayment(model.Base):
    """
    CORE-specific extensions to
    :class:`~rattail:rattail.db.model.MemberEquityPayment`.
    """
    __tablename__ = 'corepos_member_equity_payment'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['member_equity_payment.uuid'],
                                name='corepos_member_equity_payment_fk_payment'),
    )
    __versioned__ = {}

    uuid = model.uuid_column(default=None)
    payment = orm.relationship(
        model.MemberEquityPayment,
        doc="""
        Reference to the actual payment record, which this one extends.
        """,
        backref=orm.backref(
            '_corepos',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the CORE-POS extension record for this payment.
            """))

    corepos_card_number = sa.Column(sa.Integer(), nullable=False, doc="""
    ``stockpurchases.card_no`` value for this payment, within CORE-POS.
    """)

    corepos_transaction_number = sa.Column(sa.String(length=50), nullable=True, doc="""
    ``stockpurchases.trans_num`` value for this payment, within CORE-POS.
    """)

    corepos_transaction_id = sa.Column(sa.Integer(), nullable=True, doc="""
    ``stockpurchases.trans_id`` value for this payment, within CORE-POS.
    """)

    corepos_department_number = sa.Column(sa.Integer(), nullable=True, doc="""
    ``stockpurchases.dept`` value for this payment, within CORE-POS.
    """)

    corepos_datetime = sa.Column(sa.DateTime(), nullable=True, doc="""
    ``stockpurchases.datetime`` value for this payment, within CORE-POS.
    """)

    def __str__(self):
        return str(self.payment)

CoreMemberEquityPayment.make_proxy(model.MemberEquityPayment, '_corepos', 'corepos_card_number')
CoreMemberEquityPayment.make_proxy(model.MemberEquityPayment, '_corepos', 'corepos_transaction_number')
CoreMemberEquityPayment.make_proxy(model.MemberEquityPayment, '_corepos', 'corepos_transaction_id')
CoreMemberEquityPayment.make_proxy(model.MemberEquityPayment, '_corepos', 'corepos_department_number')
CoreMemberEquityPayment.make_proxy(model.MemberEquityPayment, '_corepos', 'corepos_datetime')
