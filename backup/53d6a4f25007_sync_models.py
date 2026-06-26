"""sync_models

Revision ID: 53d6a4f25007
Revises:
Create Date: 2026-06-10 16:56:26.712768

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "53d6a4f25007"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # products.warehouse_id

    op.add_column(
        "products",
        sa.Column(
            "warehouse_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_products_warehouse_id",
        "products",
        "warehouses",
        ["warehouse_id"],
        ["id"]
    )

    # sales_order_items index

    op.create_index(
        "ix_sales_order_items_id",
        "sales_order_items",
        ["id"],
        unique=False
    )


    # sales_orders dates

    op.alter_column(
        "sales_orders",
        "expected_delivery_date",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )

    op.alter_column(
        "sales_orders",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        existing_server_default=sa.text("now()")
    )

    op.alter_column(
        "sales_orders",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True
    )

    op.create_index(
        "ix_sales_orders_id",
        "sales_orders",
        ["id"],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        "ix_sales_orders_id",
        table_name="sales_orders"
    )

    op.alter_column(
        "sales_orders",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )

    op.alter_column(
        "sales_orders",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        existing_server_default=sa.text("now()")
    )

    op.alter_column(
        "sales_orders",
        "expected_delivery_date",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )

    op.drop_index(
        "ix_sales_order_items_id",
        table_name="sales_order_items"
    )

    op.drop_constraint(
        "fk_products_warehouse_id",
        "products",
        type_="foreignkey"
    )

    op.drop_column(
        "products",
        "warehouse_id"
    )