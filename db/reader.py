# db/reader.py
from __future__ import annotations
from typing import Optional, Dict, Any, List
from psycopg2.extras import RealDictCursor
from db.pg import get_conn

def list_bookings(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, pickup_location, dropoff_location, fare_estimate,
                       rider_name, phone_number, posted_at, claimed, driver_name, completed_at
                FROM jobs
                ORDER BY posted_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cur.fetchall() or []
            return [dict(r) for r in rows]

def get_job(job_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, pickup_location, dropoff_location, fare_estimate,
                       rider_name, phone_number, posted_at, claimed, driver_name, completed_at
                FROM jobs
                WHERE id = %s
                """,
                (job_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
