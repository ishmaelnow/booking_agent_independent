# routes/job_view_api.py
# -------------------------------------------------------------------
# GET /jobs/view
# - Keeps SQLite for now (as in your code)
# - Uses row_factory for readability and consistent shape
# -------------------------------------------------------------------
from __future__ import annotations
from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/view")
def view_jobs():
    conn = sqlite3.connect("booking_agent.db")
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, pickup_location, dropoff_location, fare_estimate, claimed, posted_at
            FROM jobs
            ORDER BY posted_at DESC
            """
        )
        rows = cur.fetchall()
        # Normalize records
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "pickup": r["pickup_location"],
                "dropoff": r["dropoff_location"],
                "fare": r["fare_estimate"],
                "status": "claimed" if r["claimed"] else "available",
                "posted_at": r["posted_at"],  # if string; format if datetime
            })
        return {"jobs": result}
    finally:
        conn.close()
