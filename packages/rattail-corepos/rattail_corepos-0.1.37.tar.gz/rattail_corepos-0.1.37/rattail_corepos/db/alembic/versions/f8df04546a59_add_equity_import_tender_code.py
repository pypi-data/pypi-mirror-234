# -*- coding: utf-8; -*-
"""add equity_import tender_code

Revision ID: f8df04546a59
Revises: d426a274f0c2
Create Date: 2023-09-16 15:38:25.569334

"""

# revision identifiers, used by Alembic.
revision = 'f8df04546a59'
down_revision = 'd426a274f0c2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import rattail.db.types



def upgrade():

    # batch_corepos_equity_import_row
    op.add_column('batch_corepos_equity_import_row', sa.Column('tender_code', sa.String(length=2), nullable=True))


def downgrade():

    # batch_corepos_equity_import_row
    op.drop_column('batch_corepos_equity_import_row', 'tender_code')
