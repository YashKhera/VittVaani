# 12 · Roadmap

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs
Reference PRD: [`01-PRD.md`](./01-PRD.md) · Milestones M0–M5

---

## 1. Milestones

| # | Milestone       | Scope                                                            | Definition of Done                          |
| - | --------------- | ---------------------------------------------------------------- | -------------------------------------------- |
| M0| Foundation      | Backend scaffold, config, DB, auth, serve scripts                 | Register/login works; `/health` ok           |
| M1| Catalog         | scheme + scheme_v2 models, seed 73 schemes, list/detail APIs       | 73 schemes in DB; Swagger shows endpoints    |
| M2| Profiling       | Profile CRUD router + questionnaire sync                          | Profile persists; answers sync               |
| M3| Matching        | Eligibility engine + ranked recommendations v1 + v2               | Ranked results with score breakdown          |
| M4| UX polish       | i18n EN/Hindi, dark mode, saved schemes, responsive CSS            | All stories US-11..US-14 pass                |
| M5| Hardening       | Tests, security pass, docs, demo runbook                           | 100% of unit tests green; demo checklist done |

Status: M0–M4 **implemented** (per codebase); M5 in progress (this docs kit).

## 2. Backlog

### P0 — next
- [ ] pytest + httpx integration tests for auth/profile routers
- [ ] Seeded data invariants test (≥ 70 schemes, no dupes)
- [ ] CORS production allowlist + HTTPS notes
- [ ] Rate limiting on `/auth/login` & `/auth/forgot-password`

### P1 — should
- [ ] Alembic migrations replacing manual scripts
- [ ] Email delivery for password-reset links (SMTP)
- [ ] Frontend E2E test harness (Playwright) happy path
- [ ] Scheme deadline / application-closed flags + UI badge

### P2 — could
- [ ] AI assistant (chat) grounded on scheme catalog (`ai_service.py` reserved)
- [ ] More Indian languages (Tamil, Bengali, Marathi, ...)
- [ ] PWA offline mode
- [ ] Export/share recommendations as PDF/print view

## 3. Data Maintenance

- re-curate scheme pages monthly (update `last_verified`).
- New schemes: add to `data/schemes_seed_v2.py` with `_scheme()` helper + rules.
- Run `python data/schemes_seed_v2.py --force` after reviewing git diff.

## 4. Future Scope (post-hackathon)

- Government application-portal handoff (application submission).
- KYC/document upload with verification.
- NGO / field-officer multi-profile workspaces.
- Analytics dashboard for scheme-uptake insights.