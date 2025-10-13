# resources/geo_utils.py
# --------------------------------------------------------------
# Purpose:
#   - Geocode addresses with OpenStreetMap (via `geocoder`)
#   - Provide distance estimation (geodesic miles)
#   - Provide a reusable (lng, lat) geocode helper for dispatch
#
# Features:
#   - Explicit User-Agent (OSM/Nominatim policy)
#   - Timeout + light retries
#   - LRU cache to avoid hammering OSM for repeated inputs
#   - Graceful fallbacks so the API remains reliable
# --------------------------------------------------------------

from __future__ import annotations

from functools import lru_cache
from typing import Tuple, Optional
import time

from geopy.distance import geodesic
import geocoder

# Be a good API citizen with an identifying User-Agent
UA = {"User-Agent": "booking-agent/1.0 (contact: ops@yourdomain.com)"}

# Network behavior
TIMEOUT_SEC = 6           # request timeout to OSM
RETRIES = 2               # minimal retry attempts
RETRY_SLEEP = 0.35        # seconds between retries

# Fallback when geocoding fails or inputs are missing
FALLBACK_MILES = 10.0


# ----------------------------
# Internal geocoding utilities
# ----------------------------

def _geocode_once(query: str):
    """
    Single OSM request. We keep this tiny wrapper to centralize headers/timeouts.
    """
    return geocoder.osm(query, headers=UA, timeout=TIMEOUT_SEC)


def _geocode_with_retry(query: str):
    """
    Try a couple of times; return a geocoder result or None.
    """
    last_err: Exception | None = None
    for _ in range(RETRIES + 1):
        try:
            res = _geocode_once(query)
            if res and res.ok and res.lat is not None and res.lng is not None:
                return res
        except Exception as e:
            last_err = e  # you could log this
        time.sleep(RETRY_SLEEP)
    # Optionally log last_err
    return None


@lru_cache(maxsize=1024)
def _coords_lat_lng(query: str) -> Optional[Tuple[float, float]]:
    """
    Cached geocode result as (lat, lng) tuple, or None if not found.
    """
    res = _geocode_with_retry(query)
    if not res:
        return None
    return (float(res.lat), float(res.lng))


# ----------------------------
# Public helpers
# ----------------------------

def geocode_lng_lat(address: str, retries: int = RETRIES, delay: float = RETRY_SLEEP) -> Optional[Tuple[float, float]]:
    """
    Geocode a free-form address string to a (lng, lat) tuple.

    Returns:
        (lng, lat) on success, or None on failure.

    Notes:
        - Uses an LRU-cached path to avoid repeated external calls.
        - `retries`/`delay` are kept for API parity; the cached function already
          includes a minimal retry internally.
    """
    addr = (address or "").strip()
    if not addr:
        return None

    # Use the cached (lat, lng) then flip the order for convenience in mapping/DB
    latlng = _coords_lat_lng(addr)
    if not latlng:
        return None
    lat, lng = latlng
    return (lng, lat)


def estimate_miles(pickup: str, dropoff: str) -> float:
    """
    Return rounded miles between pickup and dropoff using geodesic distance.

    If geocoding fails for either endpoint, return a conservative default so the
    booking flow can continue without blocking.

    Args:
        pickup:  Free-form address string
        dropoff: Free-form address string

    Returns:
        Miles as float (rounded to 2 decimals), or FALLBACK_MILES on failure.
    """
    p = (pickup or "").strip()
    d = (dropoff or "").strip()
    if not p or not d:
        return FALLBACK_MILES

    # If exact same text, treat as zero distance
    if p.lower() == d.lower():
        return 0.0

    p_latlng = _coords_lat_lng(p)
    d_latlng = _coords_lat_lng(d)
    if not p_latlng or not d_latlng:
        return FALLBACK_MILES

    miles = geodesic(p_latlng, d_latlng).miles
    return round(float(miles), 2)
