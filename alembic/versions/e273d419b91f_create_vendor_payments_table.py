"""create vendor payments table

Revision ID: e273d419b91f
Revises: d20682f668c3
Create Date: 2026-05-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


# revision identifiers
revision: str = 'e273d419b91f'
down_revision: Union[str, Sequence[str], None] = 'd20682f668c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'vendor_payments',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            index=True
        ),

        sa.Column(
            'organization_id',
            sa.Integer(),
            sa.ForeignKey('organizations.id'),
            nullable=False
        ),

        sa.Column(
            'vendor_id',
            UUID(as_uuid=True),
            sa.ForeignKey('vendors.id'),
            nullable=False
        ),

        sa.Column(
            'bill_id',
            UUID(as_uuid=True),
            sa.ForeignKey('bills.id'),
            nullable=False
        ),

        sa.Column(
            'amount',
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            'payment_method',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'reference_number',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'notes',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'payment_date',
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            'created_by',
            sa.Integer(),
            sa.ForeignKey('users.id')
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        )
    )


def downgrade() -> None:

    op.drop_table('vendor_payments')