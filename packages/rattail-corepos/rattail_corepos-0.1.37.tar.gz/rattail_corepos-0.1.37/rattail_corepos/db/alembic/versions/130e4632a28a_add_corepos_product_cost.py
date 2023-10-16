# -*- coding: utf-8 -*-
"""add corepos_product_cost

Revision ID: 130e4632a28a
Revises: 9c5029effe93
Create Date: 2020-09-04 18:30:17.041521

"""

# revision identifiers, used by Alembic.
revision = '130e4632a28a'
down_revision = '9c5029effe93'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_product_cost
    op.create_table('corepos_product_cost',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['product_cost.uuid'], name='corepos_product_cost_fk_cost'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_product_cost_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_product_cost_version_end_transaction_id'), 'corepos_product_cost_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_product_cost_version_operation_type'), 'corepos_product_cost_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_product_cost_version_transaction_id'), 'corepos_product_cost_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_product_cost
    op.drop_index(op.f('ix_corepos_product_cost_version_transaction_id'), table_name='corepos_product_cost_version')
    op.drop_index(op.f('ix_corepos_product_cost_version_operation_type'), table_name='corepos_product_cost_version')
    op.drop_index(op.f('ix_corepos_product_cost_version_end_transaction_id'), table_name='corepos_product_cost_version')
    op.drop_table('corepos_product_cost_version')
    op.drop_table('corepos_product_cost')
