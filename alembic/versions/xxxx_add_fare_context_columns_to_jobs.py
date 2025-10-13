from alembic import op

# revision identifiers
revision = "add_fare_ctx"
down_revision = None  # or your previous revision id

def upgrade():
    op.execute("""
        ALTER TABLE jobs
        ADD COLUMN IF NOT EXISTS estimated_miles REAL,
        ADD COLUMN IF NOT EXISTS fare_notes TEXT,
        ADD COLUMN IF NOT EXISTS fare_explanation TEXT
    """)
)

def downgrade():
    op.execute("""
        ALTER TABLE jobs
        DROP COLUMN IF EXISTS fare_explanation,
        DROP COLUMN IF EXISTS fare_notes,
        DROP COLUMN IF EXISTS estimated_miles
    """)
