# routes/auth.py
from __future__ import annotations
import base64, hashlib, hmac, json, os, time
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel

from db.pg import get_conn

router = APIRouter(prefix="/auth", tags=["auth"])

# ---- tiny signed token (not JWT) ----
_SECRET = os.getenv("JWT_SECRET", "change-me").encode()

def _sign(payload: Dict[str, Any]) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode()
    sig = hmac.new(_SECRET, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"

def _verify(token: str) -> Dict[str, Any]:
    try:
        body, sig = token.rsplit(".", 1)
    except ValueError:
        raise HTTPException(status_code=401, detail="invalid token format")
    expected = hmac.new(_SECRET, body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=401, detail="bad token signature")
    payload = json.loads(base64.urlsafe_b64decode(body + "===").decode())
    # optional exp check
    exp = payload.get("exp")
    if exp is not None and time.time() > float(exp):
        raise HTTPException(status_code=401, detail="token expired")
    return payload

def _bearer(authz: Optional[str]) -> str:
    if not authz or not authz.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    return authz.split(" ", 1)[1].strip()

# ------------- Schemas -------------
class DriverLogin(BaseModel):
    email: str
    secret: str

@router.post("/driver/login")
def driver_login(body: DriverLogin):
    """
    Verify driver by (email, api_secret) and return a signed bearer token.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, email FROM drivers WHERE email=%s AND api_secret=%s LIMIT 1",
            (body.email, body.secret),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="invalid driver credentials")

        driver_id, name, email = row

    now = int(time.time())
    payload = {"sub": str(driver_id), "role": "driver", "email": email, "iat": now, "exp": now + 3600}
    token = _sign(payload)
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}

# -------- Dependencies you can use elsewhere --------
def require_driver(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    token = _bearer(authorization)
    claims = _verify(token)
    if claims.get("role") != "driver":
        raise HTTPException(status_code=403, detail="driver role required")
    return claims
