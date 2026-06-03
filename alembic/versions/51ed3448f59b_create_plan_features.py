"""create_plan_features

Revision ID: 51ed3448f59b
Revises: f6ff036a4844
Create Date: 2026-05-29 17:41:59.052159
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "51ed3448f59b"
down_revision: Union[str, Sequence[str], None] = "f6ff036a4844"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "plan_features",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "plan_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "feature_id",
            sa.Integer(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["subscription_plans.id"]
        ),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["features.id"]
        ),
        sa.PrimaryKeyConstraint(
            "id"
        )
    )

    op.create_index(
        op.f("ix_plan_features_id"),
        "plan_features",
        ["id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f("ix_plan_features_id"),
        table_name="plan_features"
    )

    op.drop_table(
        "plan_features"
    )