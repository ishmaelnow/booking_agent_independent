"""add fare context columns to jobs

Revision ID: 49ae5cbe5295
Revises: 718531d68752
Create Date: 2025-10-12 05:43:24.045119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49ae5cbe5295'
down_revision: Union[str, Sequence[str], None] = '718531d68752'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
