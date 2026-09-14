# 09 · Testing Strategy

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. Scope

Backend unit tests live in `backend/tests/`. Frontend has no formal test harness
yet — visual/manual testing plus live API integration.

## 2. Backend Tests

### Files

| File                         | What it tests                                          |
| ---------------------------- | ------------------------------------------------------ |
| `tests/__init__.py`          | package init                                           |
| `tests/test_constants.py`    | Canonical constant values shared across the stack      |
| `tests/test_eligibility_engine.py` | `EligibilityEngine`, `RelevanceScorer`, `MatchingEngineV2` |
| `tests/test_serializers.py`  | Government Data Structure serializer output correctness |

### Run
```bash
cd backend
python -m unittest discover tests -v
```

## 3. What Is Tested

- Eligibility hard-rule filter correctly rejects ineligible profiles.
- Relevance scoring produces expected breakdown values and ordering.
- Serializer produces the correct Government Data Structure shape for known inputs.
- Constants are stable across schema and UI.

## 4. What Is NOT Covered (Gaps)

| Gap                               | Mitigation                           |
| --------------------------------- | ------------------------------------ |
| API integration / end-to-end      | manual Swagger testing               |
| Frontend rendering                 | visual QA + demo                     |
| Auth flow (register/login/JWT)    | manual QA via Swagger                |
| Scheme seed data integrity        | run `migrate_v2.py` then check counts|

## 5. Future Testing Roadmap

- Add `pytest` + `httpx` `TestClient` tests for auth and profile routers.
- Add schema-count invariant test post-seed (`assert count schemes_v2 ≥ 70`).
- Add `pytest-cov` and target ≥ 80% branch coverage on `eligibility_engine`.
- Add frontend E2E tests (Playwright) for questionnaire → results happy path.

## 6. Demo Validation Checklist

Use this before any live demo:
1. Backend starts cleanly (`python run.py`, no errors on startup log).
2. `GET /health` returns `"status": "ok"`.
3. `python migrate_v2.py` reports 73 seeded schemes.
4. All unit tests pass.
5. Frontend loads at `http://localhost:3000` without JS errors.
6. Complete login → profile → questionnaire → results flow in EN and Hindi.
7. Save a scheme → check it appears in `saved-schemes.html`.