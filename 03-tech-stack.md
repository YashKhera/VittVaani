# 03 · Tech Stack

**Project:** VittVanni — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. Stack Summary

```
┌─────────────────────────────────────────────┐
│  FRONTEND  ·  static site, no build step    │
│                                             │
│  HTML5  ·  CSS3 (custom properties)         │
│  Vanilla JavaScript (ES6+ modules)          │
├─────────────────────────────────────────────┤
│  fetch ⇄ JSON  ·  CORS                      │
├─────────────────────────────────────────────┤
│  BACKEND  ·  Python 3.10+                   │
│                                             │
│  FastAPI · SQLAlchemy 2.x · Pydantic        │
│  JWT auth (python-jose + passlib/bcrypt)    │
├─────────────────────────────────────────────┤
│  DATABASE                                   │
│  SQLite (dev) ⇄ PostgreSQL (prod-ready)     │
└─────────────────────────────────────────────┘
```

| Layer       | Technology                       | Why                                                                 |
| ----------- | -------------------------------- | ------------------------------------------------------------------- |
| Frontend    | HTML5, CSS3, Vanilla JS (ES6+)   | Zero install, instant dev, hackathon-speed iteration, no toolchain  |
| Backend     | Python 3.10+, FastAPI            | Fast development, automatic OpenAPI docs, async-ready, type-safe    |
| ORM         | SQLAlchemy 2.x                   | Migrates cleanly from SQLite → PostgreSQL                           |
| Validation  | Pydantic v2 (`pydantic-settings`) | Request/response schemas + env config                               |
| Auth        | `python-jose` + `passlib[bcrypt]` | Standard JWT flow used across gov-tech projects                     |
| Database    | SQLite / PostgreSQL adapter      | `psycopg2-binary` for prod                                          |
| Frontend serve | Python `serve.py` (no cache)   | Deterministic local dev server                                      |
| AI/ML hooks | `anthropic`, `huggingface_hub`, `tokenizers` | Reserved for future AI assistant grounded on scheme data |

---

## 2. Frontend Stack

### 2.1 Languages & APIs
- **HTML5** — semantic pages with IDs for page controllers
- **CSS3** — design-token variables (`css/variables.css`), component modules
  (`global.css`, `layout.css`, `components.css`, `navigation.css`, `responsive.css`)
- **Vanilla JS (ES6+)** — modular, no frameworks

### 2.2 Module Map
| Module                 | Responsibility                                        |
| ---------------------- | ----------------------------------------------------- |
| `js/api.js`            | **Sole** backend communication layer (`fetch` wrapper) |
| `js/storage.js`        | `localStorage` helpers (tokens, prefs)                |
| `js/validation.js`     | Form validation                                       |
| `js/matching.js`       | Normalizes v1/v2 payloads + score helpers             |
| `js/theme.js`          | Dark/light theme manager                              |
| `js/i18n.js`           | EN ⇄ Hindi dictionary + switcher                      |
| `js/data/questions.js` | Questionnaire definition (`showIf` branching)         |
| `js/data/schemes.js`   | Mock dataset (Government Data Structure format)       |
| `js/components/*`      | `navbar`, `scheme-card`, `progress-bar` renderers     |
| `js/pages/*`           | One controller per HTML page                           |

### 2.3 Conventions
- Never call `fetch` outside `api.js`.
- Page controllers attach behavior after DOM load; static server injects no cache.
- No build step; served by `python serve.py --port 3000`.

---

## 3. Backend Stack

### 3.1 Core
- **Python 3.10+**
- **FastAPI 0.104** — routes, validation, auto `/docs` + `/redoc`
- **SQLAlchemy 2.0.52** — ORM models
- **Pydantic / pydantic-settings** — schemas + env-driven config (`app/config.py`)

### 3.2 Auth
- `python-jose[cryptography]==3.3.0` — JWT encode/decode
- `passlib[bcrypt]==1.7.4` — password hashing
- `email-validator` — email validation
- `python-multipart` — form parsing

### 3.3 DB / Data
- SQLite default; `psycopg2-binary==2.9.13` for PostgreSQL prod
- `python-dotenv` — `.env` loading (always relative to `backend/`)

### 3.4 Execution & Tools
- `uvicorn[standard]==0.24.0` — ASGI server
- `pytest==7.4.3` (tests) + stdlib `unittest`
- `anthropic`, `huggingface_hub`, `tokenizers`, `hf-xet` — reserved for AI service (`app/services/ai_service.py`)

---

## 4. Version Pins (requirements.txt)

The single source of truth is the **`requirements.txt`** in this folder and the
copied pin-set in `backend/requirements.txt`. Run with:

```bash
pip install -r requirements.txt
```

## 5. Database Strategy

| Environment | Engine      | URL shape                                    |
| ----------- | ----------- | -------------------------------------------- |
| Dev         | SQLite      | `sqlite:///vittvanni.db` (default)           |
| Production  | PostgreSQL  | `DATABASE_URL=postgresql://user:pass@host/db` |

SQLAlchemy models (`app/models/*`) are engine-agnostic; schemas and seed scripts
work on both. Migrations for v2 tables: `backend/migrate_v2.py`.

## 6. How Frontend ↔ Backend Talk

1. Frontend pages call methods on `API` (`js/api.js`).
2. `api.js` uses `BASE_URL` (default `http://127.0.0.1:8000/api`).
3. FastAPI serves JSON at `/api/*`; CORS allows the dev frontend origins.
4. `js/matching.js` normalizes v1 (flat) and v2 (nested) recommendations into one
   card shape for `js/components/scheme-card.js`.

## 7. Deviation Log

| Change                                  | Reason                                   |
| --------------------------------------- | ---------------------------------------- |
| No React/Vue                           | Keep hackathon stack zero-build & simple |
| Google OAuth router kept but unused     | README states JWT-only for v1            |
| AI libs pinned, ai_service reserved     | Future AI assistant, not in MVP scope    |