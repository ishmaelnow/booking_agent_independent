# routes/track_location.py
# -------------------------------------------------------------------
# POST /track/location
# - Validates payload (role enum, pin as string, lat/lng bounds)
# - Uses pg pool
# - Best-effort insert; clear 4xx on bad input, 5xx on DB error
# -------------------------------------------------------------------
from __future__ import annotations
from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from db.pg import get_conn

router = APIRouter(tags=["tracking"])

class Role(str, Enum):
    driver = "driver"
    rider = "rider"

class LocationPayload(BaseModel):
    pin: str = Field(..., min_length=4, max_length=6, description="Digits; kept as string to preserve leading zeros")
    role: Role
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

    @field_validator("pin")
    @classmethod
    def digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("PIN must contain only digits")
        return v

@router.post("/track/location")
def track_location(payload: LocationPayload):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO locations (pin, role, location, timestamp)
                    VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), now())
                    """,
                    (
                        payload.pin,
                        payload.role.value,
                        payload.lng,  # X = longitude
                        payload.lat,  # Y = latitude
                    ),
                )
                conn.commit()
        return {"status": "success"}
    except Exception as e:
        # In prod you might log the exception; keep details light for clients
        raise HTTPException(status_code=500, detail="Failed to record location")
