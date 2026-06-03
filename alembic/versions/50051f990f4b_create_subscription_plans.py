"""create_subscription_plans

Revision ID: 50051f990f4b
Revises: e273d419b91f
Create Date: 2026-05-29

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "50051f990f4b"
down_revision: Union[str, Sequence[str], None] = "e273d419b91f"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "subscription_plans",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
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
            nullable=False,
            unique=True
        ),

        sa.Column(
            "description",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "monthly_price",
            sa.Numeric(12, 2),
            server_default="0"
        ),

        sa.Column(
            "yearly_price",
            sa.Numeric(12, 2),
            server_default="0"
        ),

        sa.Column(
            "max_users",
            sa.Integer(),
            server_default="1"
        ),

        sa.Column(
            "max_customers",
            sa.Integer(),
            server_default="0"
        ),

        sa.Column(
            "max_vendors",
            sa.Integer(),
            server_default="0"
        ),

        sa.Column(
            "max_products",
            sa.Integer(),
            server_default="0"
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true")
        )
    )

    op.create_index(
        "ix_subscription_plans_id",
        "subscription_plans",
        ["id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        "ix_subscription_plans_id",
        table_name="subscription_plans"
    )

    op.drop_table(
        "subscription_plans"
    )