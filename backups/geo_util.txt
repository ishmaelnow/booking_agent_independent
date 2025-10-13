from geopy.distance import geodesic
import geocoder

def estimate_miles(pickup: str, dropoff: str) -> float:
    try:
        p = geocoder.osm(pickup, headers={"User-Agent": "booking-agent"})
        d = geocoder.osm(dropoff, headers={"User-Agent": "booking-agent"})
        if p.ok and d.ok:
            return round(geodesic((p.lat, p.lng), (d.lat, d.lng)).miles, 2)
    except Exception:
        pass
    return 10.0  # fallback default