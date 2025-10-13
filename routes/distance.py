# routes/distance.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from resources.geo_utils import estimate_miles

router = APIRouter(tags=["distance"])

class DistanceReq(BaseModel):
    pickup: str = Field(..., min_length=2)
    dropoff: str = Field(..., min_length=2)

@router.post("/distance")
def calculate_distance(body: DistanceReq):
    miles = estimate_miles(body.pickup, body.dropoff)
    return {"miles": miles}
