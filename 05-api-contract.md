# 05 · API Contract

**Project:** ArthSetu — AI Scheme Analyzer for Marginalized Entrepreneurs
**Base URL (dev):** `http://127.0.0.1:8000/api`
**Interactive docs:** `http://localhost:8000/docs` (Swagger) · `/redoc` (ReDoc)

Auth: protected endpoints require `Authorization: Bearer <access_token>`

---

## 1. Endpoint Summary

| Method | Endpoint                                       | Auth | Description                              |
| ------ | ---------------------------------------------- | ---- | ----------------------------------------- |
| GET    | `/health`                                      | No   | Liveness + version                        |
| GET    | `/`                                            | No   | Service metadata, docs links              |
| POST   | `/api/auth/register`                           | No   | Register (email + password)               |
| POST   | `/api/auth/login`                              | No   | Login → JWT access token                  |
| GET    | `/api/auth/me`                                 | Yes  | Current user                              |
| POST   | `/api/auth/forgot-password`                    | No   | Request password reset token              |
| POST   | `/api/auth/reset-password`                     | No   | Set new password with reset token         |
| POST   | `/api/profile`                                 | Yes  | Create entrepreneur profile               |
| GET    | `/api/profile`                                 | Yes  | Fetch profile (incl. support needs)       |
| PUT    | `/api/profile`                                 | Yes  | Update profile                            |
| POST   | `/api/recommendations`                         | Yes  | **Core** eligibility-based recommendations |
| GET    | `/api/schemes`                                 | Yes  | List schemes (filterable summaries)       |
| GET    | `/api/schemes/{id}`                            | Yes  | Full scheme in Gov Data Structure         |
| GET    | `/api/saved-schemes`                           | Yes  | List saved schemes                        |
| POST   | `/api/saved-schemes/{id}`                      | Yes  | Save a scheme                             |
| DELETE | `/api/saved-schemes/{id}`                      | Yes  | Remove saved scheme                       |
| POST   | `/api/v2/recommendations`                      | Yes  | v2 flavor of same engine                  |
| GET    | `/api/v2/recommendations/schemes`              | Yes  | List all v2 schemes (client-side filter)  |
| GET    | `/api/v2/recommendations/schemes/{id}`         | Yes  | v2 scheme detail                          |

---

## 2. Auth Endpoints

### 2.1 `POST /api/auth/register`
```json
// Request
{ "email": "priya@example.com", "password": "StrongPass123" }
// Response 200
{ "id": 1, "email": "priya@example.com", "created_at": "..." }
```
Errors: `400` duplicate/invalid email.

### 2.2 `POST /api/auth/login`
```json
// Request
{ "email": "priya@example.com", "password": "StrongPass123" }
// Response 200
{ "access_token": "<jwt>", "token_type": "bearer" }
```
Errors: `401` bad credentials.

### 2.3 `GET /api/auth/me`
Returns current user object. Errors: `401` missing/invalid token.

### 2.4 Password Reset
```json
// POST /api/auth/forgot-password
{ "email": "priya@example.com" }
// Response 200 — dev logs the reset link

// POST /api/auth/reset-password
{ "token": "<reset-jwt>", "new_password": "NewStrongPass123" }
```
Reset token is a short-lived JWT with `typ=reset`. Frontend: `reset-password.html?token=...`.

---

## 3. Profile Endpoints

### 3.1 `POST /api/profile` (create)
```json
{
  "business_name": "Priya Stitching",
  "business_type": "self_employed",
  "business_sector": "textiles_apparel",
  "business_stage": "early_stage",
  "state": "maharashtra",
  "enterprise_category": "micro",
  "annual_income_range": "under_1_lakh",
  "social_category": "obc",
  "gender": "female",
  "business_age_months": 14,
  "funding_needed": true,
  "support_needs": ["loan", "training"]
}
```

### 3.2 `GET /api/profile` / `PUT /api/profile`
Same shape; GET returns profile joined with requirements/support needs.

---

## 4. Recommendations (Core)

### 4.1 `POST /api/recommendations`
```json
// Request
{
  "sector": "food_processing",
  "state": "maharashtra",
  "business_stage": "early_stage",
  "annual_income_range": "under_1_lakh",
  "entrepreneur_type": "other",
  "support_needs": ["loan", "marketing", "training"],
  "description": "small pickle manufacturing unit",
  "min_score": 40,
  "max_results": 10
}
```

