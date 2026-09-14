# VittVaani — Scheme Analyzer for Marginalized Entrepreneurs

> AI-powered government scheme analyzer for **marginalized Indian entrepreneurs**.
> Smart India Hackathon 2026 · Team VittVaani

Arth Setu ("wealth bridge" in Hindi) is the flagship product of **VittVaani** — it
helps women, SC/ST/OBC, persons with disabilities and rural micro-entrepreneurs
discover the **government schemes they are actually eligible for** — not just a
generic list. Tell us about your business once, and get ranked,
eligibility-scored recommendations with clear reasons, in your own language.

---

## ✨ Highlights

- **AI business understanding** — describe your business in plain words; the AI
  derives sector + tags so the matching engine uses real business context.
  Powered by Gemini with a built-in rule-based fallback so the app works even
  with **no API key**.
- **Eligibility matching engine** — hard eligibility-rule filter followed by
  weighted relevance scoring → ranked results with a score breakdown per scheme.
- **Explanations that matter** — top matches get a short plain-language AI
  "why it fits you" summary (generated concurrently to keep latency low).
- **Adaptive questionnaire** — a short branching flow (9 questions) that skips
  irrelevant follow-ups.
- **Bilingual UI** — English ↔ Hindi toggle, persisted per user.
- **Dark mode** — OS-preference aware and persisted.
- **Saved schemes** — bookmark and revisit schemes anytime.

## 🧱 Tech Stack

| Layer      | Technology |
| ---------- | ---------- |
| Frontend   | HTML5 · CSS3 · Vanilla JavaScript (ES6+), no build step |
| Backend    | Python 3.10+ · FastAPI · Uvicorn |
| Database   | SQLite (dev) · PostgreSQL (production-ready via `DATABASE_URL`) |
| ORM        | SQLAlchemy 2.x |
| Auth       | JWT (`python-jose` + `bcrypt`), OTP via SMTP for password reset |
| AI         | Google Gemini (Interactions/Gemini models) + built-in rule fallback |
| API Docs   | Swagger UI at `/docs`, ReDoc at `/redoc` |

## 📁 Repository Layout

```
Arth Setu/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── routers/          # auth, profile, questionnaire, schemes,
│   │   │                     # recommendations, saved, preferences, ai-understanding
│   │   ├── services/         # matching, understanding (Gemini + fallback), email, auth
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── config.py         # settings (reads backend/.env)
│   │   └── main.py           # FastAPI app + CORS
│   ├── data/schemes_seed.py  # curated scheme catalog (central + state)
│   ├── tests/                # pytest suite
│   ├── requirements.txt
│   └── run.py                # dev server → http://127.0.0.1:8001
├── frontend/                 # static site, no build step
│   ├── index.html            # landing
│   ├── profile.html          # business profile
│   ├── questionnaire.html    # adaptive questionnaire
│   ├── results.html          # ranked recommendations
│   ├── scheme-details.html   # scheme detail page
│   ├── saved-schemes.html    # bookmarks
│   ├── oauth/callback.html   # (optional) auth callback
│   ├── css/  js/  assets/
│   └── serve.py              # static server → http://127.0.0.1:8080
├── 01-PRD.md  …  13-contributing.md   # design docs (see below)
└── README.md
```

## 🚀 Quick Start

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure environment (secrets are NEVER committed)
copy .env.example .env            # Windows
# fill in GEMINI_API_KEY (optional — app falls back to builtin matching)

# Seed the scheme catalog
python -m data.schemes_seed

# Run the API on http://127.0.0.1:8001 (docs at /docs)
python run.py
```

### 2. Frontend

```bash
cd frontend
python serve.py            # → http://127.0.0.1:8080
```

Open `http://127.0.0.1:8080`, register, complete your profile, confirm the AI's
understanding of your business, and view your matched schemes.

## 🔌 API Overview

Base: `http://127.0.0.1:8001/api` · Interactive docs: `/docs`

| Method | Endpoint                        | Description |
| ------ | ------------------------------- | ----------- |
| POST   | `/auth/register`                | Create account |
| POST   | `/auth/login`                   | JWT login |
| POST   | `/auth/forgot-password`         | Send password reset OTP |
| POST   | `/auth/reset-password`          | Reset password with OTP |
| GET    | `/profile`                      | Current profile |
| POST   | `/profile`                      | Create profile |
| PUT    | `/profile`                      | Update profile |
| GET/PUT| `/questionnaire/progress`       | Save/resume questionnaire answers |
| GET    | `/schemes`  `/schemes/{id}`     | Scheme catalog |
| GET    | `/ai/understanding`             | Current AI understanding |
| POST   | `/ai/understand`                | AI infers sector/tags from business description |
| POST   | `/ai/confirm`                   | Accept the AI understanding (unlocks recommendations) |
| POST   | `/recommendations`              | Ranked, personalized schemes (+ top-5 AI explanations) |
| POST/DELETE | `/saved-schemes/{id}`      | Bookmark / remove |
| GET    | `/saved-schemes`                | List saved schemes |
| GET    | `/preferences`  (PUT)           | UI language/theme preferences |

## 🧪 Tests

```bash
cd backend
..\.venv\Scripts\python.exe -m pytest tests -q
```

The suite is **hermetic** — no live AI/network required; AI calls are forced to
the built-in fallback, so tests run offline and fast.

## ⚠️ Security

Secrets are never committed:

- `backend/.env` is git-ignored — create it from `.env.example`.
- `backend/*.db` (SQLite files) are git-ignored.
- Frontend is intentionally static and public.

For production hardening see [`10-security.md`](./10-security.md).

## 📚 Documentation

| # | Doc | Covers |
| - | --- | ------ |
| 01 | [`01-PRD.md`](./01-PRD.md) | Product requirements, personas, success metrics |
| 02 | [`02-RD.md`](./02-RD.md) | Functional & non-functional requirements |
| 03 | [`03-tech-stack.md`](./03-tech-stack.md) | Stack rationale & versions |
| 04 | [`04-architecture.md`](./04-architecture.md) | Architecture, matching pipeline, data flow |
| 05 | [`05-api-contract.md`](./05-api-contract.md) | REST contract & error shapes |
| 06 | [`06-database-schema.md`](./06-database-schema.md) | Tables & relationships |
| 07 | [`07-user-stories.md`](./07-user-stories.md) | Stories & acceptance criteria |
| 08 | [`08-design-system.md`](./08-design-system.md) | UI/UX, components, i18n, theming |
| 09 | [`09-testing.md`](./09-testing.md) | Test strategy & commands |
| 10 | [`10-security.md`](./10-security.md) | Auth, secrets, data handling |
| 11 | [`11-deployment.md`](./11-deployment.md) | Deploy & runbooks |
| 12 | [`12-roadmap.md`](./12-roadmap.md) | Milestones & backlog |
| 13 | [`13-contributing.md`](./13-contributing.md) | Workflow & conventions |

## 👥 Team

VittVaani — Smart India Hackathon 2026.