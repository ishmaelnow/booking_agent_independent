"""add drivers table"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "fe62ee1c3c87"
# If you already have an earlier migration (e.g., 0001_init), put its revision id here.
# If this is your FIRST migration ever, set down_revision = None.
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create a simple drivers table + a geospatial column for later use
    op.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        id            bigserial PRIMARY KEY,
        name          text NOT NULL,
        email         text UNIQUE,
        vehicle       text,
        plate         text,
        is_available  boolean NOT NULL DEFAULT true,
        home_base     geography(Point,4326)
    );
    """)
    # GIST index so nearest-driver queries are fast
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_drivers_home_base
      ON drivers USING GIST(home_base);
    """)

def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_drivers_home_base;")
    op.execute("DROP TABLE IF EXISTS drivers;")

