"""add product id to sales invoice items

Revision ID: PRODUCT_INVOICE_001
Revises: 299495c15eb3
Create Date: 2026-05-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'PRODUCT_INVOICE_001'
down_revision: Union[str, Sequence[str], None] = '299495c15eb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'sales_invoice_items',

        sa.Column(
            'product_id',
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        'fk_sales_invoice_items_product_id',

        'sales_invoice_items',

        'products',

        ['product_id'],

        ['id']
    )


def downgrade() -> None:

    op.drop_constraint(
        'fk_sales_invoice_items_product_id',

        'sales_invoice_items',

        type_='foreignkey'
    )

    op.drop_column(
        'sales_invoice_items',

        'product_id'
    )