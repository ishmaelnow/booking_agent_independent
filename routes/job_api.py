# routes/job_api.py
from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

router = APIRouter(prefix="/jobs", tags=["Jobs"])

from db.job_board import claim_job, complete_job
from db.reader import get_job

# optional driver email notification on claim
try:
    from notifications.driver_notifier import notify_driver_claim
except Exception:
    def notify_driver_claim(*args, **kwargs):  # no-op in dev
        pass

@router.post("/claim")
def claim(
    job_id: int = Query(..., ge=1),
    driver_name: str = Query(..., min_length=1),
    driver_email: str | None = Query(None, description="optional; if set, email confirmation is sent")
):
    try:
        result = claim_job(job_id, driver_name)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to claim job")

    if result is None:
        raise HTTPException(status_code=404, detail="Job not found or already claimed")

    # fire-and-forget email if provided
    try:
        if driver_email:
            notify_driver_claim(driver_email, {
                "pickup": result.get("pickup_location", ""),
                "dropoff": result.get("dropoff_location", ""),
                "fare": str(result.get("fare_estimate", "")),
                "eta": "—",
            })
    except Exception:
        pass

    return {"status": "Job claimed", "details": result}

@router.post("/complete")
def complete(job_id: int = Query(..., ge=1)):
    try:
        complete_job(job_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to complete job")
    return {"status": f"Job {job_id} marked complete"}

@router.get("/status")
def job_status(job_id: int = Query(..., ge=1)):
    """
    Returns a rider/driver-friendly status block.
    """
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.get("completed_at"):
        state = "completed"
    elif job.get("claimed"):
        state = "assigned"
    else:
        state = "pending_dispatch"

    return {
        "job_id": job["id"],
        "status": state,
        "summary": {
            "pickup": job.get("pickup_location", ""),
            "dropoff": job.get("dropoff_location", "")
        },
        "fare": {
            "amount": str(job.get("fare_estimate") or ""),
            "currency": "USD"
        },
        "driver": {
            "name": job.get("driver_name") if state != "pending_dispatch" else None
        },
        "timestamps": {
            "posted_at": job.get("posted_at"),
            "completed_at": job.get("completed_at")
        }
    }
