# -*- coding: utf-8; -*-
"""add corepos_tax

Revision ID: 673ff7088d35
Revises: 1f2e2f57c90b
Create Date: 2023-10-06 21:01:01.105790

"""

# revision identifiers, used by Alembic.
revision = '673ff7088d35'
down_revision = '1f2e2f57c90b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_tax
    op.create_table('corepos_tax',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['tax.uuid'], name='corepos_tax_fk_tax'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('corepos_tax_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_corepos_tax_version_end_transaction_id'), 'corepos_tax_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_tax_version_operation_type'), 'corepos_tax_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_tax_version_transaction_id'), 'corepos_tax_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_tax
    op.drop_index(op.f('ix_corepos_tax_version_transaction_id'), table_name='corepos_tax_version')
    op.drop_index(op.f('ix_corepos_tax_version_operation_type'), table_name='corepos_tax_version')
    op.drop_index(op.f('ix_corepos_tax_version_end_transaction_id'), table_name='corepos_tax_version')
    op.drop_table('corepos_tax_version')
    op.drop_table('corepos_tax')
