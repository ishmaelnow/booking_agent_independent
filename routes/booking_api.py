# routes/booking_api.py
# -------------------------------------------------------------------
# GET /bookings/view
# - Mirrors your existing endpoint but with pagination + consistent shape
# - Avoids double-registration issues (keep only ONE include_router in api.py)
# -------------------------------------------------------------------

from __future__ import annotations

from typing import List, Dict, Any
from fastapi import APIRouter, Query

# Optional DB (reader); fallback to in-memory from book.py if not present
try:
    from db.reader import list_bookings
except Exception:
    list_bookings = None

# Import the in-memory fallback list from book.py to avoid duplication
try:
    from .book import _FALLBACK_BOOKINGS  # type: ignore
except Exception:
    _FALLBACK_BOOKINGS = []  # worst case, empty

router = APIRouter(prefix="/bookings", tags=["bookings"])

def _list_bookings(limit: int, offset: int) -> List[Dict[str, Any]]:
    if list_bookings:
        try:
            return list_bookings(limit=limit, offset=offset)
        except Exception:
            pass
    return _FALLBACK_BOOKINGS[offset : offset + limit]

@router.get("/view")
def view_bookings(
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    items = _list_bookings(limit=limit, offset=offset)
    return {"ok": True, "count": len(items), "items": items}
