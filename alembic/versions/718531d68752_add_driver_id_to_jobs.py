"""add driver_id to jobs"""

from alembic import op

# Use the id Alembic generated for THIS file:
revision = "718531d68752"
# Point to your previous migration's revision id (the drivers one):
down_revision = "fe62ee1c3c87"
branch_labels = None
depends_on = None

def upgrade():
    # 1) add a nullable driver_id column
    op.execute("""
    ALTER TABLE jobs
    ADD COLUMN IF NOT EXISTS driver_id bigint NULL;
    """)

    # 2) optional: create an index to speed up lookups by driver
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_jobs_driver_id
      ON jobs(driver_id);
    """)

    # 3) optional (no hard FK yet): if you want a real FK and your data is clean,
    # uncomment this later
    # op.execute("""
    # ALTER TABLE jobs
    #   ADD CONSTRAINT fk_jobs_driver
    #   FOREIGN KEY (driver_id) REFERENCES drivers(id)
    #   DEFERRABLE INITIALLY DEFERRED;
    # """)

def downgrade():
    # Drop in reverse order
    op.execute("DROP INDEX IF EXISTS idx_jobs_driver_id;")
    op.execute("""
    ALTER TABLE jobs
    DROP COLUMN IF EXISTS driver_id;
    """)

