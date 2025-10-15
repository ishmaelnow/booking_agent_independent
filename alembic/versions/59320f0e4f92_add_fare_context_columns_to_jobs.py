"""add fare context columns to jobs

Revision ID: 59320f0e4f92
Revises: 49ae5cbe5295
Create Date: 2025-10-15 04:48:20.026918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59320f0e4f92'
down_revision: Union[str, Sequence[str], None] = '49ae5cbe5295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("jobs") as b:
        b.add_column(sa.Column("fare_explanation", sa.Text(), nullable=True))
        b.add_column(sa.Column("fare_notes", sa.Text(), nullable=True))
        b.add_column(sa.Column("estimated_miles", sa.Float(), nullable=True))

def downgrade():
    with op.batch_alter_table("jobs") as b:
        b.drop_column("estimated_miles")
        b.drop_column("fare_notes")
        b.drop_column("fare_explanation")

