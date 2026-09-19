"""Vercel serverless entrypoint for the VittVaani FastAPI backend.

Routing model (verified against the live deployment):
- Vercel routes `/api` and its subpaths to this function natively and
  preserves the original path (`scope["path"] == "/api/..."`), so the FastAPI
  routers registered under `/api` match directly. No prefix stripping needed.
- Any path that is NOT a route (``, `/login.html`, `/css/*`, ...) ALSO falls
  through to this function with the original path intact, so the frontend is
  served here via ``StaticFiles`` mounted at ``/`` with ``html=True``.

`VERCEL=1` triggers the production bootstrap: `app.main` creates the tables on
import, and the scheme catalog is seeded (idempotently) on the first cold start.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from fastapi.routing import APIRoute  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

from app.main import app as _api_app  # noqa: E402  (import also runs create_all)
from data.schemes_seed import seed_schemes  # noqa: E402


def _bootstrap_production_db():
    if not os.environ.get("VERCEL"):
        return
    try:
        from app.database import SessionLocal
        from app.models.scheme import Scheme  # noqa: F401

        with SessionLocal() as db:
            if db.query(Scheme).count() == 0:
                seed_schemes(db)
    except Exception as exc:  # pragma: no cover - DB unreachable at cold start
        print("VittVaani production DB bootstrap skipped:", exc)


_bootstrap_production_db()

_api_app.router.routes = [
    r for r in _api_app.router.routes
    if not (isinstance(r, APIRoute) and r.path == "/")
]

_frontend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.isdir(_frontend):
    _api_app.mount("/", app=StaticFiles(directory=_frontend, html=True), name="static")


class _DiagApp:
    """Echoes the raw ASGI scope when the `x-vv-diag: 1` header is present.

    Temporary debugging aid for verifying Vercel's path handling; harmless in
    production (returns JSON only for that exact header).
    """

    def __init__(self, target):
        self.target = target

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers") or [])
            if b"x-vv-diag" in headers:
                body = json.dumps({
                    "path": scope.get("path"),
                    "raw_path": (scope.get("raw_path") or b"").decode("utf-8", "replace"),
                    "root_path": scope.get("root_path"),
                    "method": scope.get("method"),
                    "host": (headers.get(b"host", b"") or b"").decode(),
                }).encode()
                await send({
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"application/json")],
                })
                await send({"type": "http.response.body", "body": body})
                return
        await self.target(scope, receive, send)


app = _DiagApp(_api_app)