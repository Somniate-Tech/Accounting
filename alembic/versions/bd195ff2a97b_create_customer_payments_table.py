"""create customer payments table

Revision ID: bd195ff2a97b
Revises: 9d71a12e80dc
Create Date: 2026-05-26 13:03:40.990530
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'bd195ff2a97b'
down_revision: Union[str, Sequence[str], None] = '9d71a12e80dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'customer_payments',

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
            'customer_id',
            sa.Integer(),
            sa.ForeignKey('customers.id'),
            nullable=False
        ),

        sa.Column(
            'invoice_id',
            sa.Integer(),
            sa.ForeignKey('sales_invoices.id'),
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

    op.drop_table('customer_payments')