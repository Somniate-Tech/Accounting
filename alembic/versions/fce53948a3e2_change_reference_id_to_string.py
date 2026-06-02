"""change reference_id to string

Revision ID: fce53948a3e2
Revises: aea37db9b518
Create Date: 2026-06-02 17:46:39.255777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fce53948a3e2'
down_revision: Union[str, Sequence[str], None] = 'aea37db9b518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'journal_entries',
        'reference_id',
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True
    )

def downgrade() -> None:
    op.alter_column(
        'journal_entries',
        'reference_id',
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True
    )
