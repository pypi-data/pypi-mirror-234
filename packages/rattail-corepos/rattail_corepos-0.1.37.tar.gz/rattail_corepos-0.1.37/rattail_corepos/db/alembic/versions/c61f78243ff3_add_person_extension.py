# -*- coding: utf-8 -*-
"""add Person extension

Revision ID: c61f78243ff3
Revises: b43e93d32275
Create Date: 2020-03-16 16:50:55.266325

"""

# revision identifiers, used by Alembic.
revision = 'c61f78243ff3'
down_revision = 'b43e93d32275'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_person
    op.create_table('corepos_person',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_customer_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['person.uuid'], name='corepos_person_fk_person'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_person_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_customer_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_person_version_end_transaction_id'), 'corepos_person_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_person_version_operation_type'), 'corepos_person_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_person_version_transaction_id'), 'corepos_person_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_person
    op.drop_index(op.f('ix_corepos_person_version_transaction_id'), table_name='corepos_person_version')
    op.drop_index(op.f('ix_corepos_person_version_operation_type'), table_name='corepos_person_version')
    op.drop_index(op.f('ix_corepos_person_version_end_transaction_id'), table_name='corepos_person_version')
    op.drop_table('corepos_person_version')
    op.drop_table('corepos_person')
