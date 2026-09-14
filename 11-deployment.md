# 11 · Deployment & Setup Runbook

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. Prerequisites

- Python 3.10+ (backend + dev servers)
- Any static-capable host for the frontend (or `python serve.py`)
- Git

## 2. Backend Setup (dev)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows (activate on macOS/Linux)
pip install -r requirements.txt

# Optional env config (sensible defaults exist)
copy .env.example .env          # Windows
```

`.env` is loaded relative to `backend/`, so the server runs from anywhere.

### Start backend
```bash
python run.py
# or
uvicorn app.main:app --reload
```
URLs: API root `http://localhost:8000` · docs `/docs` · health `/health`

## 3. Database Initialization

```bash
cd backend
python migrate_v2.py                 # create tables + seed v2 catalog
python data/schemes_seed_v2.py --force   # refresh 73 schemes (destructive to schemes only)
```

Invariant post-seed: `SELECT COUNT(*) FROM schemes_v2` ≥ 70 and no
duplicate bad rows. Users/profiles/saved survive a `--force` re-seed.

## 4. Frontend Setup (dev)

```bash
cd frontend
python serve.py --port 3000     # no-cache static dev server
# → http://localhost:3000
```

No build step. `js/api.js` `BASE_URL` points at `http://127.0.0.1:8000/api`.

## 5. Tests

```bash
cd backend
python -m unittest discover tests -v
```

## 6. Production (target topology)

```
Browser ──► Nginx / static CDN  ── /        ──► frontend/ (static)
                              └── /api/*, /docs ──► uvicorn (FastAPI) :8000
                                                        │
                                                        ▼
                                                  PostgreSQL
```

Steps:
1. Backend: set `ENVIRONMENT=production`, strong `SECRET_KEY`, `DATABASE_URL`
   (PostgreSQL). Run once: `python migrate_v2.py`.
2. Start with a process manager (systemd / supervisor / pm2):
   `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2`.
3. Frontend: `git checkout` `frontend/` into the web root (or upload to static
   host), set `api.js` `BASE_URL` to the production `/api` origin.
4. Configure HTTPS + real CORS origin in `main.py`.

## 7. Common Commands Cheat-Sheet

| Task                              | Command                                              |
| --------------------------------- | ---------------------------------------------------- |
| Start backend (dev)               | `python run.py`                                      |
| Start frontend (dev)              | `python serve.py --port 3000` (from `frontend/`)     |
| Create DB tables + seed           | `python migrate_v2.py`                               |
| Force-refresh scheme catalog      | `python data/schemes_seed_v2.py --force`             |
| Run backend tests                 | `python -m unittest discover tests -v`               |
| Install deps                      | `pip install -r requirements.txt`                    |
| View API docs                     | open `http://localhost:8000/docs`                    |

## 8. Troubleshooting

| Symptom                                  | Fix                                            |
| ---------------------------------------- | ---------------------------------------------- |
| Frontend can't reach API                 | Check CORS allowlist; confirm backend on :8000  |
| `ImportError` on start                   | `pip install -r requirements.txt` in venv      |
| Missing scheme tables                    | `python migrate_v2.py`                          |
| Stale frontend assets                    | Use `serve.py` (no-cache) or hard refresh       |
| Port 8000 in use                         | Change config or kill the old process           |