# -*- coding: utf-8; -*-
"""add card_number_raw for member import

Revision ID: d6a0f21a6a94
Revises: 50961b4b854a
Create Date: 2022-03-15 11:24:41.764317

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = 'd6a0f21a6a94'
down_revision = '50961b4b854a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_corepos_member_row
    op.add_column('batch_corepos_member_row', sa.Column('card_number_raw', sa.String(length=20), nullable=True))


def downgrade():

    # batch_corepos_member_row
    op.drop_column('batch_corepos_member_row', 'card_number_raw')
