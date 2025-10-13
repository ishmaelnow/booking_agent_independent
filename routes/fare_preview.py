# routes/fare_preview.py
# -------------------------------------------------------------------
# GET /fare/preview?miles=...
# Light-weight preview: “What would the fare be for X miles?”
# - Uses the same fare engine as bookings
# - Returns consistent, customer-friendly wording (no formula dump)
# -------------------------------------------------------------------

from __future__ import annotations

from fastapi import APIRouter, Query
from typing import Optional, Dict, Any

from resources.fare_engine import calculate_base_fare  # returns Decimal

router = APIRouter(prefix="/fare", tags=["Fare Preview"])


def _friendly_explanation(miles: float, fare_str: str) -> str:
    # Match the short phrasing you approved elsewhere
    return (
        f"Estimated fare ${fare_str} for about {miles:.2f} miles. "
        "Final price may vary with traffic, route, and wait time."
    )


@router.get("/preview", summary="Preview a fare for a given distance")
def preview_fare(
    miles: float = Query(..., gt=0, description="Assumed trip length in miles"),
    explain: Optional[bool] = Query(True, description="Include a short natural-language line"),
) -> Dict[str, Any]:
    fare = calculate_base_fare(miles)          # Decimal
    fare_str = f"{fare:.2f}"                   # money stays a string in responses

    response: Dict[str, Any] = {
        "input_miles": float(miles),
        "fare_estimate": fare_str,
    }

    if explain:
        response["fare_explanation"] = _friendly_explanation(miles, fare_str)

    return response
