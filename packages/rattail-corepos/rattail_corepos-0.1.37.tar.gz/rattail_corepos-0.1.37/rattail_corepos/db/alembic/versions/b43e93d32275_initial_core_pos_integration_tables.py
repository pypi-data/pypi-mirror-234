# -*- coding: utf-8 -*-
"""initial CORE-POS integration tables

Revision ID: b43e93d32275
Revises: dfc1ed686f3f
Create Date: 2020-03-04 14:21:23.625568

"""

# revision identifiers, used by Alembic.
revision = 'b43e93d32275'
down_revision = None
branch_labels = ('rattail_corepos',)
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_vendor
    op.create_table('corepos_vendor',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['vendor.uuid'], name='corepos_vendor_fk_vendor'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_vendor_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_vendor_version_end_transaction_id'), 'corepos_vendor_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_vendor_version_operation_type'), 'corepos_vendor_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_vendor_version_transaction_id'), 'corepos_vendor_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_vendor
    op.drop_index(op.f('ix_corepos_vendor_version_transaction_id'), table_name='corepos_vendor_version')
    op.drop_index(op.f('ix_corepos_vendor_version_operation_type'), table_name='corepos_vendor_version')
    op.drop_index(op.f('ix_corepos_vendor_version_end_transaction_id'), table_name='corepos_vendor_version')
    op.drop_table('corepos_vendor_version')
    op.drop_table('corepos_vendor')
