# 14 · Implementation Plan (SC Concessional Lending Mission)

**Project:** VittVaani — AI Scheme Analyzer for Marginalized Entrepreneurs & Students
**Event:** Smart India Hackathon 2026 · **Status:** Steps 1–5 ✅ done, Step 6 next (integration & impact polish)

---

## Step 1 — Catalog & rules  ✅ (done)

- Extended scheme model with channel-finance fields: `loan_category`
  (micro_finance | term_loan | education), `interest_rate_min/max`,
  `moratorium_min/max_months`, `max_coverage_pct`, `max_project_cost`,
  `tenure_min/max_months`, `income_ceiling` (₹5L default), `channel_financed`.
- Added the SC concessional loan catalog (NSTFDC-style: Micro Finance Scheme,
  Term Loan, Educational Loan, Mahila Samridhi, Adarsh Gram, …) to the seed
  data alongside existing schemes.
- Added hard eligibility rules: income ≤ ₹5L, category (SC/ST/OBC/minority/PwD),
  gender, state, and project-type.
- **Further changes made:**
  - Catalog grown to **90+ schemes** (central + state + 21 dedicated education
    loan/scholarship schemes incl. Vidya Lakshmi, CSIS, Dr. Ambedkar CSS,
    Post-Matric SC, Ishan Uday, NHFDC, and state-specific schemes for
    Maharashtra, Delhi, UP, Bihar, West Bengal, NE states).
  - `education` added to the sectors/taxonomy used by AI understanding and
    matching (Step 1 original scope, now complete).

## Step 2 — Recommender tuning  ✅ (done)

- Income-ceiling rule + project-cost-based tiering in `matching_service`:
  small ≤ ₹1.4L → Micro Finance; large ≤ ₹50L → Term Loan;
  education → Education Loan.
- AI understanding gains `project_type` (business vs education).
- **Further changes made:**
  - **State hard filter:** state-specific schemes only surface for users in
    those states (blocking otherwise).
  - **Project-type hard filter:** education users see only education schemes;
    business users are blocked from education-only schemes.
  - Sector/stage matching now education-aware (full score for
    `education` sector / `planning` stage for students).
  - Verified end-to-end + tests green.

## Step 3 — Financial Calculator  (/api/calculator)  ✅ done

- Backend service: EMI = P·r·(1+r)^n / [(1+r)^n − 1] with moratorium handling
  (interest accrues during moratorium; EMI starts after) + coverage/subsidy
  adjustments; amortization summary + total interest.
- Endpoints: `GET /api/calculator/defaults`, `POST /api/calculator`,
  `GET /api/calculator/schemes` (scheme defaults), `POST /api/calculator/schemes`
  (compare up to 5 schemes by EMI) — all auth-gated.
- Frontend `calculator.html` (**multilingual** — 23 Indian languages, keys
  added EN/HI with English fallback for regional packs) with sliders for
  cost/rate/tenure/coverage/moratorium/subsidy, EMI + amortization results,
  and "Compare schemes" picker.
- Per-scheme CTA "Calculate EMI" added to scheme cards and scheme-details page
  (deep-links with `?scheme=<id>&autocalc=1`).
- 29 parametrized unit tests; full suite 181 passed (incl. 2 previously stale
  matching/education tests realigned to deployed hard filters).
- **Further changes made:** Step 3 now complete — calculator deployed to
  production.

## Step 4 — Channel Partner directory  ✅ done

- New ChannelPartner model (`app/models/channel_partner.py`) + seed
  (`data/partners_seed.py`, **120 partners** across all 29 states: SCA, PSB,
  RRB, NBFC-MFI with lat/long, loan categories served, fund utilization %,
  NPA %, overdue %).
- APIs (`/api/partners`, all auth-gated):
  - `GET /api/partners` — search/filter (name/city/district, state, city,
    pincode, partner_type, loan_category, min_health) with pagination.
  - `GET /api/partners/nearest` — haversine nearest within `max_distance_km`,
    ranked by distance then health, optionally filtered by loan_category/type.
  - `GET /api/partners/eligible` — channel-health eligibility filter
    (min_utilization, max_npa, max_overdue, loan_category, state, city, type).
  - `GET /api/partners/{id}` — detail.
- Partners seeded on Vercel cold-start alongside schemes (`api/index.py`).
- 18 end-to-end tests; full suite 199 passed + 1 expected failure.

## Step 5 — Geo-spatial Locator & Router UI  ✅ done

- Leaflet + OpenStreetMap (no API key), pincode/city lookup + browser
  geolocation.
- On a scheme → show nearest eligible partners, ranked by distance and health
  (utilization, NPA, overdues), with directions link + contact.
- Implemented: `partners.html?scheme=<id>&loan_category=<cat>` deep-link with
  scheme banner + auto-run (`/eligible` fallback when no location);
  pincode → Nominatim geocode → `/nearest` with directory-filter fallback;
  browser geolocate → `/nearest`; "Find partners" CTAs on scheme cards +
  scheme-details; EN/HI i18n; frontend copy synced to `backend/frontend/`.

## Step 6 — Integration & impact polish

- Results page chain: Scheme → EMI → nearest eligible partner.
- Financial-literacy content (what is concessional lending, channel finance
  explained) — **multilingual** (EN/HI + regional packs).
- Router warns on high-NPA partners; full mobile responsiveness; i18n keys
  completed for all 23 languages.

## Step 7 — Hardening & demo readiness

- Tests for calculator, geo search, router logic; seed integrity checks;
  privacy pass; demo runbook; README/docs updated.
- **Further changes made:** production deploy pipeline on **Vercel** (static
  frontend + FastAPI backend) with **Neon Postgres** (branching); README
  revamped with deployment guide and env vars.

---

## Status Summary

| Step | Title                         | Status     |
| ---- | ----------------------------- | ---------- |
| 1    | Catalog & rules               | ✅ Done    |
| 2    | Recommender tuning            | ✅ Done    |
| 3    | Financial Calculator          | ✅ Done    |
| 4    | Channel Partner directory     | ✅ Done    |
| 5    | Geo-spatial Locator & Router  | ✅ Done    |
| 6    | Integration & impact polish   | ⬜ Pending |
| 7    | Hardening & demo readiness    | ⬜ Pending |