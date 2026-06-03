"""add paid and due amount to bills

Revision ID: d20682f668c3
Revises: bd195ff2a97b
Create Date: 2026-05-26 15:01:28.110335
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'd20682f668c3'
down_revision: Union[str, Sequence[str], None] = 'bd195ff2a97b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'bills',

        sa.Column(
            'paid_amount',
            sa.Numeric(18, 2),
            nullable=True,
            server_default='0'
        )
    )

    op.add_column(
        'bills',

        sa.Column(
            'due_amount',
            sa.Numeric(18, 2),
            nullable=True,
            server_default='0'
        )
    )


def downgrade() -> None:

    op.drop_column(
        'bills',
        'due_amount'
    )

    op.drop_column(
        'bills',
        'paid_amount'
    )