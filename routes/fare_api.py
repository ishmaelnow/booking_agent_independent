# routes/fare_api.py
# -------------------------------------------------------------------
# GET /fare/estimate?pickup=...&dropoff=...[&explain=true]
# - Validates query params
# - Reuses explain_fare_fn (single source of truth)
# - Returns miles, fare (as string), and optional explanation
# -------------------------------------------------------------------

# routes/fare_api.py
from __future__ import annotations

from typing import Optional, Dict, Any
from fastapi import APIRouter, Query

from resources.fare_helpers import get_fare_quote

router = APIRouter(prefix="/fare", tags=["fare"])

@router.get("/estimate", summary="Get a fare estimate without booking")
def estimate_fare(
    pickup: str = Query(..., min_length=2, description="Pickup location"),
    dropoff: str = Query(..., min_length=2, description="Dropoff location"),
    explain: Optional[bool] = Query(True, description="Include natural-language explanation"),
) -> Dict[str, Any]:
    result = get_fare_quote(pickup, dropoff)
    if not explain:
        result.pop("fare_explanation", None)
    return result

