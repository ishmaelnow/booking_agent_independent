from fastapi import APIRouter, HTTPException
from db.job_board import claim_job, complete_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/claim")
def claim(job_id: int, driver_name: str):
    result = claim_job(job_id, driver_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found or driver mismatch")
    return {"status": "Job claimed", "details": result}

@router.post("/complete")
def complete(job_id: int):
    complete_job(job_id)
    return {"status": f"Job {job_id} marked complete"}