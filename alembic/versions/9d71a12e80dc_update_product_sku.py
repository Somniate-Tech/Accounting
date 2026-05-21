"""update product sku

Revision ID: 9d71a12e80dc
Revises: 46926cfe6cd7
Create Date: 2026-05-21 11:11:41.675618

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d71a12e80dc'

down_revision: Union[str, Sequence[str], None] = '46926cfe6cd7'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'products',
        'sku',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.create_unique_constraint(
        'uq_products_sku',
        'products',
        ['sku']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'uq_products_sku',
        'products',
        type_='unique'
    )

    op.alter_column(
        'products',
        'sku',
        existing_type=sa.VARCHAR(),
        nullable=False
    )