from __future__ import annotations
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# --- Alembic identifiers ---
revision: str = "ce20dc36c4e3"           # <- keep this id
down_revision: Union[str, Sequence[str], None] = "179c876350b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "jobs",
        sa.Column("driver_pin", sa.String(length=12), nullable=True),
    )
    op.add_column(
        "jobs",
        sa.Column("driver_pin_expires", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_jobs_driver_pin",
        "jobs",
        ["driver_pin"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_jobs_driver_pin", table_name="jobs")
    op.drop_column("jobs", "driver_pin_expires")
    op.drop_column("jobs", "driver_pin")
