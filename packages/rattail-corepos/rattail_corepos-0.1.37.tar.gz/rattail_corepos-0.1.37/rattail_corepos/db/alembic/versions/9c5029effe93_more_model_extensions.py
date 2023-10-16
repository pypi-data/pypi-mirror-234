# -*- coding: utf-8; -*-
"""more model extensions

Revision ID: 9c5029effe93
Revises: c61f78243ff3
Create Date: 2020-07-06 19:27:06.156401

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '9c5029effe93'
down_revision = 'c61f78243ff3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # corepos_customer
    op.create_table('corepos_customer',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_account_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['customer.uuid'], name='corepos_customer_fk_customer'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_customer_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_account_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_customer_version_end_transaction_id'), 'corepos_customer_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_customer_version_operation_type'), 'corepos_customer_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_customer_version_transaction_id'), 'corepos_customer_version', ['transaction_id'], unique=False)

    # corepos_member
    op.create_table('corepos_member',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_account_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['member.uuid'], name='corepos_member_fk_member'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_member_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_account_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_member_version_end_transaction_id'), 'corepos_member_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_member_version_operation_type'), 'corepos_member_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_member_version_transaction_id'), 'corepos_member_version', ['transaction_id'], unique=False)

    # corepos_department
    op.create_table('corepos_department',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_number', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['department.uuid'], name='corepos_department_fk_department'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_department_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_department_version_end_transaction_id'), 'corepos_department_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_department_version_operation_type'), 'corepos_department_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_department_version_transaction_id'), 'corepos_department_version', ['transaction_id'], unique=False)

    # corepos_subdepartment
    op.create_table('corepos_subdepartment',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_number', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['subdepartment.uuid'], name='corepos_subdepartment_fk_subdepartment'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_subdepartment_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_number', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_subdepartment_version_end_transaction_id'), 'corepos_subdepartment_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_subdepartment_version_operation_type'), 'corepos_subdepartment_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_subdepartment_version_transaction_id'), 'corepos_subdepartment_version', ['transaction_id'], unique=False)

    # corepos_product
    op.create_table('corepos_product',
                    sa.Column('uuid', sa.String(length=32), nullable=False),
                    sa.Column('corepos_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['uuid'], ['product.uuid'], name='corepos_product_fk_product'),
                    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('corepos_product_version',
                    sa.Column('uuid', sa.String(length=32), autoincrement=False, nullable=False),
                    sa.Column('corepos_id', sa.Integer(), autoincrement=False, nullable=True),
                    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
                    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
                    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid', 'transaction_id')
    )
    op.create_index(op.f('ix_corepos_product_version_end_transaction_id'), 'corepos_product_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_corepos_product_version_operation_type'), 'corepos_product_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_corepos_product_version_transaction_id'), 'corepos_product_version', ['transaction_id'], unique=False)


def downgrade():

    # corepos_product
    op.drop_index(op.f('ix_corepos_product_version_transaction_id'), table_name='corepos_product_version')
    op.drop_index(op.f('ix_corepos_product_version_operation_type'), table_name='corepos_product_version')
    op.drop_index(op.f('ix_corepos_product_version_end_transaction_id'), table_name='corepos_product_version')
    op.drop_table('corepos_product_version')
    op.drop_table('corepos_product')

    # corepos_subdepartment
    op.drop_index(op.f('ix_corepos_subdepartment_version_transaction_id'), table_name='corepos_subdepartment_version')
    op.drop_index(op.f('ix_corepos_subdepartment_version_operation_type'), table_name='corepos_subdepartment_version')
    op.drop_index(op.f('ix_corepos_subdepartment_version_end_transaction_id'), table_name='corepos_subdepartment_version')
    op.drop_table('corepos_subdepartment_version')
    op.drop_table('corepos_subdepartment')

    # corepos_department
    op.drop_index(op.f('ix_corepos_department_version_transaction_id'), table_name='corepos_department_version')
    op.drop_index(op.f('ix_corepos_department_version_operation_type'), table_name='corepos_department_version')
    op.drop_index(op.f('ix_corepos_department_version_end_transaction_id'), table_name='corepos_department_version')
    op.drop_table('corepos_department_version')
    op.drop_table('corepos_department')

    # corepos_member
    op.drop_index(op.f('ix_corepos_member_version_transaction_id'), table_name='corepos_member_version')
    op.drop_index(op.f('ix_corepos_member_version_operation_type'), table_name='corepos_member_version')
    op.drop_index(op.f('ix_corepos_member_version_end_transaction_id'), table_name='corepos_member_version')
    op.drop_table('corepos_member_version')
    op.drop_table('corepos_member')

    # corepos_customer
    op.drop_index(op.f('ix_corepos_customer_version_transaction_id'), table_name='corepos_customer_version')
    op.drop_index(op.f('ix_corepos_customer_version_operation_type'), table_name='corepos_customer_version')
    op.drop_index(op.f('ix_corepos_customer_version_end_transaction_id'), table_name='corepos_customer_version')
    op.drop_table('corepos_customer_version')
    op.drop_table('corepos_customer')
