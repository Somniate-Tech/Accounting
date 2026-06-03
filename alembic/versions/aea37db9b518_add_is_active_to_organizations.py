"""add is_active to organizations

Revision ID: aea37db9b518
Revises: 677ec0bea5d7
Create Date: 2026-06-02 13:23:19.523735
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aea37db9b518"
down_revision: Union[str, Sequence[str], None] = "677ec0bea5d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "organizations",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true")
        )
    )


def downgrade() -> None:

    op.drop_column(
        "organizations",
        "is_active"
    )