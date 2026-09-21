"""Vercel serverless entrypoint for VittVaani."""
import os
import sys
import traceback

# Fix Neon channel_binding on Vercel (causes write failures)
_db_url = os.environ.get("DATABASE_URL", "")
if "channel_binding=require" in _db_url and os.environ.get("VERCEL"):
    os.environ["DATABASE_URL"] = _db_url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from fastapi import Request  # noqa: E402
from fastapi.routing import APIRoute  # noqa: E402
from starlette.responses import JSONResponse  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

from app.main import app as _api_app  # noqa: E402
from data.schemes_seed import seed_schemes  # noqa: E402
from data.partners_seed import seed_partners  # noqa: E402

# Seed DB on first cold start
if os.environ.get("VERCEL"):
    try:
        from app.database import SessionLocal
        from app.models.scheme import Scheme
        from app.models.channel_partner import ChannelPartner
        with SessionLocal() as db:
            if db.query(Scheme).count() == 0:
                seed_schemes(db)
            if db.query(ChannelPartner).count() == 0:
                seed_partners(db)
    except Exception as exc:
        print("DB bootstrap skipped:", exc)

# Remove inner root "/" route (conflicts with static index.html)
_api_app.router.routes = [
    r for r in _api_app.router.routes
    if not (isinstance(r, APIRoute) and r.path == "/")
]

# Exception handler: always log + return error detail
async def _on_error(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"UNHANDLED {type(exc).__name__}: {exc}")
    print(tb)
    return JSONResponse(
        {"error": f"{type(exc).__name__}: {exc}"},
        status_code=500,
    )

_api_app.add_exception_handler(Exception, _on_error)

# Mount static frontend
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _d in ("backend/frontend", "frontend"):
    _dir = os.path.join(_root, _d)
    if os.path.isdir(_dir):
        _api_app.mount("/", StaticFiles(directory=_dir, html=True), name="static")
        break

app = _api_app