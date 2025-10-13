# routes/quote.py
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any

from resources.fare_helpers import get_fare_quote

router = APIRouter(prefix="/quote", tags=["quote"])

class QuoteInput(BaseModel):
    pickup_location: str = Field(..., examples=["Times Square, NYC"])
    dropoff_location: str = Field(..., examples=["JFK Airport"])

@router.post("", summary="Get a fare quote without booking")
def get_quote(payload: QuoteInput) -> Dict[str, Any]:
    return get_fare_quote(payload.pickup_location, payload.dropoff_location)
