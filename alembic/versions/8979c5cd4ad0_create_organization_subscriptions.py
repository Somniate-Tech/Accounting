"""create_organization_subscriptions

Revision ID: 8979c5cd4ad0
Revises: 50051f990f4b
Create Date: 2026-05-29

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "8979c5cd4ad0"
down_revision: Union[str, Sequence[str], None] = "50051f990f4b"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "organization_subscriptions",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "organization_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "plan_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "end_date",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "is_trial",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false")
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"]
        ),

        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["subscription_plans.id"]
        )
    )

    op.create_index(
        "ix_organization_subscriptions_id",
        "organization_subscriptions",
        ["id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        "ix_organization_subscriptions_id",
        table_name="organization_subscriptions"
    )

    op.drop_table(
        "organization_subscriptions"
    )