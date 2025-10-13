# db/driver_registry.py
# Purpose: Postgres + PostGIS helpers for driver queries, using pooled connections.

from __future__ import annotations
from typing import Optional, Dict, Any, List
from psycopg2.extras import RealDictCursor
from db.pg import get_conn  # <-- use pooled connection helper

def list_available_drivers() -> List[Dict[str, Any]]:
    """Return all currently available drivers (basic listing)."""
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, name, email, vehicle, plate, is_available
            FROM drivers
            WHERE is_available = true
            ORDER BY id
        """)
        rows = cur.fetchall() or []
        return [dict(r) for r in rows]

def find_nearest_available_driver(pickup_lng: float, pickup_lat: float) -> Optional[Dict[str, Any]]:
    """
    Use PostGIS to compute the nearest available driver to the pickup location.
    - pickup_lng: longitude (X)
    - pickup_lat: latitude (Y)
    Returns a driver row (dict) or None.
    """
    sql = """
        SELECT
            id, name, email, vehicle, plate,
            ST_Distance(
                home_base,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
            ) AS meters
        FROM drivers
        WHERE is_available = true
          AND home_base IS NOT NULL
        ORDER BY home_base <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
        LIMIT 1
    """
    params = (pickup_lng, pickup_lat, pickup_lng, pickup_lat)
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None

def set_driver_availability(driver_id: int, available: bool) -> None:
    """Flip a driver's availability bit."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE drivers SET is_available = %s WHERE id = %s", (available, driver_id))
        conn.commit()

