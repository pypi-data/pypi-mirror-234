# -*- coding: utf-8; -*-
"""add equity import batch

Revision ID: 93978a7adc66
Revises: 08d879bbe118
Create Date: 2023-09-12 23:09:09.148879

"""

# revision identifiers, used by Alembic.
revision = '93978a7adc66'
down_revision = '08d879bbe118'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_corepos_equity_import
    op.create_table('batch_corepos_equity_import',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('created_by_uuid', sa.String(length=32), nullable=False),
                    sa.Column('cognized', sa.DateTime(), nullable=True),
                    sa.Column('cognized_by_uuid', sa.String(length=32), nullable=True),
                    sa.Column('rowcount', sa.Integer(), nullable=True),
                    sa.Column('complete', sa.Boolean(), nullable=False),
                    sa.Column('executed', sa.DateTime(), nullable=True),
                    sa.Column('executed_by_uuid', sa.String(length=32), nullable=True),
                    sa.Column('purge', sa.Date(), nullable=True),
                    sa.Column('notes', sa.Text(), nullable=True),
                    sa.Column('params', rattail.db.types.JSONTextDict(), nullable=True),
                    sa.Column('extra_data', sa.Text(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['cognized_by_uuid'], ['user.uuid'], name='batch_corepos_equity_import_fk_cognized_by'),
                    sa.ForeignKeyConstraint(['created_by_uuid'], ['user.uuid'], name='batch_corepos_equity_import_fk_created_by'),
                    sa.ForeignKeyConstraint(['executed_by_uuid'], ['user.uuid'], name='batch_corepos_equity_import_fk_executed_by'),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('batch_corepos_equity_import_row',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('batch_uuid', sa.String(length=32), nullable=False),
                    sa.Column('sequence', sa.Integer(), nullable=False),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('removed', sa.Boolean(), nullable=False),
                    sa.Column('card_number', sa.Integer(), nullable=True),
                    sa.Column('first_name', sa.String(length=30), nullable=True),
                    sa.Column('last_name', sa.String(length=30), nullable=True),
                    sa.Column('member_type_id', sa.Integer(), nullable=True),
                    sa.Column('payment_amount', sa.Numeric(precision=10, scale=2), nullable=True),
                    sa.Column('department_number', sa.Integer(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('corepos_equity_total', sa.Numeric(precision=10, scale=2), nullable=True),
                    sa.Column('rattail_equity_total', sa.Numeric(precision=10, scale=2), nullable=True),
                    sa.Column('other_equity_total', sa.Numeric(precision=10, scale=2), nullable=True),
                    sa.Column('payment_uuid', sa.String(length=32), nullable=True),
                    sa.Column('member_uuid', sa.String(length=32), nullable=True),
                    sa.ForeignKeyConstraint(['batch_uuid'], ['batch_corepos_equity_import.uuid'], name='batch_corepos_equity_import_row_fk_batch_uuid'),
                    sa.ForeignKeyConstraint(['payment_uuid'], ['member_equity_payment.uuid'], name='batch_corepos_equity_import_row_fk_payment'),
                    sa.ForeignKeyConstraint(['member_uuid'], ['member.uuid'], name='batch_corepos_equity_import_row_fk_member'),
                    sa.PrimaryKeyConstraint('uuid')
                    )


def downgrade():

    # batch_corepos_equity_import
    op.drop_table('batch_corepos_equity_import_row')
    op.drop_table('batch_corepos_equity_import')
