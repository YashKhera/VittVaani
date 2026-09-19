"""Vercel serverless entrypoint for the VittVaani FastAPI backend.

Vercel invokes the module-level ``app`` ASGI application for the routes declared
in ``vercel.json`` (``/api/*``, ``/docs``, ``/health``). Static assets in
``frontend/`` are served directly by Vercel and never touch this function.

Notes:
- Vercel strips the function's ``/api`` mount prefix from the ASGI path, while
  the FastAPI routers are registered under ``/api``. This wrapper re-adds the
  prefix so routes match regardless of whether Vercel strips it or not.
- Production uses PostgreSQL (Neon). Tables are created by ``app.main`` on
  import; the scheme catalog is seeded here (idempotent) on the first cold
  start. Local runs are untouched (guarded by the ``VERCEL`` env var).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from app.main import app as _api_app  # noqa: E402  (import also runs create_all)
from data.schemes_seed import seed_schemes  # noqa: E402

# Paths FastAPI exposes at the app root (no "/api" prefix in the routers).
_DOC_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json"}


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


class _NormalizedPathApp:
    def __init__(self, target):
        self.target = target

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path") or ""
            if not path.startswith("/api") and path not in _DOC_PATHS:
                scope["path"] = "/api" + path
        await self.target(scope, receive, send)


app = _NormalizedPathApp(_api_app)