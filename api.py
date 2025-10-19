# api.py
# ============================================================
# Booking Agent API (FastAPI)
# - Keeps ALL existing routes & imports intact
# - Adds safer CORS (env-driven), a lightweight /health route,
#   optional JSON-style logging, Swagger UI at /docs, ReDoc at /redoc,
#   and a sanity check for duplicate routes.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---- Standard lib / env ----
import os
from typing import List

# Optional: load .env in local dev; prod platforms set env vars differently
try:
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
from routes.feedback import router as feedback_router
from routes.track_location import router as track_location_router
from routes.distance import router as distance_router
from routes.live_tracking import router as live_router
from routes.admin import router as admin_router
from routes.quote import router as quote_router
from routes.auth import router as auth_router
from routes.driver_api import router as driver_router
from routes.driver_pin import router as driver_pin_router
from routes.job_pin import router as job_pin_router


# ------------------------------------------------------------
# App with Swagger metadata
# ------------------------------------------------------------
app = FastAPI(
    title="Booking Agent API",
    description="Modular backend for booking, dispatch, tracking, and fare management.",
    version="1.0.0",
    contact={
        "name": "Coach",
        "email": "coachishmael@yahoo.com",
        "url": "https://booking-agent-api-f0d6.onrender.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# ------------------------------------------------------------
# CORS (env-driven, fallback to dev + prod domains)
# ------------------------------------------------------------
origins_csv = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,https://booking-interface-tbd4.onrender.com"
)
ALLOWED_ORIGINS: List[str] = [o.strip() for o in origins_csv.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,   # fine; just don’t use "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

 
# ------------------------------------------------------------
# Healthcheck (MUST stay dependency-free)
# ------------------------------------------------------------
@app.get("/health", tags=["System"])
def health():
    return {"ok": True, "service": "backend"}, 200

# ------------------------------------------------------------
# Register ALL routers (UNCHANGED ORDER)
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
app.include_router(auth_router)
app.include_router(driver_router)
app.include_router(driver_pin_router)
app.include_router(job_pin_router)

# ------------------------------------------------------------
# Optional: JSON-ish logging (nice in Render/Heroku logs)
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
        for k in ("path", "method", "status_code", "request_id"):
            if hasattr(record, k):
                payload[k] = getattr(record, k)
        return json.dumps(payload, ensure_ascii=False)

_root = logging.getLogger()
if not _root.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(JsonFormatter())
    _root.addHandler(_h)
_root.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

# ------------------------------------------------------------
# Optional: Duplicate route detector
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

_warn_on_duplicate_paths()