"""Vercel serverless entrypoint for the VittVaani FastAPI backend.

Single rewrite (`/(.*)` -> `/api`) sends every request here. Vercel invokes the
function with its mount prefix (`/api`) prepended to the original path, so this
wrapper strips that prefix once and hands the original path to FastAPI, which
serves BOTH the `/api/*` routers and the static `frontend/` (mounted at `/`).

Production uses PostgreSQL (Neon): `app.main` creates tables on import; the
scheme catalog is seeded (idempotently) on the first cold start. Local runs are
untouched (guarded by the `VERCEL` env var).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from fastapi.staticfiles import StaticFiles  # noqa: E402

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


def _serve_static_frontend():
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
    if not os.path.isdir(frontend_dir):
        print("Static frontend not found at:", frontend_dir)
        return
    # Drop the plain "/" JSON route so the website index wins at "/".
    _api_app.routes[:] = [
        r for r in _api_app.routes
        if not (getattr(r, "path", None) == "/" and r.__class__.__name__ == "APIRoute")
    ]
    _api_app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")


_bootstrap_production_db()
_serve_static_frontend()


class _NormalizedPathApp:
    """Removes the single `/api` mount prefix Vercel prepends to the path."""

    def __init__(self, target):
        self.target = target
        self.strip_on_vercel = bool(os.environ.get("VERCEL"))

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and self.strip_on_vercel:
            path = scope.get("path") or "/"
            if path.startswith("/api"):
                path = path[4:] or "/"
            scope["path"] = path
        await self.target(scope, receive, send)


app = _NormalizedPathApp(_api_app)