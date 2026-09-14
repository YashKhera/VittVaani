# 10 · Security

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs

---

## 1. Authentication

- **Password storage:** bcrypt hashing via `passlib[bcrypt]` — plaintext never stored.
- **JWT sessions:** `python-jose[cryptography]` issues an access token.
  Default expiry 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`, configurable).
- **Token type:** `Authorization: Bearer <access_token>` on protected routes,
  enforced by `app/dependencies/auth.py`.
- **Password reset:** `forgot-password` issues a short-lived token with
  `typ=reset` claim; `reset-password` exchanges it for a new password hash.
  Dev logs the reset link (no email transport yet).

## 2. Secrets Management

| Secret                        | Handling                                            |
| ----------------------------- | --------------------------------------------------- |
| `SECRET_KEY` (JWT signing)    | env var via `app/config.py` (`pydantic-settings`)   |
| `DATABASE_URL`                | env var; dev default is local `vittvaani.db`        |
| `.env`                        | gitignored; commit `.env.example` only              |

**Rules:**
- Never hardcode secrets or log them.
- Never commit `.env`, `vittvaani.db`, or generated tokens.
- Rotate `SECRET_KEY` between environments.

## 3. API Security

- CORS restricted to known dev origins (`main.py`), frontend URL from settings.
- Pydantic input validation on every request (type + constraint checks).
- Errors are message-only `{"detail": ...}`; no stack traces leaked.

## 4. Data Protection

- `entrepreneur_profiles` carries personal data → treat as PII.
- Saved schemes are scoped to the owning `user_id`; list endpoints filter by user.
- Timestamps maintained (`created_at`/`updated_at`) for audit.
- Scheme data keeps `source_url` + `last_verified` for provenance.

## 5. Threat Checklist

| Concern                | Status                                                        |
| ---------------------- | ------------------------------------------------------------- |
| Password reuse/leak    | Mitigated by hashing + email validation                       |
| Token theft            | Short expiry; HTTPS in prod                                   |
| Injection (SQL)        | Mitigated by SQLAlchemy ORM + parameterized queries           |
| XSS                    | No `innerHTML` from untrusted data on core flows; keep escaping |
| CSRF                   | JWT in header (not cookie) reduces risk; review session flow   |
| Data poisoning (seed)  | Curated seed + source URLs; refresh is controlled             |

## 6. Before Production

- Enforce HTTPS everywhere.
- Replace dev CORS allowlist with the real domain.
- Configure strong `SECRET_KEY` and `DATABASE_URL` (PostgreSQL).
- Add rate-limit for `login` / `forgot-password`.
- Add Alembic migrations; never deploy auto-migrate seed scripts.
- Audit dependency versions (`pip-audit` / Dependabot).
- Add server-side rate limiting and logging to a secure sink.

## 7. Incident Reporting

Document any found vulnerability in the repo issue tracker; fix + re-test before
public deployment.