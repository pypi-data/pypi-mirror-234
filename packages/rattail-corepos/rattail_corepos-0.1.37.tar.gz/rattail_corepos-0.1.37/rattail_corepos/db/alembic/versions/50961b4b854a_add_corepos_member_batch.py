# -*- coding: utf-8; -*-
"""add corepos_member batch

Revision ID: 50961b4b854a
Revises: 7fea5aebddfb
Create Date: 2021-11-04 18:36:23.494783

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '50961b4b854a'
down_revision = '7fea5aebddfb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_corepos_member
    op.create_table('batch_corepos_member',
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
                    sa.Column('input_file', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['cognized_by_uuid'], ['user.uuid'], name='batch_corepos_member_fk_cognized_by'),
                    sa.ForeignKeyConstraint(['created_by_uuid'], ['user.uuid'], name='batch_corepos_member_fk_created_by'),
                    sa.ForeignKeyConstraint(['executed_by_uuid'], ['user.uuid'], name='batch_corepos_member_fk_executed_by'),
                    sa.PrimaryKeyConstraint('uuid')
    )

    # batch_corepos_member_row
    op.create_table('batch_corepos_member_row',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('batch_uuid', sa.String(length=32), nullable=False),
                    sa.Column('sequence', sa.Integer(), nullable=False),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('status_text', sa.String(length=255), nullable=True),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('removed', sa.Boolean(), nullable=False),
                    sa.Column('card_number', sa.Integer(), nullable=True),
                    sa.Column('first_name', sa.String(length=30), nullable=True),
                    sa.Column('first_name_old', sa.String(length=30), nullable=True),
                    sa.Column('last_name', sa.String(length=30), nullable=True),
                    sa.Column('last_name_old', sa.String(length=30), nullable=True),
                    sa.Column('street', sa.String(length=255), nullable=True),
                    sa.Column('street_old', sa.String(length=255), nullable=True),
                    sa.Column('city', sa.String(length=20), nullable=True),
                    sa.Column('city_old', sa.String(length=20), nullable=True),
                    sa.Column('state', sa.String(length=2), nullable=True),
                    sa.Column('state_old', sa.String(length=2), nullable=True),
                    sa.Column('zipcode', sa.String(length=10), nullable=True),
                    sa.Column('zipcode_old', sa.String(length=10), nullable=True),
                    sa.Column('phone', sa.String(length=30), nullable=True),
                    sa.Column('phone_old', sa.String(length=30), nullable=True),
                    sa.Column('email1', sa.String(length=50), nullable=True),
                    sa.Column('email1_old', sa.String(length=50), nullable=True),
                    sa.Column('email2', sa.String(length=50), nullable=True),
                    sa.Column('email2_old', sa.String(length=50), nullable=True),
                    sa.Column('member_type_id', sa.SmallInteger(), nullable=True),
                    sa.Column('member_type_id_old', sa.SmallInteger(), nullable=True),
                    sa.ForeignKeyConstraint(['batch_uuid'], ['batch_corepos_member.uuid'], name='batch_corepos_member_row_fk_batch_uuid'),
                    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade():

    # batch_corepos_member*
    op.drop_table('batch_corepos_member_row')
    op.drop_table('batch_corepos_member')
