# dispatch/dispatcher.py
# --------------------------------------------------------------
# Choose the nearest available driver using the *real* pickup
# coordinates obtained via geocoding, then assign and reserve.
# --------------------------------------------------------------

from __future__ import annotations
from typing import Dict, Any

from resources.geo_utils import geocode_lng_lat, FALLBACK_MILES
from db.driver_registry import find_nearest_available_driver, set_driver_availability
from db.writer import assign_job_to_driver


def _pickup_lng_lat_from_state(state: Dict[str, Any]) -> tuple[float, float] | None:
    """
    Geocode the pickup_location in the state and return (lng, lat).
    If geocoding fails, return None (we'll handle a graceful fallback).
    """
    pickup = (state.get("pickup_location") or "").strip()
    if not pickup:
        return None
    return geocode_lng_lat(pickup)  # -> (lng, lat) or None


def dispatch_booking(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    1) Geocode pickup to (lng, lat)
    2) Query nearest available driver (PostGIS KNN) using that point
    3) If none: return a 'pending' response
    4) If found: assign job + mark driver unavailable + enrich response
    """
    coords = _pickup_lng_lat_from_state(state)
    if coords is None:
        # No geocode result -> do not crash the flow; tell the user gracefully
        return {
            **state,
            "dispatch_info": "❌ Could not determine pickup location precisely yet. Please try again in a moment.",
            "driver_name": None,
            "vehicle": None,
            "plate": None,
            "eta_minutes": None,
        }

    lng, lat = coords
    driver = find_nearest_available_driver(lng, lat)

    if not driver:
        return {
            **state,
            "dispatch_info": "❌ No available drivers at the moment.",
            "driver_name": None,
            "vehicle": None,
            "plate": None,
            "eta_minutes": None,
        }

    # We have a driver — assign the job and mark the driver unavailable
    job_id = int(state["job_id"])  # job_id must already be persisted by /book/ride
    assign_job_to_driver(job_id, driver_id=driver["id"], driver_name=driver["name"])
    set_driver_availability(driver["id"], False)

    # Simple ETA placeholder (you can replace with real routing later)
    eta_minutes = 8

    dispatch_info = (
        f"✅ Driver Assigned: {driver['name']} ({driver.get('vehicle', '?')}, {driver.get('plate', '?')})\n"
        f"⏱️ ETA: {eta_minutes} minutes"
    )

    return {
        **state,
        "dispatch_info": dispatch_info,
        "driver_name": driver["name"],
        "vehicle": driver.get("vehicle"),
        "plate": driver.get("plate"),
        "eta_minutes": eta_minutes,
    }
