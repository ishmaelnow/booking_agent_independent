# resources/fare_utils.py
# --------------------------------------------------------------
# Keep this as a thin compatibility layer so existing imports don't break.
# We delegate to geo_utils + fare_engine and (optionally) to the LLM node.
# --------------------------------------------------------------

from __future__ import annotations

from resources.geo_utils import estimate_miles
from resources.fare_engine import calculate_base_fare

__all__ = ["estimate_miles", "calculate_base_fare"]
