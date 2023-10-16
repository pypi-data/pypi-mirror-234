# -*- coding: utf-8; -*-
"""add tender

Revision ID: c40a6ec00428
Revises: f8df04546a59
Create Date: 2023-09-26 18:22:17.804658

"""

# revision identifiers, used by Alembic.
revision = 'c40a6ec00428'
down_revision = 'f8df04546a59'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_tender
    op.create_table('corepos_tender',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['tender.uuid'], name='corepos_tender_fk_tender'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('corepos_tender_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_corepos_tender_version_end_transaction_id'), 'corepos_tender_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_tender_version_operation_type'), 'corepos_tender_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_tender_version_transaction_id'), 'corepos_tender_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_tender
    op.drop_table('corepos_tender')
    op.drop_index(op.f('ix_corepos_tender_version_transaction_id'), table_name='corepos_tender_version')
    op.drop_index(op.f('ix_corepos_tender_version_operation_type'), table_name='corepos_tender_version')
    op.drop_index(op.f('ix_corepos_tender_version_end_transaction_id'), table_name='corepos_tender_version')
    op.drop_table('corepos_tender_version')
