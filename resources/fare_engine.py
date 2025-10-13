# resources/fare_engine.py
# --------------------------------------------------------------
# Money-safe fare calculation using Decimal to avoid float issues.
# Rates are env-driven with sensible defaults.
# --------------------------------------------------------------

from __future__ import annotations

import os
from decimal import Decimal, ROUND_HALF_UP

# Read from env with sane defaults (strings → Decimal)
BASE_FARE = Decimal(os.getenv("FARE_BASE", "3.00"))
PER_MILE  = Decimal(os.getenv("FARE_PER_MILE", "4.00"))
MULTIPLIER = Decimal(os.getenv("FARE_MULTIPLIER", "0.70"))  # dynamic pricing factor

def _money(d: Decimal) -> Decimal:
    # Normalize to 2 decimals with bankers' rounding style common to USD
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_base_fare(miles: float) -> Decimal:
    # Guard: negative or NaN miles → treat as 0
    try:
        m = Decimal(str(max(0.0, float(miles))))
    except Exception:
        m = Decimal("0")
    fare = BASE_FARE + (m * PER_MILE * MULTIPLIER)
    return _money(fare)
