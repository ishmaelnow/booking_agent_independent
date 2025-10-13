# state.py
"""
State and schema definitions for the Booking Agent.

Design goals:
- Keep LangGraph compatibility by exposing a dict-like `BookingState` (TypedDict).
- Use Pydantic models to validate/normalize inputs/outputs at API boundaries.
- Group related fields (booking input, fare, dispatch, feedback) to reduce coupling.
- Provide tiny helpers to safely merge partial updates into the state.
"""

from __future__ import annotations

from typing import Optional, TypedDict, NotRequired, Literal, Dict, Any
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict, field_validator, conint, constr

# -----------------------------
# 1) Typed state (dict) for LangGraph
# -----------------------------

class BookingState(TypedDict, total=False):
    """
    The working state we pass around the graph (dict-based for LangGraph).
    All keys are optional so nodes can incrementally enrich the state.
    """
    # ---- Booking input ----
    task: NotRequired[str]                         # e.g. "create_booking"
    pickup_location: NotRequired[str]
    dropoff_location: NotRequired[str]
    ride_time: NotRequired[str]                    # ISO string or natural text pre-normalization
    rider_name: NotRequired[str]
    phone_number: NotRequired[str]                 # store as string to avoid locale/format loss

    # ---- Derived / normalized input ----
    ride_time_iso: NotRequired[str]                # normalized ISO8601 timestamp string

    # ---- Booking output ----
    booking_request: NotRequired[str]              # LLM-composed summary or user-facing draft

    # ---- Fare logic ----
    estimated_miles: NotRequired[float]           # prefer float for quick math; DB can store Decimal
    fare_estimate: NotRequired[str]               # e.g., "$23.50" or "23.50 USD"
    fare_notes: NotRequired[str]
    fare_explanation: NotRequired[str]

    # ---- Dispatch logic ----
    dispatch_info: NotRequired[str]
    driver_name: NotRequired[str]
    vehicle: NotRequired[str]                     # "Toyota Sienna" / "Suburban"
    plate: NotRequired[str]
    eta_minutes: NotRequired[int]                 # non-negative
    pin: NotRequired[str]                         # store as STRING to preserve leading zeros

    # ---- Feedback ----
    feedback_rating: NotRequired[int]             # 1..5
    feedback_comments: NotRequired[str]

    # ---- Meta / tracking ----
    created_at: NotRequired[str]                  # ISO timestamp
    updated_at: NotRequired[str]                  # ISO timestamp
    job_id: NotRequired[str]                      # id in your job table/queue


# -----------------------------
# 2) Pydantic request/response models (strict)
#    These DO NOT replace the state; they validate data entering/exiting your system.
# -----------------------------

# Basic phone pattern; tweak as you like (allows digits, +, (), -, spaces)
PhoneStr = constr(pattern=r"^[0-9\-\+\(\)\s]{7,20}$")

class BookingInput(BaseModel):
    """Incoming fields needed to create a booking."""
    model_config = ConfigDict(extra="forbid")  # reject unknown keys to avoid silent bugs

    task: Literal["create_booking", "estimate_fare"] = "create_booking"  # constrain to known ops
    pickup_location: constr(min_length=2, strip_whitespace=True)
    dropoff_location: constr(min_length=2, strip_whitespace=True)
    ride_time: constr(min_length=1, strip_whitespace=True)               # accept natural text; normalize later
    rider_name: constr(min_length=1, strip_whitespace=True)
    phone_number: PhoneStr

class FareInfo(BaseModel):
    """Derived fare info from fare engine or distance service."""
    model_config = ConfigDict(extra="forbid")

    estimated_miles: float = Field(ge=0.0)         # non-negative
    fare_estimate: Decimal = Field(..., description="Money value in base currency")  # keep as Decimal
    currency: constr(min_length=1, strip_whitespace=True) = "USD"
    fare_notes: Optional[str] = None
    fare_explanation: Optional[str] = None         # LLM explanation, optional

    @field_validator("fare_estimate", mode="before")
    @classmethod
    def coerce_money(cls, v):
        """
        Accept strings like "$23.50" or "23.50", convert to Decimal("23.50").
        """
        if isinstance(v, Decimal):
            return v
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        if isinstance(v, str):
            cleaned = v.replace("$", "").strip()
            return Decimal(cleaned)
        raise TypeError("Invalid fare_estimate")

class DispatchInfo(BaseModel):
    """Assignment details for the driver/vehicle."""
    model_config = ConfigDict(extra="forbid")

    driver_name: constr(min_length=1, strip_whitespace=True)
    vehicle: constr(min_length=1, strip_whitespace=True)                 # e.g., "Toyota Sienna"
    plate: constr(min_length=1, strip_whitespace=True)
    eta_minutes: conint(ge=0) = 0
    pin: constr(min_length=4, max_length=6)                              # keep as string to preserve leading zeros

class FeedbackInput(BaseModel):
    """Rider feedback after the ride."""
    model_config = ConfigDict(extra="forbid")

    rating: conint(ge=1, le=5)
    comments: Optional[str] = None

class BookingCreated(BaseModel):
    """
    Example response payload when a booking is created.
    (Use in your /book/ride endpoint response_model.)
    """
    model_config = ConfigDict(extra="forbid")

    job_id: str
    pin: str
    message: str = "Booking created"


# -----------------------------
# 3) Helpers to convert/merge between Pydantic models and the dict state
# -----------------------------

def now_iso() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def merge_state(state: BookingState, patch: Dict[str, Any]) -> BookingState:
    """
    Shallow merge only defined keys (ignores None). Returns the same dict for convenience.
    This avoids accidentally overwriting fields with None from partial updates.
    """
    for k, v in patch.items():
        if v is not None:
            state[k] = v  # inline: TypedDict is just a dict at runtime
    state.setdefault("updated_at", now_iso())
    return state

def booking_input_to_state(b: BookingInput) -> BookingState:
    """
    Convert validated BookingInput to initial BookingState.
    Also stamps created/updated timestamps.
    """
    d: BookingState = {
        "task": b.task,
        "pickup_location": b.pickup_location,
        "dropoff_location": b.dropoff_location,
        "ride_time": b.ride_time,              # keep raw; normalize later in a node
        "rider_name": b.rider_name,
        "phone_number": b.phone_number,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    return d

def fare_info_to_state(f: FareInfo) -> BookingState:
    """
    Convert validated FareInfo to state patch (keeps Decimal as string for JSON safety).
    """
    return {
        "estimated_miles": float(f.estimated_miles),
        "fare_estimate": str(f.fare_estimate),     # inline: avoid float precision issues
        "fare_notes": f.fare_notes or "",
        "fare_explanation": f.fare_explanation or "",
        "updated_at": now_iso(),
    }

def dispatch_info_to_state(disp: DispatchInfo) -> BookingState:
    """
    Convert validated DispatchInfo to state patch.
    """
    return {
        "driver_name": disp.driver_name,
        "vehicle": disp.vehicle,
        "plate": disp.plate,
        "eta_minutes": int(disp.eta_minutes),
        "pin": disp.pin,                           # keep as string to preserve leading zeros
        "updated_at": now_iso(),
    }

def feedback_input_to_state(f: FeedbackInput) -> BookingState:
    """
    Convert validated FeedbackInput to state patch.
    """
    return {
        "feedback_rating": int(f.rating),
        "feedback_comments": f.comments or "",
        "updated_at": now_iso(),
    }
