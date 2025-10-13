# routes/feedback.py
# -------------------------------------------------------------------
# POST /book/feedback   (keeping your original path group under /book)
# - Validates rating/comments
# - Best-effort persistence; does not block on notifications
# -------------------------------------------------------------------

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from state import FeedbackInput, feedback_input_to_state, merge_state

# Optional DB
try:
    from db.writer import save_feedback  # expected: save_feedback(payload: dict) -> None
except Exception:
    save_feedback = None

# Reuse book prefix as your original path
router = APIRouter(prefix="/book", tags=["feedback"])

# In-memory fallback store
_FEEDBACKS: List[Dict[str, Any]] = []

@router.post("/feedback")
def submit_feedback(payload: FeedbackInput):
    patch = feedback_input_to_state(payload)
    # Persist if possible
    if save_feedback:
        try:
            save_feedback(patch)
        except Exception:
            # fallback to memory
            _FEEDBACKS.append(patch)
    else:
        _FEEDBACKS.append(patch)

    return {"ok": True, "message": "Thanks for your feedback!"}
