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
from starlette.responses import JSONResponse, RedirectResponse  # noqa: E402
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

# Clean-URL support: serve /partners from partners.html (address bar stays
# clean) and 301-redirect legacy .html URLs to their clean form.
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_static_dir = None
for _d in ("backend/frontend", "frontend"):
    _dir = os.path.join(_root, _d)
    if os.path.isdir(_dir):
        _static_dir = _dir
        break

_API_PREFIXES = ("/api", "/docs", "/openapi", "/redoc")


@_api_app.middleware("http")
async def _clean_urls(request: Request, call_next):
    path = request.url.path
    if path.endswith(".html"):
        clean = path[:-5] or "/"
        return RedirectResponse(url=str(request.url.replace(path=clean)), status_code=301)
    if (
        _static_dir
        and not path.startswith(_API_PREFIXES)
        and "." not in path.rsplit("/", 1)[-1]  # not a file asset
    ):
        candidate = path.strip("/") or "index"
        full = os.path.join(_static_dir, candidate + ".html")
        if os.path.isfile(full):
            request.scope["path"] = "/" + candidate + ".html"
            request.scope["raw_path"] = ("/" + candidate + ".html").encode("latin-1")
    return await call_next(request)


# Mount static frontend
if _static_dir:
    _api_app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")

app = _api_app