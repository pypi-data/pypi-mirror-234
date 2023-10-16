# -*- coding: utf-8; -*-
"""add equity_payment.corepos_datetime

Revision ID: d426a274f0c2
Revises: 93978a7adc66
Create Date: 2023-09-13 20:59:42.706994

"""

# revision identifiers, used by Alembic.
revision = 'd426a274f0c2'
down_revision = '93978a7adc66'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_member_equity_payment
    op.add_column('corepos_member_equity_payment', sa.Column('corepos_datetime', sa.DateTime(), nullable=True))
    op.add_column('corepos_member_equity_payment_version', sa.Column('corepos_datetime', sa.DateTime(), autoincrement=False, nullable=True))


def downgrade():

    # corepos_member_equity_payment
    op.drop_column('corepos_member_equity_payment_version', 'corepos_datetime')
    op.drop_column('corepos_member_equity_payment', 'corepos_datetime')
