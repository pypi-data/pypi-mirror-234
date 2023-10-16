# -*- coding: utf-8; -*-
"""add customer.card_number

Revision ID: ae74c537ea51
Revises: d6a0f21a6a94
Create Date: 2023-06-05 19:04:25.574077

"""

# revision identifiers, used by Alembic.
revision = 'ae74c537ea51'
down_revision = 'd6a0f21a6a94'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_customer
    op.alter_column('corepos_customer', 'corepos_account_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('corepos_customer', sa.Column('corepos_card_number', sa.Integer(), nullable=True))
    op.add_column('corepos_customer_version', sa.Column('corepos_card_number', sa.Integer(), autoincrement=False, nullable=True))


def downgrade():

    # corepos_customer
    op.drop_column('corepos_customer_version', 'corepos_card_number')
    op.drop_column('corepos_customer', 'corepos_card_number')
    op.alter_column('corepos_customer', 'corepos_account_id',
               existing_type=sa.INTEGER(),
               nullable=False)
