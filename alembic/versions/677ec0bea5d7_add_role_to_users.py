"""add role to users

Revision ID: 677ec0bea5d7
Revises: 47cf72407f2f
Create Date: 2026-06-02 11:02:20.792827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '677ec0bea5d7'
down_revision: Union[str, Sequence[str], None] = '47cf72407f2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(),
            nullable=False,
            server_default='OWNER'
        )
    )


def downgrade() -> None:

    op.drop_column(
        'users',
        'role'
    )