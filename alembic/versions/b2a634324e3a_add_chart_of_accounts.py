"""add chart of accounts

Revision ID: b2a634324e3a
Revises: PRODUCT_INVOICE_001
Create Date: 2026-05-20 11:25:43.251995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b2a634324e3a'
down_revision: Union[str, Sequence[str], None] = 'PRODUCT_INVOICE_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'chart_of_accounts',

        sa.Column('id', sa.Integer(), nullable=False),

        sa.Column(
            'organization_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'account_code',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'account_name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'account_type',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'parent_account_id',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.ForeignKeyConstraint(
            ['parent_account_id'],
            ['chart_of_accounts.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_chart_of_accounts_id'),
        'chart_of_accounts',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_chart_of_accounts_id'),
        table_name='chart_of_accounts'
    )

    op.drop_table('chart_of_accounts')
