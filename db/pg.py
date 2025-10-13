# db/pg.py
# -------------------------------------------------------------------
# Small psycopg2 connection pool, configured via env.
# Use DATABASE_URL or individual vars (PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT).
# -------------------------------------------------------------------
from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Iterator
from psycopg2.pool import SimpleConnectionPool
import psycopg2

# Prefer DATABASE_URL. Fallback to discrete vars.
DSN = os.getenv("DATABASE_URL") or (
    f"dbname={os.getenv('PGDATABASE','booking_agent')} "
    f"user={os.getenv('PGUSER','postgres')} "
    f"password={os.getenv('PGPASSWORD','')} "
    f"host={os.getenv('PGHOST','localhost')} "
    f"port={os.getenv('PGPORT','5432')}"
)

# Create a tiny pool (1..5). If DB is local dev, this is enough.
_POOL: SimpleConnectionPool | None = None

def _pool() -> SimpleConnectionPool:
    global _POOL
    if _POOL is None:
        # Note: raise on fail so you see it at boot.
        _POOL = SimpleConnectionPool(minconn=1, maxconn=5, dsn=DSN)
    return _POOL

@contextmanager
def get_conn() -> Iterator[psycopg2.extensions.connection]:
    """
    Usage:
      with get_conn() as conn:
          with conn.cursor() as cur:
              ...
    """
    pool = _pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)
