# routes/live_tracking.py
# -------------------------------------------------------------------
# GET /track/live?pin=1234
# - Uses pg pool (db/pg.py), no hard-coded secrets
# - Validates pin as string to preserve leading zeros
# - Returns timestamps as ISO strings
# -------------------------------------------------------------------
from __future__ import annotations
from fastapi import APIRouter, Query
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any
from db.pg import get_conn   # NEW helper

router = APIRouter(tags=["tracking"])  # keep path as /track/live via direct route path below

def _get_latest_location(pin: str, role: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                  ST_Y(location::geometry) AS lat,
                  ST_X(location::geometry) AS lng,
                  timestamp
                FROM locations
                WHERE pin = %s AND role = %s
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (pin, role),
            )
            row = cur.fetchone()
            if not row:
                return None
            # Normalize timestamp to ISO string; psycopg returns datetime
            ts = row.get("timestamp")
            if hasattr(ts, "isoformat"):
                row["timestamp"] = ts.isoformat()
            return dict(row)

@router.get("/track/live")
def get_live_locations(
    pin: str = Query(..., min_length=4, max_length=6, description="Ride PIN as digits (keeps leading zeros)")
):
    # Store PIN as string to preserve leading zeros
    driver = _get_latest_location(pin=pin, role="driver")
    rider = _get_latest_location(pin=pin, role="rider")

    resp: Dict[str, Any] = {}
    if driver:
        resp["driver"] = driver
    if rider:
        resp["rider"] = rider

    if not resp:
        return {"status": "empty", "detail": "No live location available for this pin."}
    return resp
