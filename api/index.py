"""Vercel serverless entrypoint for VittVaani."""
import os
import sys

# Fix Neon channel_binding on Vercel (causes write failures)
_db_url = os.environ.get("DATABASE_URL", "")
if "channel_binding=require" in _db_url and os.environ.get("VERCEL"):
    os.environ["DATABASE_URL"] = _db_url.replace("&channel_binding=require", "").replace("?channel_binding=require", "")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from fastapi.routing import APIRoute  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

from app.main import app as _api_app  # noqa: E402
from data.schemes_seed import seed_schemes  # noqa: E402

# Seed DB on first cold start
if os.environ.get("VERCEL"):
    try:
        from app.database import SessionLocal
        from app.models.scheme import Scheme
        with SessionLocal() as db:
            if db.query(Scheme).count() == 0:
                seed_schemes(db)
    except Exception as exc:
        print("DB bootstrap skipped:", exc)

# Remove inner root "/" route (conflicts with static index.html)
_api_app.router.routes = [
    r for r in _api_app.router.routes
    if not (isinstance(r, APIRoute) and r.path == "/")
]

# Mount static frontend (inside backend/ since Vercel ships that dir)
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _d in ("backend/frontend", "frontend"):
    _dir = os.path.join(_root, _d)
    if os.path.isdir(_dir):
        _api_app.mount("/", StaticFiles(directory=_dir, html=True), name="static")
        break

app = _api_app