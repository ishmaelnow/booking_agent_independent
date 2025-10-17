# routes/driver_api.py
from __future__ import annotations

from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException

from db.driver_registry import list_available_drivers
from db.pg import get_conn

# Prefer the router-local auth module import
try:
    from routes.auth import require_driver  # dependency implemented in routes/auth.py
except Exception:
    from auth import require_driver  # fallback if auth.py is at project root

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/available")
def get_available_drivers():
    """
    Public: list currently available drivers.
    """
    return {"available_drivers": list_available_drivers()}


@router.get("/me")
def driver_me(user: Dict[str, Any] = Depends(require_driver)):
    """
    Protected: return info from the driver token.
    """
    return {
        "sub": user.get("sub"),
        "email": user.get("email"),
        "role": user.get("role"),
    }


@router.get("/jobs")
def driver_my_jobs(user: Dict[str, Any] = Depends(require_driver)):
    """
    Protected: list jobs assigned to the authenticated driver.
    Matches by driver_id (preferred) or by driver_name (legacy fallback).
    """
    driver_id = str(user.get("sub") or "")
    driver_email = (user.get("email") or "").strip()

    if not driver_id:
        raise HTTPException(status_code=401, detail="invalid token: missing sub")

    sql = """
        SELECT id, pickup_location, dropoff_location,
               fare_estimate, claimed, driver_id, driver_name
        FROM jobs
        WHERE driver_id::text = %s OR driver_name = %s
        ORDER BY id DESC
        LIMIT 50
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (driver_id, driver_email))
        rows = cur.fetchall() or []
        cols = [d[0] for d in cur.description]

    items = [dict(zip(cols, r)) for r in rows]
    return {"count": len(items), "items": items}
