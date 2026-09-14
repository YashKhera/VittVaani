# 06 · Database Schema

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs
**Engine:** SQLite (dev, `vittvaani.db`) ⇄ PostgreSQL (prod)

ORM models live in `backend/app/models/*`.

---

## 1. Tables

| Table                  | Model file        | Purpose                                   |
| ---------------------- | ----------------- | ----------------------------------------- |
| `users`                | `user.py`         | Authentication accounts                   |
| `entrepreneur_profiles`| `entrepreneur.py` | User business profiles                    |
| `requirements`         | `requirement.py`  | Per-profile support needs                 |
| `schemes`              | `scheme.py`       | Legacy v1 schemes (kept for compat)       |
| `schemes_v2`           | `scheme_v2.py`    | **Canonical** structured schemes          |
| `eligibility_rules`    | `scheme_v2.py`    | Rules attached to v2 schemes              |
| `saved_schemes`        | `saved_scheme.py` | User bookmarks                            |

## 2. Entity Relationship (logical)

```
users 1 ─── 1 entrepreneur_profiles 1 ─── * requirements
  │                                        (support needs)
  │
  ├── * saved_schemes * ──── schemes_v2
  │                     (bookmarks)          │
  │                                          ├── * eligibility_rules
  │                                          │
  └── (legacy: schemes kept for compat)
```

## 3. Table Details

### 3.1 `users`
| Column        | Type     | Notes                         |
| ------------- | -------- | ----------------------------- |
| id            | PK       | auto-increment                |
| email         | unique   | validated, indexed            |
| hashed_password| text    | bcrypt hash                   |
| reset_token / reset expiry | text/datetime | for password reset (if stored) |
| created_at / updated_at | datetime |             |

### 3.2 `entrepreneur_profiles`
| Column                    | Type    | Notes                                 |
| ------------------------- | ------- | -------------------------------------- |
| id                        | PK      | —                                      |
| user_id                   | FK → users | unique per user                     |
| business_name             | text    | --                                    |
| business_type             | text    | e.g. `self_employed`                  |
| business_sector           | text    | e.g. `food_processing`                |
| business_stage            | text    | e.g. `early_stage`                    |
| state                     | text    | Indian state key                      |
| enterprise_category       | text    | micro / small / medium                 |
| annual_income_range       | text    | band key                              |
| social_category           | text    | general / obc / sc / st / other        |
| gender                    | text    | female / male / others / any           |
| business_age_months       | int     | --                                    |
| funding_needed            | bool    | --                                    |
| description               | text    | free-text context                     |

### 3.3 `requirements` (support needs)
| Column          | Type     | Notes                       |
| --------------- | -------- | --------------------------- |
| id              | PK       | —                           |
| profile_id      | FK → entrepreneur_profiles | — |
| requirement_type| text     | loan, subsidy, grant, training, marketing, ... |

### 3.4 `schemes_v2` (canonical)
Stores the flat-ish structured model consumed by the eligibility engine and the
Gov Data Structure serializer.

| Column                    | Type      | Notes                                  |
| ------------------------- | --------- | -------------------------------------- |
| id                        | PK        | —                                      |
| name / short_name         | text      | —                                      |
| description               | text      | —                                      |
| scheme_type               | text      | loan/subsidy/grant/credit_subsidy/...  |
| status                    | text      | `active` filtered by engine            |
| ministry / department / implementing_agency | text | —            |
| primary_sector            | text      | —                                      |
| sub_sectors               | JSON array| —                                      |
| applicant_types           | JSON array| —                                      |
| business_stages           | JSON array| —                                      |
| geographic_scope          | text      | national / state                       |
| states                    | JSON array| —                                      |
| enterprise_categories     | JSON array| micro/small/medium/...                |
| business_age min/max      | int       | months                                 |
| turnover min/max          | numeric   | —                                      |
| investment min/max        | numeric   | —                                      |
| founder age min/max       | int       | —                                      |
| gender_eligibility        | JSON array| —                                      |
| social_categories         | JSON array| —                                      |
| supported_purposes        | JSON array| —                                      |
| funding_required          | bool      | —                                      |
| benefit_types             | JSON array| —                                      |
| benefit_description       | text      | —                                      |
| maximum_amount            | numeric   | —                                      |
| application_mode          | text      | online/offline/both                    |
| official_url / application_url | text | —                                   |
| source_name / source_url  | text      | audit trail                            |
| last_verified             | date      | data freshness                        |
| eligibility_summary       | JSON array| human-readable bullets                |
| benefits_list             | JSON array| —                                      |
| application_process       | JSON array| step-by-step                          |
| required_documents        | JSON array| `[{name, mandatory}]`                 |
| created_at / updated_at   | datetime  | —                                      |
| version                   | int       | seed version                           |

### 3.5 `eligibility_rules`
| Column     | Type  | Notes                                      |
| ---------- | ----- | ------------------------------------------ |
| id         | PK    | —                                          |
| scheme_id  | FK → schemes_v2 | —                              |
| field      | text  | e.g. `business_age_months`, `turnover`     |
| operator   | text  | `gte` / `lte` / `eq` / `in` / `contains`   |
| value      | text  | —                                          |
| required   | bool  | `true` = hard filter rule                  |

### 3.6 `saved_schemes`
| Column     | Type          | Notes                       |
| ---------- | ------------- | --------------------------- |
| id         | PK            | —                           |
| user_id    | FK → users    | —                           |
| scheme_id  | FK → schemes_v2 | —                         |
| saved_at   | datetime      | —                           |

### 3.7 `schemes` (legacy v1)
Kept for backward compatibility; v1 API and older seed data reference it. New
work must use `schemes_v2`.

---

## 4. Indexes & Constraints

| Table                  | Index / constraint                         |
| ---------------------- | ------------------------------------------ |
| users                  | unique(email)                              |
| entrepreneur_profiles  | unique(user_id)                            |
| saved_schemes          | unique(user_id, scheme_id); indexes on both FKs |
| eligibility_rules      | index(scheme_id)                           |
| schemes_v2             | index(primary_sector), index(status)       |

## 5. Migration / Seeding

```bash
# create missing tables + seed v2 catalog (idempotent)
python migrate_v2.py

# destructive refresh of scheme rows only (users/profiles preserved)
python data/schemes_seed_v2.py --force
```

## 6. Production Notes

- Swap `DATABASE_URL` to PostgreSQL; models are engine-agnostic.
- JSON array columns use SQLAlchemy JSON types (portable across SQLite/PG).
- In prod, add proper migration tooling (Alembic) before scaling schema changes.