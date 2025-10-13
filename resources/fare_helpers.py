# resources/fare_helpers.py
# Single source of truth for fare quotes used by both /fare/estimate (GET)
# and /quote (POST). Keeps wording consistent with bookings.

from __future__ import annotations
from typing import Dict, Any

# Reuse the same node that bookings use (computes miles + fare + explanation)
from nodes.explain_fare import explain_fare_fn

def get_fare_quote(pickup: str, dropoff: str) -> Dict[str, Any]:
    """
    Return a normalized fare quote payload:
      - pickup_location
      - dropoff_location
      - estimated_miles (float)
      - fare_estimate (string money, e.g. "40.52")
      - fare_explanation (polished, no formulas)
    """
    state = {
        "pickup_location": (pickup or "").strip(),
        "dropoff_location": (dropoff or "").strip(),
    }
    out = explain_fare_fn(state)
    return {
        "pickup_location": state["pickup_location"],
        "dropoff_location": state["dropoff_location"],
        "estimated_miles": out.get("estimated_miles"),
        "fare_estimate": out.get("fare_estimate"),
        "fare_explanation": out.get("fare_explanation"),
    }
