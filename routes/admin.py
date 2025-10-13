# routes/admin.py
from __future__ import annotations

import csv
import io
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from db.driver_registry import set_driver_availability
from db.pg import get_conn

router = APIRouter(prefix="/admin", tags=["admin"])


# -----------------------------
# Auth: simple token via ?token=
# -----------------------------
def require_admin(token: Optional[str] = Query(None, alias="token")):
    expected = os.getenv("ADMIN_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN not configured")
    if token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid admin token"
        )
    return True


# ---------- Schemas ----------
class SeedDriver(BaseModel):
    name: str = Field(..., examples=["Alice"])
    vehicle: str = Field(..., examples=["Toyota Camry"])
    plate: str = Field(..., examples=["NYC-111"])
    email: str = Field(..., examples=["alice@example.com"])
    is_available: bool = True
    # Optional start home_base position (lng/lat). If both provided, we set home_base.
    lng: float | None = None
    lat: float | None = None


# ---------- Helpers ----------
def _insert_driver(d: SeedDriver) -> int:
    """
    Upsert a driver by email.
    If lng/lat provided, update home_base too.
    Returns the id of the inserted/updated row.
    """
    with get_conn() as conn, conn.cursor() as cur:
        if d.lng is not None and d.lat is not None:
            cur.execute(
                """
                INSERT INTO drivers (name, vehicle, plate, email, is_available, home_base)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography)
                ON CONFLICT (email) DO UPDATE
                SET name = EXCLUDED.name,
                    vehicle = EXCLUDED.vehicle,
                    plate = EXCLUDED.plate,
                    is_available = EXCLUDED.is_available,
                    home_base = EXCLUDED.home_base
                RETURNING id
                """,
                (d.name, d.vehicle, d.plate, d.email, d.is_available, d.lng, d.lat),
            )
        else:
            cur.execute(
                """
                INSERT INTO drivers (name, vehicle, plate, email, is_available)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE
                SET name = EXCLUDED.name,
                    vehicle = EXCLUDED.vehicle,
                    plate = EXCLUDED.plate,
                    is_available = EXCLUDED.is_available
                RETURNING id
                """,
                (d.name, d.vehicle, d.plate, d.email, d.is_available),
            )
        new_id = cur.fetchone()[0]
        conn.commit()
        return int(new_id)


# ---------- Driver endpoints ----------
@router.get("/drivers", dependencies=[Depends(require_admin)])
def admin_list_drivers():
    """
    Return all drivers (available and unavailable).
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, vehicle, plate, email, is_available FROM drivers ORDER BY id"
        )
        rows = cur.fetchall() or []
    return {
        "count": len(rows),
        "items": [
            {
                "id": r[0],
                "name": r[1],
                "vehicle": r[2],
                "plate": r[3],
                "email": r[4],
                "is_available": r[5],
            }
            for r in rows
        ],
    }


@router.post("/drivers/seed", dependencies=[Depends(require_admin)])
def admin_seed_drivers(seed: list[SeedDriver]):
    """
    Seed one or more drivers. Upserts by email.
    """
    ids = [_insert_driver(d) for d in seed]
    return {"inserted": len(ids), "ids": ids}


@router.post("/drivers/reset", dependencies=[Depends(require_admin)])
def admin_reset_availability():
    """
    Set ALL drivers to available = true.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE drivers SET is_available = true")
        conn.commit()
    return {"ok": True}


@router.post("/drivers/{driver_id}/availability", dependencies=[Depends(require_admin)])
def admin_set_availability(driver_id: int, available: bool = Query(...)):
    """
    Toggle a single driver's availability.
    """
    set_driver_availability(driver_id, available)
    return {"ok": True, "driver_id": driver_id, "is_available": available}


# ---------- Job endpoints ----------
@router.get("/jobs", dependencies=[Depends(require_admin)])
def admin_list_jobs(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    """
    List jobs (most recent first).
    """
    sql = """
      SELECT
        id, pickup_location, dropoff_location,
        rider_name, phone_number,
        fare_estimate, claimed, driver_id, driver_name
      FROM jobs
      ORDER BY id DESC
      LIMIT %s OFFSET %s
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (limit, offset))
        rows = cur.fetchall() or []
        cols = [d[0] for d in cur.description]
    items = [dict(zip(cols, r)) for r in rows]
    return {"count": len(items), "items": items}


@router.get("/jobs/latest", dependencies=[Depends(require_admin)])
def admin_latest_job():
    """
    Return the most recent job (or null if none).
    """
    sql = """
      SELECT
        id, pickup_location, dropoff_location,
        rider_name, phone_number,
        fare_estimate, claimed, driver_id, driver_name
      FROM jobs
      ORDER BY id DESC
      LIMIT 1
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            return {"item": None}
        cols = [d[0] for d in cur.description]
        return {"item": dict(zip(cols, row))}


@router.post("/jobs/clear", dependencies=[Depends(require_admin)])
def admin_clear_jobs():
    """
    Delete ALL jobs (careful!). Drivers table is NOT touched.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM jobs")
        conn.commit()
    return {"ok": True, "message": "all jobs deleted"}


@router.get("/jobs/export", dependencies=[Depends(require_admin)])
def admin_export_jobs_csv():
    """
    Stream all jobs as CSV (most recent first).
    """
    sql = """
      SELECT
        id, pickup_location, dropoff_location,
        rider_name, phone_number,
        fare_estimate, claimed, driver_id, driver_name
      FROM jobs
      ORDER BY id DESC
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall() or []
        cols = [d[0] for d in cur.description]

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(cols)
    for r in rows:
        writer.writerow(list(r))
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="jobs.csv"'},
    )


@router.post("/jobs/{job_id}/complete", dependencies=[Depends(require_admin)])
def admin_complete_job(job_id: int):
    """
    Mark a job as completed and free up its driver.
    We:
      1) read the job's driver_id
      2) set that driver's is_available = true
      3) set jobs.claimed = false (so it's no longer active)
    """
    with get_conn() as conn, conn.cursor() as cur:
        # 1) find driver for this job
        cur.execute("SELECT driver_id FROM jobs WHERE id = %s", (job_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="job not found")
        driver_id = row[0]

        # If no driver was assigned (edge case), just flip claimed to false
        if driver_id is not None:
            # 2) free the driver
            cur.execute("UPDATE drivers SET is_available = true WHERE id = %s", (driver_id,))

        # 3) mark job not-claimed anymore (completed/closed)
        cur.execute("UPDATE jobs SET claimed = false WHERE id = %s", (job_id,))
        conn.commit()

    return {"ok": True, "job_id": job_id, "driver_id": driver_id, "driver_available": True}
