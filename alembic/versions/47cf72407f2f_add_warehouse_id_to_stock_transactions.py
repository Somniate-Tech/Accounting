"""add warehouse id to stock transactions

Revision ID: 47cf72407f2f
Revises: e8626259bba0
Create Date: 2026-06-01 11:23:38.460232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '47cf72407f2f'
down_revision: Union[str, Sequence[str], None] = 'e8626259bba0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass