"""merge heads

Revision ID: 179c876350b9
Revises: 59320f0e4f92, add_driver_pin_to_jobs
Create Date: 2025-10-15 05:50:38.244345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '179c876350b9'
down_revision: Union[str, Sequence[str], None] = ('59320f0e4f92', 'add_driver_pin_to_jobs')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
