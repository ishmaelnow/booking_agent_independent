# nodes/explain_fare.py
# --------------------------------------------------------------
# Deterministic fare explanation (polished, rider-friendly).
# No formulas, no debug fields. Optional LLM paraphrase is
# supported via USE_LLM_EXPLANATION=1 but is OFF by default.
# --------------------------------------------------------------

from __future__ import annotations
import os
from decimal import Decimal
from typing import Dict, Any

from dotenv import load_dotenv
load_dotenv()

from resources.geo_utils import estimate_miles
from resources.fare_engine import calculate_base_fare

# Feature flag: keep LLM OFF by default
USE_LLM = os.getenv("USE_LLM_EXPLANATION", "0") == "1"

# Optional LLM (only used if USE_LLM=1 and init succeeds)
fare_chain = None
if USE_LLM:
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You write short, polished fare explanations for riders."),
            ("human", "Explain in one sentence why the estimated fare from {pickup} to {dropoff} is ${fare}. Be friendly and clear, with no formulas.")
        ])
        fare_chain = prompt | llm
    except Exception:
        fare_chain = None  # fail-soft: stick with template


def _rider_copy(pickup: str, dropoff: str, miles: float, fare: Decimal) -> str:
    """
    Single, professional sentence with no formulas.
    """
    return (
        f"Estimated fare ${fare:.2f} for about {miles:.1f} miles from "
        f"{pickup or 'pickup'} to {dropoff or 'destination'}. "
        "Final price may vary with traffic, route, and wait time."
    )


def explain_fare_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    pickup = (state.get("pickup_location") or "").strip()
    dropoff = (state.get("dropoff_location") or "").strip()

    miles = estimate_miles(pickup, dropoff)
    fare: Decimal = calculate_base_fare(miles)

    # Default polished copy
    explanation = _rider_copy(pickup, dropoff, miles, fare)

    # Optional LLM paraphrase (still short, no formulas)
    if fare_chain is not None:
        try:
            res = fare_chain.invoke({
                "pickup": pickup or "the pickup",
                "dropoff": dropoff or "the destination",
                "fare": f"{fare:.2f}",
            })
            text = getattr(res, "content", "") or ""
            if text.strip():
                explanation = text.strip()
        except Exception:
            pass  # keep template

    return {
        **state,
        "estimated_miles": float(miles),
        "fare_estimate": f"{fare:.2f}",     # string for JSON-safety
        "fare_explanation": explanation,    # rider-friendly, no formulas
    }
