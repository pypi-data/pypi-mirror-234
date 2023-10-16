# -*- coding: utf-8; -*-
"""add core_employee

Revision ID: 1f2e2f57c90b
Revises: c40a6ec00428
Create Date: 2023-10-01 19:03:56.921897

"""

# revision identifiers, used by Alembic.
revision = '1f2e2f57c90b'
down_revision = 'c40a6ec00428'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_employee
    op.create_table('corepos_employee',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_number', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['uuid'], ['employee.uuid'], name='corepos_employee_fk_employee'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('corepos_employee_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_corepos_employee_version_end_transaction_id'), 'corepos_employee_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_employee_version_operation_type'), 'corepos_employee_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_employee_version_transaction_id'), 'corepos_employee_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_employee
    op.drop_index(op.f('ix_corepos_employee_version_transaction_id'), table_name='corepos_employee_version')
    op.drop_index(op.f('ix_corepos_employee_version_operation_type'), table_name='corepos_employee_version')
    op.drop_index(op.f('ix_corepos_employee_version_end_transaction_id'), table_name='corepos_employee_version')
    op.drop_table('corepos_employee_version')
    op.drop_table('corepos_employee')
