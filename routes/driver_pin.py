# routes/driver_pin.py
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from db.pg import get_conn

router = APIRouter(tags=["driver-pin"])

# --- simple admin token guard (same pattern as routes/admin.py) ---
def require_admin(token: Optional[str] = Query(None, alias="token")):
    expected = os.getenv("ADMIN_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN not configured")
    if token != expected:
        raise HTTPException(status_code=401, detail="invalid admin token")
    return True

# --- models ---
class PinVerifyBody(BaseModel):
    job_id: int
    pin: str

# --- helpers ---
def _generate_pin(n: int = 6) -> str:
    # 6-digit numeric PIN, zero-padded
    # NOTE: we keep it numeric for easy phone/SMS entry
    import random
    return f"{random.randint(0, 10**n - 1):0{n}d}"

# --- endpoints ---

@router.post("/admin/jobs/{job_id}/driver-pin/issue", dependencies=[Depends(require_admin)])
def issue_driver_pin(job_id: int, ttl_minutes: int = Query(30, ge=1, le=240)):
    """
    Admin issues/rotates a driver PIN for a specific job.
    Stores (driver_pin, driver_pin_expires) on the job.
    """
    pin = _generate_pin(6)
    expires = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)

    with get_conn() as conn, conn.cursor() as cur:
        # ensure job exists
        cur.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="job not found")

        cur.execute(
            """
            UPDATE jobs
               SET driver_pin = %s,
                   driver_pin_expires = %s
             WHERE id = %s
            """,
            (pin, expires, job_id),
        )
        conn.commit()

    return {
        "ok": True,
        "job_id": job_id,
        "driver_pin": pin,
        "driver_pin_expires": expires.isoformat(),
        "note": "Share this PIN only with the assigned driver.",
    }


@router.get("/admin/jobs/{job_id}/driver-pin/status", dependencies=[Depends(require_admin)])
def driver_pin_status(job_id: int):
    """
    Admin view of the current driver PIN & expiry for a job.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT driver_pin, driver_pin_expires
              FROM jobs
             WHERE id = %s
            """,
            (job_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="job not found")

        pin, expires = row
        return {
            "job_id": job_id,
            "driver_pin": pin,
            "driver_pin_expires": expires.isoformat() if expires else None,
        }


@router.post("/jobs/driver-pin/verify")
def verify_driver_pin(body: PinVerifyBody):
    """
    Public verification: a driver can verify they have access to this job.
    Returns minimal job info on success so the app can proceed (e.g. to claim/view).
    """
    now = datetime.now(timezone.utc)

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, driver_pin, driver_pin_expires, pickup_location, dropoff_location,
                   driver_id, driver_name, claimed
              FROM jobs
             WHERE id = %s
            """,
            (body.job_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="job not found")

        (jid, pin, expires, pickup, dropoff, driver_id, driver_name, claimed) = row

        if not pin or not expires:
            raise HTTPException(status_code=403, detail="driver PIN not issued")

        if body.pin != pin:
            raise HTTPException(status_code=403, detail="invalid driver PIN")

        if expires <= now:
            raise HTTPException(status_code=403, detail="driver PIN expired")

        return {
            "ok": True,
            "job_id": jid,
            "pickup_location": pickup,
            "dropoff_location": dropoff,
            "claimed": claimed,
            "driver_id": driver_id,
            "driver_name": driver_name,
        }
