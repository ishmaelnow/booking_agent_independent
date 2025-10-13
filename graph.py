# graph.py
# -------------------------------------------------------------
# Booking LangGraph:
#   generate_booking  -> explain_fare  -> [dispatch or end]
# - Uses dict-based state (BookingState) for LangGraph compatibility
# - Avoids name collision with FastAPI's `app` by exporting `booking_graph`
# - Optional dispatch: skip if `task == "estimate_fare"`
# -------------------------------------------------------------

from __future__ import annotations

import sys
import os
from typing import Dict, Any

# Ensure relative imports work when launched from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import BookingState
from nodes.generate_booking import generate_booking
from nodes.explain_fare import explain_fare_fn

# Dispatcher may not be available in early dev. Fail-soft with a no-op.
try:
    from dispatch.dispatcher import dispatch_booking
except Exception:
    def dispatch_booking(state: Dict[str, Any]) -> Dict[str, Any]:
        # No-op dispatch fallback, keeps graph functional in dev
        return {**state, "dispatch_info": state.get("dispatch_info", "pending (dev-noop)")}

from langgraph.graph import StateGraph, END

# -----------------------------
# Build the graph
# -----------------------------
graph = StateGraph(BookingState)

# Register nodes (functions must accept & return dict-like state)
graph.add_node("generate_booking", generate_booking)
graph.add_node("explain_fare", explain_fare_fn)
graph.add_node("dispatch", dispatch_booking)

# Static linear edges up to explain
graph.add_edge("generate_booking", "explain_fare")

# Conditional edge after explanation:
# If task == "estimate_fare", end early (no dispatch).
# Otherwise, proceed to dispatch.
def decide_after_explain(state: BookingState) -> str:
    task = (state.get("task") or "").strip().lower()
    return END if task == "estimate_fare" else "dispatch"

graph.add_conditional_edges(
    "explain_fare",
    decide_after_explain,
    {
        END: END,             # stop here if just estimating
        "dispatch": "dispatch"
    }
)

# Entry point
graph.set_entry_point("generate_booking")

# Compile once and export under a non-conflicting name
booking_graph = graph.compile()

# -----------------------------
# Convenience wrapper for routes
# -----------------------------
def run_booking_flow(state: BookingState) -> BookingState:
    """
    Execute the booking graph synchronously and return the final state.
    Call this from your FastAPI route.

    Example:
        state = booking_input_to_state(payload)
        final_state = run_booking_flow(state)
    """
    # booking_graph.invoke returns the updated state dict
    return booking_graph.invoke(state)
