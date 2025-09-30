from fastapi import APIRouter, Form
from db.job_board import complete_job  # ✅ Fixed import

router = APIRouter(prefix="/complete", tags=["Completion"])

@router.post("/ride")
def complete_ride(job_id: int = Form(...), driver_name: str = Form(...)):
    complete_job(job_id)
    return {"status": f"Job {job_id} completed by {driver_name}"}