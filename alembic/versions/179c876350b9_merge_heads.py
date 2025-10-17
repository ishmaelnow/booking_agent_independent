# alembic/versions/179c876350b9_merge_heads.py
from __future__ import annotations
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# This is a NO-OP merge revision that just linearizes history.
revision: str = "179c876350b9"
down_revision: Union[str, Sequence[str], None] = "59320f0e4f92"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # merge point only; no schema changes
    pass

def downgrade() -> None:
    # merge point only; no schema changes
    pass
