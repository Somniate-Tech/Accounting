"""add warehouse id to stock transactions

Revision ID: e8626259bba0
Revises: 51ed3448f59b
Create Date: 2026-06-01 11:22:18.592491
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e8626259bba0"
down_revision: Union[str, Sequence[str], None] = "51ed3448f59b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stock_transactions",
        sa.Column(
            "warehouse_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_stock_transactions_warehouse_id_warehouses",
        "stock_transactions",
        "warehouses",
        ["warehouse_id"],
        ["id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_stock_transactions_warehouse_id_warehouses",
        "stock_transactions",
        type_="foreignkey"
    )

    op.drop_column(
        "stock_transactions",
        "warehouse_id"
    )