"""Vercel serverless entrypoint for VittVaani."""
import os
import sys
import traceback

# ── Fix Neon channel_binding on Vercel (causes transaction failures) ──────────
_db_url = os.environ.get("DATABASE_URL", "")
if "channel_binding=require" in _db_url and os.environ.get("VERCEL"):
    os.environ["DATABASE_URL"] = _db_url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from app.main import app as _api_app  # noqa: E402
from data.schemes_seed import seed_schemes  # noqa: E402

# ── Seed DB on first cold start ──────────────────────────────────────────────
def _bootstrap():
    if not os.environ.get("VERCEL"):
        return
    try:
        from app.database import SessionLocal
        from app.models.scheme import Scheme
        with SessionLocal() as db:
            if db.query(Scheme).count() == 0:
                seed_schemes(db)
        print("VittVaani DB bootstrap OK")
    except Exception as exc:
        print("VittVaani DB bootstrap FAILED:", exc)
        traceback.print_exc()

_bootstrap()

# ── Remove the inner root "/" route (returns JSON; conflicts with static) ────
from fastapi.routing import APIRoute
_api_app.router.routes = [
    r for r in _api_app.router.routes
    if not (isinstance(r, APIRoute) and r.path == "/")
]

# ── Mount static frontend ────────────────────────────────────────────────────
from starlette.staticfiles import StaticFiles
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _d in ("backend/frontend", "frontend"):
    _dir = os.path.join(_root, _d)
    if os.path.isdir(_dir):
        _api_app.mount("/", StaticFiles(directory=_dir, html=True), name="static")
        break

# ── Debug endpoint (temporary) ───────────────────────────────────────────────
import json as _json
from fastapi import Request
from starlette.responses import JSONResponse

@_api_app.get("/api/debug")
async def _debug(request: Request):
    info = {"env": {}, "db": {}, "imports": {}}
    # env
    for k in ("DATABASE_URL", "SECRET_KEY", "ENVIRONMENT", "FRONTEND_URL", "VERCEL"):
        v = os.environ.get(k)
        if v and k == "DATABASE_URL":
            v = v[:40] + "..."
        elif v and k == "SECRET_KEY":
            v = v[:8] + "..."
        info["env"][k] = v or "(not set)"
    # imports
    try:
        import bcrypt; info["imports"]["bcrypt"] = bcrypt.__version__
    except Exception as e:
        info["imports"]["bcrypt"] = "FAILED: " + str(e)
    try:
        import jose; info["imports"]["jose"] = "OK"
    except Exception as e:
        info["imports"]["jose"] = "FAILED: " + str(e)
    try:
        import sqlalchemy; info["imports"]["sqlalchemy"] = sqlalchemy.__version__
    except Exception as e:
        info["imports"]["sqlalchemy"] = "FAILED: " + str(e)
    # db
    try:
        from app.database import SessionLocal
        from app.models.user import User
        with SessionLocal() as db:
            info["db"]["users_count"] = db.query(User).count()
            info["db"]["status"] = "OK"
    except Exception as e:
        info["db"]["status"] = "FAILED: " + str(e)
        info["db"]["traceback"] = traceback.format_exc().splitlines()[-3:]
    return info

# ── Register with full error reporting (temporary) ───────────────────────────
from fastapi import Depends
from sqlalchemy.orm import Session as DbSession
from app.database import get_db
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService

@_api_app.post("/api/debug-register")
async def _debug_register(payload: RegisterRequest, db: DbSession = Depends(get_db)):
    try:
        result = AuthService(db).register(payload)
        return {"ok": True, "email": payload.email}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": type(e).__name__, "tb": traceback.format_exc().splitlines()[-10:]}
        )