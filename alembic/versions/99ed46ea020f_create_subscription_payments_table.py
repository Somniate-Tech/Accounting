"""create subscription payments table"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "99ed46ea020f"
down_revision: Union[str, Sequence[str], None] = "fce53948a3e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "subscription_payments",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "organization_id",
            sa.Integer(),
            sa.ForeignKey("organizations.id"),
            nullable=False
        ),

        sa.Column(
            "plan_id",
            sa.Integer(),
            sa.ForeignKey("subscription_plans.id"),
            nullable=False
        ),

        sa.Column(
            "amount",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "billing_cycle",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "gateway",
            sa.String(),
            nullable=False,
            server_default="RAZORPAY"
        ),

        sa.Column(
            "order_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "payment_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "signature",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="PENDING"
        ),

        sa.Column(
            "paid_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        )
    )

    op.create_index(
        "ix_subscription_payments_id",
        "subscription_payments",
        ["id"]
    )


def downgrade() -> None:

    op.drop_index(
        "ix_subscription_payments_id",
        table_name="subscription_payments"
    )

    op.drop_table(
        "subscription_payments"
    )