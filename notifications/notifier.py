# notifications/notifier.py
# --------------------------------------------------------------
# Purpose: write a simple operator notification to a log file.
# Adds safe defaults so notes/explanation never show as blank.
# --------------------------------------------------------------

from datetime import datetime
from typing import Dict, Any

LOG_PATH = "notifications.log"

def notify_operator(state: Dict[str, Any]) -> None:
    try:
        notes = (state.get("fare_notes") or "Standard metered fare applied").strip()
        explanation = (state.get("fare_explanation") or "").strip()

        message = (
            f"[{datetime.now().isoformat()}] NEW BOOKING\n"
            f"📍 Pickup: {state.get('pickup_location','')}\n"
            f"🏁 Dropoff: {state.get('dropoff_location','')}\n"
            f"🕒 Time: {state.get('ride_time','')}\n"
            f"📞 Phone: {state.get('phone_number','')}\n"
            f"💰 Fare: ${state.get('fare_estimate','')}\n"
            f"🧾 Notes: {notes}\n"
        )

        if explanation:
            message += f"🧠 Explanation: {explanation}\n"

        message += "-----------------------------\n"

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(message)
    except Exception:
        # Do not raise: notifications are best-effort
        pass
