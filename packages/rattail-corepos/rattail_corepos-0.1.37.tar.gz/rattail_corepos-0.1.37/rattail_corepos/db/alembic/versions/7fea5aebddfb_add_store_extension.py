# -*- coding: utf-8; -*-
"""add store extension

Revision ID: 7fea5aebddfb
Revises: 130e4632a28a
Create Date: 2021-01-27 21:01:59.767884

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '7fea5aebddfb'
down_revision = '130e4632a28a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_store
    op.create_table('corepos_store',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['store.uuid'], name='corepos_store_fk_store'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_store_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_store_version_end_transaction_id'), 'corepos_store_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_store_version_operation_type'), 'corepos_store_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_store_version_transaction_id'), 'corepos_store_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_store
    op.drop_index(op.f('ix_corepos_store_version_transaction_id'), table_name='corepos_store_version')
    op.drop_index(op.f('ix_corepos_store_version_operation_type'), table_name='corepos_store_version')
    op.drop_index(op.f('ix_corepos_store_version_end_transaction_id'), table_name='corepos_store_version')
    op.drop_table('corepos_store_version')
    op.drop_table('corepos_store')
