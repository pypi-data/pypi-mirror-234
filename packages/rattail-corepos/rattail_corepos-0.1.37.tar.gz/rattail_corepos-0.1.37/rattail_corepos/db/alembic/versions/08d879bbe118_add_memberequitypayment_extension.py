# -*- coding: utf-8; -*-
"""add MemberEquityPayment extension

Revision ID: 08d879bbe118
Revises: b025df7cf41b
Create Date: 2023-09-06 17:44:43.874500

"""

# revision identifiers, used by Alembic.
revision = '08d879bbe118'
down_revision = 'b025df7cf41b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_member_equity_payment
    op.create_table('corepos_member_equity_payment',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_card_number', sa.Integer(), nullable=False),
                    sa.Column('corepos_transaction_number', sa.String(length=50), nullable=True),
                    sa.Column('corepos_transaction_id', sa.Integer(), nullable=True),
                    sa.Column('corepos_department_number', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['uuid'], ['member_equity_payment.uuid'], name='corepos_member_equity_payment_fk_payment'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('corepos_member_equity_payment_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_card_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('corepos_transaction_number', sa.String(length=50), autoincrement=False, nullable=True),
                    sa.Column('corepos_transaction_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('corepos_department_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
                    )
    op.create_index(op.f('ix_corepos_member_equity_payment_version_end_transaction_id'), 'corepos_member_equity_payment_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_member_equity_payment_version_operation_type'), 'corepos_member_equity_payment_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_member_equity_payment_version_transaction_id'), 'corepos_member_equity_payment_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_member_equity_payment
    op.drop_index(op.f('ix_corepos_member_equity_payment_version_transaction_id'), table_name='corepos_member_equity_payment_version')
    op.drop_index(op.f('ix_corepos_member_equity_payment_version_operation_type'), table_name='corepos_member_equity_payment_version')
    op.drop_index(op.f('ix_corepos_member_equity_payment_version_end_transaction_id'), table_name='corepos_member_equity_payment_version')
    op.drop_table('corepos_member_equity_payment_version')
    op.drop_table('corepos_member_equity_payment')
