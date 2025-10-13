# api.py
# ============================================================
# Booking Agent API (FastAPI)
# - Keeps ALL existing routes & imports intact
# - Adds safer CORS (env-driven), a lightweight /health route,
#   optional JSON-style logging, and a sanity check for duplicate routes.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---- Standard lib / env ----
import os
from typing import List

# Optional: load .env in local dev; prod platforms set env vars differently
try:  # inline: guard so prod doesn't fail if python-dotenv isn't installed
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ✅ Import routers from routes/ (UNCHANGED)
from routes.book import router as book_router
from routes.complete_ride import router as complete_router
from routes.driver_api import router as driver_router
from routes.job_api import router as job_router
from routes.job_view_api import router as job_view_router
from routes.booking_api import router as booking_router
from routes.fare_api import router as fare_api_router
from routes.fare_preview import router as fare_preview_router
from routes.feedback import router as feedback_router  # ✅ NEW
from routes.track_location import router as track_location_router  # ✅ NEW
from routes.distance import router as distance_router
from routes.live_tracking import router as live_router
from routes.admin import router as admin_router
from routes.quote import router as quote_router





# ------------------------------------------------------------
# App
# ------------------------------------------------------------
app = FastAPI(title="Booking Agent API")  # keep title so existing clients don't break

# ------------------------------------------------------------
# CORS (tighten from "*" to env-driven list)
#   - Do NOT use "*" in production if you send credentials/cookies.
#   - Configure allowed frontends via CORS_ORIGINS env (CSV).
# ------------------------------------------------------------
origins_csv = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
ALLOWED_ORIGINS: List[str] = [o.strip() for o in origins_csv.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,   # inline: restrict to your UI(s)
    allow_credentials=True,          # inline: allow cookies/session if needed later
    allow_methods=["*"],             # inline: typical for APIs
    allow_headers=["*"],             # inline: Authorization, Content-Type, etc.
)

# Optional: TrustedHostMiddleware if you want to pin hostnames in prod
# from starlette.middleware.trustedhost import TrustedHostMiddleware
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com", "localhost", "127.0.0.1"])

# ------------------------------------------------------------
# Healthcheck (MUST stay dependency-free: no DB/LLM calls)
# ------------------------------------------------------------
@app.get("/health")
def health():
    # inline: keeps uptime checks from cascading failures during DB/LLM issues
    return {"ok": True, "service": "backend"}, 200

# ------------------------------------------------------------
# Register ALL routers (UNCHANGED ORDER to avoid surprises)
# ------------------------------------------------------------
app.include_router(book_router)
app.include_router(complete_router)
app.include_router(driver_router)
app.include_router(job_router)
app.include_router(job_view_router)
app.include_router(booking_router)
app.include_router(fare_api_router)
app.include_router(fare_preview_router)
app.include_router(feedback_router)
app.include_router(track_location_router)
app.include_router(distance_router)
app.include_router(live_router)
app.include_router(admin_router)
app.include_router(quote_router)


# ------------------------------------------------------------
# Optional: JSON-ish logging (nice in Render/Heroku logs)
#   - Safe: only attaches a StreamHandler if none exists.
# ------------------------------------------------------------
import logging, json, time

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": int(time.time()),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # if you later add middleware to enrich records, these will show up
        for k in ("path", "method", "status_code", "request_id"):
            if hasattr(record, k):
                payload[k] = getattr(record, k)
        return json.dumps(payload, ensure_ascii=False)

_root = logging.getLogger()
if not _root.handlers:                       # inline: avoid duplicating handlers
    _h = logging.StreamHandler()
    _h.setFormatter(JsonFormatter())
    _root.addHandler(_h)
_root.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

# ------------------------------------------------------------
# Optional: Duplicate route detector (warn-only; no behavior change)
#   - Useful because your route dump showed /bookings/view twice.
# ------------------------------------------------------------
def _warn_on_duplicate_paths() -> None:
    try:
        seen = {}
        for r in app.routes:
            methods = tuple(sorted(getattr(r, "methods", []) or []))
            path = getattr(r, "path", None)
            if not path or not methods:
                continue
            key = (path, methods)
            seen.setdefault(key, []).append(getattr(r, "name", ""))
        dups = {k: v for k, v in seen.items() if len(v) > 1}
        if dups:
            logging.warning(
                json.dumps({
                    "event": "duplicate_routes_detected",
                    "duplicates": [
                        {"path": p, "methods": list(m), "handlers": v}
                        for (p, m), v in dups.items()
                    ]
                })
            )
    except Exception as e:
        logging.debug(f"route-dup-check failed: {e}")

_warn_on_duplicate_paths()  # inline: log-only; does not modify routing
