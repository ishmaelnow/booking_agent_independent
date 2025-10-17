# routes/job_pin.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, root_validator

from db.pg import get_conn

router = APIRouter(prefix="/jobs", tags=["driver-pin"])

class VerifyRequest(BaseModel):
    job_id: int = Field(..., description="Job ID to verify")

    # Accept either 'pin' or 'driver_pin' in the body
    pin: str | None = Field(None, min_length=1, max_length=12, description="Driver PIN")
    driver_pin: str | None = Field(None, min_length=1, max_length=12, description="Driver PIN (legacy key)")

    @root_validator(pre=True)
    def coalesce_pin(cls, values):
        # If user sends only driver_pin, copy it into pin
        if not values.get("pin") and values.get("driver_pin"):
            values["pin"] = values["driver_pin"]
        return values

    # Convenience accessor
    @property
    def pin_value(self) -> str:
        return (self.pin or "").strip()

@router.post("/driver-pin/verify")
def verify_driver_pin(payload: VerifyRequest) -> Dict[str, Any]:
    job_id = payload.job_id
    pin_in = payload.pin_value

    if not pin_in:
        raise HTTPException(status_code=422, detail="pin is required")

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

    stored_pin, expires_at = row[0], row[1]

    if not stored_pin:
        raise HTTPException(status_code=401, detail="no driver pin issued for this job")
    if pin_in != stored_pin:
        raise HTTPException(status_code=401, detail="invalid pin")
    if expires_at is None:
        raise HTTPException(status_code=401, detail="pin has no expiry; reject for safety")

    now_utc = datetime.now(timezone.utc)
    if expires_at <= now_utc:
        raise HTTPException(status_code=401, detail="pin expired")

    return {"ok": True, "job_id": job_id, "status": "valid"}
