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
Schema for CORE equity import batch
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr

from rattail.db import model


class CoreEquityImportBatch(model.BatchMixin, model.Base):
    """
    Hopefully generic batch for CORE equity import
    """
    batch_key = 'corepos_equity_import'
    __tablename__ = 'batch_corepos_equity_import'
    __batchrow_class__ = 'CoreEquityImportBatchRow'
    model_title = "CORE-POS Equity Import Batch"
    model_title_plural = "CORE-POS Equity Import Batches"

    STATUS_OK                           = 1

    STATUS = {
        STATUS_OK                       : "ok",
    }


class CoreEquityImportBatchRow(model.BatchRowMixin, model.Base):
    """
    Row of data within a CORE equity import batch.
    """
    __tablename__ = 'batch_corepos_equity_import_row'
    __batch_class__ = CoreEquityImportBatch

    @declared_attr
    def __table_args__(cls):
        return cls.__default_table_args__() + (
            sa.ForeignKeyConstraint(['payment_uuid'], ['member_equity_payment.uuid'],
                                    name='batch_corepos_equity_import_row_fk_payment'),
            sa.ForeignKeyConstraint(['member_uuid'], ['member.uuid'],
                                    name='batch_corepos_equity_import_row_fk_member'),
        )

    STATUS_OK                           = 1
    STATUS_MEMBER_NOT_FOUND             = 2
    STATUS_MISSING_VALUES               = 3
    STATUS_NEEDS_ATTENTION              = 4
    STATUS_ALREADY_IN_CORE              = 5
    STATUS_EQUITY_OVERPAID              = 6

    STATUS = {
        STATUS_OK                       : "ok",
        STATUS_MEMBER_NOT_FOUND         : "member not found",
        STATUS_MISSING_VALUES           : "missing values",
        STATUS_NEEDS_ATTENTION          : "needs attention",
        STATUS_ALREADY_IN_CORE          : "already in CORE-POS",
        STATUS_EQUITY_OVERPAID          : "equity overpaid",
    }

    payment_uuid = sa.Column(sa.String(length=32), nullable=True)
    payment = orm.relationship(model.MemberEquityPayment)

    member_uuid = sa.Column(sa.String(length=32), nullable=True)
    member = orm.relationship(model.Member)

    card_number = sa.Column(sa.Integer(), nullable=True)
    first_name = sa.Column(sa.String(length=30), nullable=True)
    last_name = sa.Column(sa.String(length=30), nullable=True)
    member_type_id = sa.Column(sa.Integer(), nullable=True)
    payment_amount = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)
    department_number = sa.Column(sa.Integer(), nullable=True)
    tender_code = sa.Column(sa.String(length=2), nullable=True)
    timestamp = sa.Column(sa.DateTime(), nullable=True)
    corepos_equity_total = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)
    rattail_equity_total = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)
    other_equity_total = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)
