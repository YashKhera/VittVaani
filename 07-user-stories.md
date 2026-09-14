# 07 · User Stories

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs

Each story follows the format `As a <role>, I want <capability>, so that <value>`.
Acceptance criteria are concrete and testable.

---

## Personas

- **Priya R.** — 38, woman-owned tailoring unit, OBC, rural Maharashtra.
  Comfortable with Hindi, basic phone skills.
- **Ravi M.** — 34, differently-abled handicraft maker, urban Gujarat, 2-year-old business.
- **Anita S.** — 29, urban digital-first founder, uses English, wants candidates fast.
- **Kiran** — NGO field officer helping 20+ entrepreneurs apply for schemes.

---

## Stories

### US-01 · Register an account
> As a new user, I want to register with my email and password, so that my profile
> and results are saved across sessions.

**Acceptance criteria:**
- [ ] Register form validates email format and password strength.
- [ ] On success, I am logged in and can access protected pages.
- [ ] Duplicate email returns a clear error.

### US-02 · Log in
> As a returning user, I want to log in, so that I can continue my saved work.

**AC:**
- [ ] Login returns a JWT stored by the frontend.
- [ ] Protected API calls include the token automatically (`js/api.js`).

### US-03 · Reset a forgotten password
> As a user who forgot my password, I want to request a reset, so that I can regain access.

**AC:**
- [ ] `forgot-password` issues a short-lived reset token (link logged in dev).
- [ ] Landing on `reset-password.html?token=...` lets me set a new password.
- [ ] Old password no longer works; new password does.

### US-04 · Create my business profile
> As an entrepreneur, I want to enter my business details once, so that matching
> uses my real context.

**AC:**
- [ ] Fields: business type, sector, location/state, enterprise category, turnover band, funding need.
- [ ] `POST /api/profile` persists the profile and it appears in `GET /api/profile`.

### US-05 · Complete the guided questionnaire
> As a user, I want to answer a short adaptive questionnaire, so that I get
> personalized schemes without filling long forms.

**AC:**
- [ ] 9 questions render step by step with a progress bar.
- [ ] Branching questions (e.g., `food_processing` asks a follow-up) appear only when relevant.
- [ ] Answers sync into my profile.

### US-06 · Get ranked, eligibility-scored schemes
> As a user, I want to see schemes ranked by my eligibility, so that I can focus
> on my best options.

**AC:**
- [ ] Results exclude schemes whose mandatory rules I fail.
- [ ] Results are sorted by relevance score.
- [ ] Each card shows a score breakdown and plain-language match reasons.

### US-07 · Understand why a scheme matched
> As a user, I want to see why a scheme is recommended, so that I trust the result.

**AC:**
- [ ] Score breakdown reflects sector > purpose > stage > location > type > size weights.
- [ ] Reasons are human-readable (not raw field names).

### US-08 · View full scheme details
> As a user, I want a full scheme detail page, so that I can read benefits,
> documents required, and how to apply.

**AC:**
- [ ] Detail page renders the Government Data Structure payload.
- [ ] Official application URL is prominent.

### US-09 · Save schemes for later
> As a user, I want to bookmark schemes, so that I can apply to them later.

**AC:**
- [ ] Save/remove toggles everywhere a scheme card appears.
- [ ] `GET /api/saved-schemes` lists my bookmarks persistently.

### US-10 · View my profile completeness
> As a user, I want a completeness meter, so that I know what profile data to improve.

**AC:**
- [ ] `profile-view.html` shows a completeness percentage.
- [ ] Missing fields are listed.

### US-11 · Use the app in Hindi
> As a Hindi-first user (Priya), I want to switch the whole UI to Hindi, so that
> I can use the app comfortably.

**AC:**
- [ ] Navbar pill toggles EN ⇄ Hindi.
- [ ] All `data-i18n` strings update instantly; choice persists.

### US-12 · Use the app in dark mode
> As a user working at night, I want dark mode, so that the app is comfortable to read.

**AC:**
- [ ] Toggle persists per user.
- [ ] Default respects OS preference.

### US-13 · View saved schemes (NGO officer)
> As a field officer, I want a simple saved-schemes list, so that I can help
> multiple entrepreneurs shortlist schemes.

**AC:**
- [ ] List is shareable via plain links (no auth-blocked assets).

### US-14 · Browse catalog offline/demo
> As a demo judge, I want to see core flows even without a backend, so that the
> demo never hangs.

**AC:**
- [ ] Mock data in `js/data/schemes.js` renders cards when API is unavailable.

---

## Story → Component Mapping

| Story | Frontend files | Backend endpoint(s) |
| ----- | -------------- | ------------------- |
| US-01/02/03 | `pages/auth.js`, `register.html`, `login.html`, `reset-password.html` | `/api/auth/*` |
| US-04 | `pages/profile.js`, `profile.html` | `/api/profile` POST/GET/PUT |
| US-05 | `pages/questionnaire.js`, `data/questions.js` | `/api/profile` (sync) |
| US-06/07 | `pages/results.js`, `matching.js`, `components/scheme-card.js` | `/api/recommendations`, `/api/v2/recommendations` |
| US-08 | `pages/scheme-details.js` | `/api/schemes/{id}`, `/api/v2/recommendations/schemes/{id}` |
| US-09 | `pages/saved.js`, `pages/results.js` | `/api/saved-schemes*` |
| US-10 | `pages/profile-view.js` | `/api/profile` |
| US-11/12 | `i18n.js`, `theme.js`, all pages | — (client-side) |
| US-14 | `data/schemes.js` | — (mock) |