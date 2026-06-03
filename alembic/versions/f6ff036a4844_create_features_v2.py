"""create_features_v2

Revision ID: f6ff036a4844
Revises: 6e61edb1fbd8
Create Date: 2026-05-29 16:50:37.329345

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6ff036a4844"
down_revision: Union[str, Sequence[str], None] = "6e61edb1fbd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    op.create_table(
        "features",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "code",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "description",
            sa.String(),
            nullable=True
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True
        ),
        sa.PrimaryKeyConstraint(
            "id"
        ),
        sa.UniqueConstraint(
            "code"
        )
    )

    op.create_index(
        op.f("ix_features_id"),
        "features",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    op.drop_index(
        op.f("ix_features_id"),
        table_name="features"
    )

    op.drop_table(
        "features"
    )