### 4.2 Response (v2 shape)
```jsonc
{
  "recommendations": [
    {
      "scheme": {
        "id": 18,
        "name": "PM Formalisation of Micro Food Processing Enterprises",
        "short_name": "PMFME",
        "description": "...",
        "scheme_type": "subsidy",
        "ministry": "Ministry of Food Processing Industries",
        "department": null,
        "primary_sector": "food_processing",
        "business_stages": ["early_stage", "growth"],
        "geographic_scope": "national",
        "states": [],
        "benefit_types": ["credit_subsidy", "grant"],
        "benefit_description": "Credit linked subsidy up to 35%",
        "maximum_amount": 10000000,
        "application_url": "https://...",
        "official_url": "https://...",
        "eligibility_summary": ["...", "..."],
        "benefits_list": ["...", "..."],
        "application_process": ["...", "..."],
        "required_documents": [{ "name": "Aadhaar", "mandatory": true }]
      },
      "match_score": 87.5,
      "match_level": "strong",
      "matched_criteria": ["sector match", "state match"],
      "score_breakdown": {
        "sector": 30.0, "purpose": 25.0, "stage": 20.0,
        "location": 12.5, "type": 0.0, "size": 0.0
      }
    }
  ],
  "total_count": 5,
  "filters_applied": { "min_score": 40, "max_results": 10, "sector": "food_processing", "state": "maharashtra" }
}
```

Legacy v1 (`/api/recommendations`) returns a **flat** shape — normalized
client-side by `js/matching.js` (see `frontend/js/api.js` + README).

### 4.3 Rules Applied
1. Mandatory eligibility filter (hard rules from `eligibility_rules`)
2. Weighted scoring: **sector > purpose > stage > location > type > size**
3. Rank desc by `match_score`, keep ≥ `min_score`, slice `max_results`

---

## 5. Schemes

### 5.1 `GET /api/schemes` (list)
Query params: `sector`, `state`, `scheme_type`, `skip`, `limit`.
Returns array of `SchemeListInfo` (see `app/schemas/recommendation.py`).

### 5.2 `GET /api/schemes/{id}` (detail — Government Data Structure)
```jsonc
{
  "scheme_id": 4,
  "basic_info":   { "name", "short_name", "description", "scheme_type", "status" },
  "government":   { "ministry", "department", "implementing_agency" },
  "target_beneficiaries": { "applicant_types": [...], "business_stages": [...] },
  "sector":       { "primary", "sub_sectors": [...] },
  "geography":    { "scope": "national|state", "states": [...] },
  "business_eligibility": { "business_types", "enterprise_categories",
                            "minimum_business_age_months", "maximum_business_age_months" },
  "financial_eligibility": { "minimum_turnover", "maximum_turnover",
                             "minimum_investment", "maximum_investment" },
  "founder_eligibility":   { "minimum_age", "maximum_age", "gender", "social_categories" },
  "requirements": { "purposes": [...], "funding_required": bool },
  "benefits":     { "type": [...], "description", "maximum_amount", "currency" },
  "eligibility_rules": [ { "field", "operator", "value", "required" } ],
  "required_documents": [ { "name", "mandatory" } ],
  "application":  { "mode", "official_url", "application_url" },
  "source":       { "source_name", "source_url", "last_verified" },
  "metadata":     { "created_at", "updated_at", "version" }
}
```

---

## 6. Saved Schemes

| Method | Endpoint                    | Body/Params                       | Returns        |
| ------ | --------------------------- | -------------------------------- | -------------- |
| GET    | `/api/saved-schemes`        | —                                | saved list     |
| POST   | `/api/saved-schemes/{id}`   | `scheme_id` in path              | saved item     |
| DELETE | `/api/saved-schemes/{id}`   | `scheme_id` in path              | 204/confirmation |

---

## 7. Error Format

```json
{ "detail": "human-readable error message" }
```

| Status | Meaning                                     |
| ------ | ------------------------------------------- |
| 400    | Validation / "complete your profile first"  |
| 401    | Missing or invalid token / bad credentials  |
| 404    | Scheme/user/saved item not found            |
| 500    | Server error (logs to backend console)      |

---

## 8. Versioning Strategy

- `/api/*` — v1 endpoints (kept for backward compatibility).
- `/api/v2/*` — canonical eligibility-based API.
- Client uses `frontend/js/api.js` as the single point of change; shape changes
  land in `js/matching.js`, never scattered across pages.