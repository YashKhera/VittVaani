# 04 · Architecture

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. High-Level Architecture

```
┌──────────────┐   HTTP/JSON (CORS)   ┌───────────────────────────┐
│   BROWSER    │ ───────────────────► │        FASTAPI APP        │
│  static SPA  │                      │  app/main.py              │
│  serve.py    │ ◄─────────────────── │  routers/ · api/ · schemas│
│  3000        │                      │  services/ · models      │
└──────────────┘                      └────────────┬──────────────┘
                                                    │ SQLAlchemy ORM
                                                    ▼
                                     ┌────────────────────────────┐
                                     │  SQLite (dev) / PostgreSQL  │
                                     │  vittvaani.db              │
                                     └────────────────────────────┘
```

Two independent folders, two teams, one contract.

## 2. Backend Layering

```
routes  (FastAPI routers)   →  parse request, auth, return response
   │
services (business logic)   →  eligibility_engine, matching_service,
   │                            profile_service, auth_service, ai_service
   │
schemas (Pydantic)          →  request/response contracts
   │
models (SQLAlchemy)         →  table definitions
   │
utils                       →  constants, serializers, security, helpers
```

### Key files
| File | Role |
| ---- | ---- |
| `app/main.py` | FastAPI app factory, CORS, router registration, lifecycle |
| `app/config.py` | `pydantic-settings` env config (`APP_NAME`, `DATABASE_URL`, JWT) |
| `app/database.py` | Engine + session factory |
| `app/dependencies/auth.py` | JWT dependency for protected routes |
| `app/services/eligibility_engine.py` | `EligibilityEngine`, `RelevanceScorer`, `MatchingEngineV2` |
| `app/services/matching_service.py` | Matching orchestration service |
| `app/utils/serializers.py` | Gov Data Structure serializers |
| `app/utils/constants.py` | Canonical constant values shared across the stack |

## 3. Matching Pipeline (Core Flow)

```
Entrepreneur Profile + Questionnaire answers
              │
              ▼
  1. Mandatory Eligibility Filter  (hard rules)
     eligibility_rules: {field, operator, value, required}
              │   scheme removed if a `required` rule fails
              ▼
  2. Relevance Scoring (weighted)
     sector > purpose > stage > location > entrepreneur_type > business_size
              │
              ▼
  3. Ranking — sort desc by score, slice top-N
              │
              ▼
  4. Serialize → Government Data Structure + score breakdown + match reasons
              │
              ▼
  POST /api/recommendations  ·  POST /api/v2/recommendations
```

The engine lives in `backend/app/services/eligibility_engine.py`; it is unit-
tested in `backend/tests/test_eligibility_engine.py`.

## 4. Frontend Architecture

```
index.html ──► pages/home.js
register.html ─► pages/auth.js        ┬
login.html ──► pages/auth.js          │ page controllers
profile.html ─► pages/profile.js      │
profile-view.html ─► pages/profile-view.js
questionnaire.html ─► pages/questionnaire.js ─► data/questions.js (showIf)
results.html ─► pages/results.js ─► matching.js ─► components/scheme-card.js
scheme-details.html ─► pages/scheme-details.js
saved-schemes.html ─► pages/saved.js

Shared: api.js · storage.js · validation.js · theme.js · i18n.js
        components/navbar.js · components/progress-bar.js
        data/schemes.js (mock, offline/demo)
```

### Data normalization
`js/matching.js` `normalizeRecommendation()` maps v1-flat and v2-nested payloads
into a single card shape so page code never branches on API version.

## 5. Data Flow — Recommendation Request

```
results.js
  │  API.getRecommendations(profileAnswers)
  ▼
api.js (fetch POST /api/recommendations)
  ▼
recommendations router → matching_service → EligibilityEngine (rules)
                                     + RelevanceScorer (weights)
                                     + serializer
  ▼
JSON with { scheme, score, breakdown, reasons }
  ▼
matching.js normalize → scheme-card.js render
```

## 6. Auth Flow

```
login.html → API.login → POST /api/auth/login
  → { access_token, token_type: bearer }  → storage.js (localStorage)
  → subsequent API calls add Authorization: Bearer <token>
  → protected routers use dependencies.auth (get_current_user)
```

## 7. Data Lifecycle — Scheme Seed

```
backend/data/schemes_seed_v2.py
   │  _scheme() helper, curated content
   ▼
migrate_v2.py creates tables if missing → seed inserts 73 schemes
   │
   └── --force rebuilds schemes_v2 rows only (users intact)
```

## 8. Deployment Topology (Target)

```
NGINX/static host  ──  /            ──► frontend static files
                   └── /api/*, /docs─► uvicorn (FastAPI) on :8000
                                          │
                                          ▼
                                    PostgreSQL (prod)
```

Dev: `python run.py` (backend :8000) + `python serve.py --port 3000` (frontend).