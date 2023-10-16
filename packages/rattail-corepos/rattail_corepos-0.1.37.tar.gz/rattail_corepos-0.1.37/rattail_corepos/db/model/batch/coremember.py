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
Schema for CORE member update batch
"""

import sqlalchemy as sa

from rattail.db import model
from rattail.db.core import filename_column


class CoreMemberBatch(model.BatchMixin, model.Base):
    """
    Hopefully generic batch for adding / updating member data in CORE.
    """
    batch_key = 'corepos_member'
    __tablename__ = 'batch_corepos_member'
    __batchrow_class__ = 'CoreMemberBatchRow'
    model_title = "CORE Member Batch"
    model_title_plural = "CORE Member Batches"

    STATUS_OK                           = 1
    STATUS_CANNOT_PARSE_FILE            = 2

    STATUS = {
        STATUS_OK                       : "ok",
        STATUS_CANNOT_PARSE_FILE        : "cannot parse file",
    }

    input_file = filename_column(nullable=True, doc="""
    Base name of the input data file.
    """)


class CoreMemberBatchRow(model.BatchRowMixin, model.Base):
    """
    Row of data within a CORE member batch.
    """
    __tablename__ = 'batch_corepos_member_row'
    __batch_class__ = CoreMemberBatch

    STATUS_NO_CHANGE                    = 1
    STATUS_MEMBER_NOT_FOUND             = 2
    STATUS_FIELDS_CHANGED               = 3

    STATUS = {
        STATUS_NO_CHANGE                : "no change",
        STATUS_MEMBER_NOT_FOUND         : "member not found",
        STATUS_FIELDS_CHANGED           : "update member",
    }

    card_number_raw = sa.Column(sa.String(length=20), nullable=True)
    card_number = sa.Column(sa.Integer(), nullable=True)

    first_name = sa.Column(sa.String(length=30), nullable=True)
    first_name_old = sa.Column(sa.String(length=30), nullable=True)
    last_name = sa.Column(sa.String(length=30), nullable=True)
    last_name_old = sa.Column(sa.String(length=30), nullable=True)

    street = sa.Column(sa.String(length=255), nullable=True)
    street_old = sa.Column(sa.String(length=255), nullable=True)
    city = sa.Column(sa.String(length=20), nullable=True)
    city_old = sa.Column(sa.String(length=20), nullable=True)
    state = sa.Column(sa.String(length=2), nullable=True)
    state_old = sa.Column(sa.String(length=2), nullable=True)
    zipcode = sa.Column(sa.String(length=10), nullable=True)
    zipcode_old = sa.Column(sa.String(length=10), nullable=True)

    phone = sa.Column(sa.String(length=30), nullable=True)
    phone_old = sa.Column(sa.String(length=30), nullable=True)

    email1 = sa.Column(sa.String(length=50), nullable=True)
    email1_old = sa.Column(sa.String(length=50), nullable=True)
    email2 = sa.Column(sa.String(length=50), nullable=True)
    email2_old = sa.Column(sa.String(length=50), nullable=True)

    member_type_id = sa.Column(sa.SmallInteger(), nullable=True)
    member_type_id_old = sa.Column(sa.SmallInteger(), nullable=True)
