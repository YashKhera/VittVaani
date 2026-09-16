# 13 · Contributing & Workflow

**Project:** VittVaani — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. Team Split

The repository is split into two independent folders so backend and frontend
teams work in isolation:

```
VittVaani/
├── backend/    # FastAPI + SQLAlchemy + SQLite (backend team)
├── frontend/   # static HTML/CSS/JS (frontend team)
└── docs/       # THIS documentation kit (shared)
```

The **API contract** ([`05-api-contract.md`](./05-api-contract.md)) is the shared
interface both teams build against.

## 2. Rules of Engagement

1. **Backend team stays in `backend/`**; **frontend team stays in `frontend/`.**
2. **Keep the API contract stable.** Frontend consumes shapes through
   `js/api.js`. Change endpoints in one place, not per page.
3. **Normalize in one place.** If a payload shape changes, update
   `Matching.normalizeRecommendation` (`js/matching.js`).
4. **Never call `fetch` directly in pages** — always via `API` (`js/api.js`).
5. **Centralize constants.** Align new scheme attributes with
   `backend/app/utils/constants.py`.
6. **Document changes** — update the matching docs here when contracts change.

## 3. Git Workflow

- Branch per milestone/feature: `feature/eligibility-engine-v2`,
  `feature/i18n-hindi`, etc.
- Small, reviewable commits with descriptive messages.
- Merge to `main` only when unit tests pass.
- Tag releases (`v0.1.0` per milestone).

## 4. Definition of Done

A feature is Done when all apply:
- [ ] Code implemented in the correct folder
- [ ] Unit/integration tests added & passing (`python -m unittest discover tests -v`)
- [ ] API contract doc updated if endpoints changed
- [ ] UI strings in `i18n.js` if user-facing text added
- [ ] Works in both themes and both languages (if user-facing)
- [ ] Demo checklist (see [`09-testing.md`](./09-testing.md)) still passes

## 5. Daily Flow

```bash
git pull
git checkout -b feature/<name>
# ...implement...
python -m unittest discover tests -v   # backend
python serve.py --port 3000             # frontend manual QA
git add -A && git commit -m "feat: ..."
git push -u origin feature/<name>
# open PR → review → merge
```

## 6. Documentation Maintenance

When you change behavior:
- Contract → update `05-api-contract.md`
- Schema → update `06-database-schema.md`
- Requirements → update `02-RD.md`
- Product vision → update `01-PRD.md`
- Otherwise → update `README.md` index