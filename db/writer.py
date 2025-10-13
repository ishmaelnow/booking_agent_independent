# db/writer.py
# --------------------------------------------------------------------
# Persists jobs and assignments.
# Guarantees: we try hard to persist a non-null fare_estimate:
#   - Prefer value from `state["fare_estimate"]`
#   - If missing/unparseable, we compute a fallback using geo_utils + fare_engine
#     (so DB rows aren't left with NULL fare_estimate by accident).
# --------------------------------------------------------------------

from __future__ import annotations

from typing import Dict, Any, List, Optional
from decimal import Decimal, InvalidOperation

from psycopg2.extras import RealDictCursor

from db.pg import get_conn


# ---------- helpers ----------

def _coerce_fare(value: Optional[Any]) -> Optional[float]:
    """
    Accepts a fare that might be str/float/Decimal/None and returns a float or None.
    Examples:
      "23.45" -> 23.45
      23.45   -> 23.45
      None    -> None
      "abc"   -> None
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(Decimal(str(value)))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _compute_fare_fallback(pickup: str, dropoff: str) -> Optional[float]:
    """
    As a last resort, compute a fare if the state didn't include one.
    This keeps DB consistent even if the route mistakenly inserted before running the fare node.
    """
    try:
        # Lazy imports to avoid module cycles on import graph
        from resources.geo_utils import estimate_miles
        from resources.fare_engine import calculate_base_fare
        miles = estimate_miles(pickup, dropoff)          # float
        fare = calculate_base_fare(miles)                # Decimal | float
        return float(fare)
    except Exception:
        return None


# ---------- writes ----------

def create_job(state: dict) -> int:
    """
    Insert a job row and return the new id.

    Reads (at minimum):
      - pickup_location, dropoff_location, rider_name, phone_number
    Tries to persist:
      - fare_estimate (numeric) using state['fare_estimate'] if present,
        otherwise computes a fallback so it won't be NULL.
    """
    pickup = (state.get("pickup_location") or "").strip()
    dropoff = (state.get("dropoff_location") or "").strip()
    rider_name = (state.get("rider_name") or "").strip()
    phone_number = (state.get("phone_number") or "").strip()

    # 1) Prefer fare from state (produced by nodes/explain_fare.py)
    fare_estimate_value = _coerce_fare(state.get("fare_estimate"))

    # 2) Last-resort fallback so DB doesn't end up with NULL
    if fare_estimate_value is None and pickup and dropoff:
        fare_estimate_value = _compute_fare_fallback(pickup, dropoff)

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO jobs (
                pickup_location,
                dropoff_location,
                rider_name,
                phone_number,
                fare_estimate,   -- persisted as numeric if available
                claimed,
                driver_id,
                driver_name
            )
            VALUES (%s, %s, %s, %s, %s, false, NULL, NULL)
            RETURNING id
            """,
            (
                pickup,
                dropoff,
                rider_name,
                phone_number,
                fare_estimate_value,   # may be None if everything failed; DB column should allow NULL
            ),
        )
        job_id = cur.fetchone()[0]
        conn.commit()
        return int(job_id)


def assign_job_to_driver(job_id: int, driver_id: int, driver_name: str) -> None:
    """
    Mark a job as claimed and link it to a driver.
    - sets jobs.driver_id, jobs.driver_name
    - sets jobs.claimed = true
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE jobs
            SET driver_id = %s,
                driver_name = %s,
                claimed = true
            WHERE id = %s
            """,
            (driver_id, driver_name, job_id),
        )
        conn.commit()


# ---------- reads (for /book/history) ----------

def list_bookings(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Return recent bookings for /book/history.

    NOTE: We order by COALESCE(posted_at, created_at, id) DESC to stay resilient
    across environments where one of posted_at/created_at might not exist or be null.
    The `id` fallback guarantees stable ordering if the timestamps aren't present.
    """
    sql = """
        SELECT
          id,
          pickup_location,
          dropoff_location,
          fare_estimate,
          claimed
        FROM jobs
        ORDER BY COALESCE(posted_at, created_at, id::bigint) DESC
        LIMIT %s OFFSET %s
    """
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (limit, offset))
        rows = cur.fetchall() or []
        return [dict(r) for r in rows]
