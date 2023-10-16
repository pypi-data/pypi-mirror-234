# -*- coding: utf-8; -*-
"""add CustomerShopper.corepos_customer_id

Revision ID: b025df7cf41b
Revises: ae74c537ea51
Create Date: 2023-06-10 13:24:40.735959

"""

# revision identifiers, used by Alembic.
revision = 'b025df7cf41b'
down_revision = 'ae74c537ea51'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_customer_shopper
    op.create_table('corepos_customer_shopper',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_customer_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['uuid'], ['customer_shopper.uuid'], name='corepos_customer_shopper_fk_shopper'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('corepos_customer_shopper_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_customer_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_corepos_customer_shopper_version_end_transaction_id'), 'corepos_customer_shopper_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_customer_shopper_version_operation_type'), 'corepos_customer_shopper_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_customer_shopper_version_transaction_id'), 'corepos_customer_shopper_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_customer_shopper
    op.drop_index(op.f('ix_corepos_customer_shopper_version_transaction_id'), table_name='corepos_customer_shopper_version')
    op.drop_index(op.f('ix_corepos_customer_shopper_version_operation_type'), table_name='corepos_customer_shopper_version')
    op.drop_index(op.f('ix_corepos_customer_shopper_version_end_transaction_id'), table_name='corepos_customer_shopper_version')
    op.drop_table('corepos_customer_shopper_version')
    op.drop_table('corepos_customer_shopper')
