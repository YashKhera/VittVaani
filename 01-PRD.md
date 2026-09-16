# 01 · Product Requirements Document (PRD)

**Project:** VittVaani — AI Scheme Analyzer for Marginalized Entrepreneurs
**Team:** VittVaani · **Event:** Smart India Hackathon 2026
**Status:** v1.0 (Approved)

---

## 1. Product Summary

VittVaani is a web application that helps marginalized Indian entrepreneurs
(women, SC/ST/OBC, PwD, rural micro-entrepreneurs) discover and apply for the
government schemes they are actually eligible for. Instead of forcing users to
search through scattered government websites and PDFs, VittVaani asks a short,
adaptive questionnaire and returns a ranked list of schemes personalized to the
user's profile, business, location, and needs.

> VittVaani helps bridge the information gap between
> government schemes and the entrepreneurs who qualify for them.

## 2. Problem Statement

- Government fund & support schemes are spread across ministries, state portals,
  and PDF gazettes.
- Eligibility criteria are complex, jargon-heavy, and inconsistent across schemes.
- Marginalized entrepreneurs rarely know which schemes they qualify for or how
  to apply, leading to **low scheme uptake** for the very groups the schemes target.
- Existing aggregator portals are generic; they list schemes but do not **score
  eligibility**, leaving the hard work to the user.

## 3. Vision

Enable every marginalized Indian entrepreneur to discover, understand, and
access every government scheme they are eligible for — in minutes, in their own
language.

## 4. Target Users / Personas

| Persona            | Description                                            | Primary Need                         |
| ------------------ | ------------------------------------------------------ | ------------------------------------ |
| Priya (rural woman entrepreneur) | Tailoring business, village in Maharashtra, OBC | Finds it for a low-interest loan + training scheme |
| Ravi (differently-abled maker)   | Handicraft unit, age 34, 2 years old business  | Loan top-up + subsidy for equipment   |
| Digital-first entrepreneur       | Urban, English/Hindi, wants quick shortlists  | Fast ranked results with reasons      |
| Field officer / NGO volunteer    | Helps multiple entrepreneurs apply          | Simple shareable scheme detail pages  |

Primary audience priority: **marginalized micro-entrepreneurs** > general
MSME owners > facilitators/NGOs.

## 5. Goals

### 5.1 Business Goals
- Maximize comprehensible, eligibility-scored scheme recommendations.
- Reduce time-to-answer: from "hours of research" to **under 5 minutes**.
- Maximize reach via bilingual (EN/Hindi) and mobile-friendly UI.

### 5.2 User Goals
- Answer a guided questionnaire once; get ranked, personalized schemes.
- Understand **why** a scheme matches (score breakdown + reasons).
- Save/bookmark schemes and revisit them.
- Read scheme details in the official Government Data Structure format.

### 5.3 Non-Goals (v1)
- No live application submission to government portals.
- No financial advisory or legal guarantee of approval.
- No offline mobile app (responsive web only).

## 6. Scope

### 6.1 In Scope (MVP)
- Account registration & JWT login (email + password).
- Entrepreneur profile creation/update (business, sector, location, category).
- Adaptive 9-question questionnaire (branching follow-ups).
- Eligibility-based matching engine (mandatory-rule filter + weighted scoring).
- Ranked results with score breakdown and match reasons.
- Scheme catalog (`schemes_v2`) of 73 central + state schemes with structured rules.
- Scheme detail pages in Government Data Structure format.
- Bookmark / saved-schemes.
- Bilingual UI (English + Hindi) and dark mode.
- Profile view with completeness meter.

### 6.2 Out of Scope (v1)
- Payment/integration with government application portals.
- Automated document upload / KYC.
- Chatbot assistant.
- Mobile native apps.

## 7. Key Features

| ID   | Feature                     | Description                                                            |
| ---- | --------------------------- | ---------------------------------------------------------------------- |
| F-01 | Adaptive questionnaire      | 9-question flow; `showIf` branching (e.g., `food_processing` reveals follow-up) |
| F-02 | Eligibility matching engine | Mandatory-rule hard filter → weighted relevance scoring → ranking      |
| F-03 | Ranked recommendations      | Score breakdown + match reasons per scheme card                        |
| F-04 | Scheme catalog              | 73 structured schemes, central + state-level coverage                  |
| F-05 | Scheme detail              | Full Government Data Structure payload per scheme                      |
| F-06 | Saved schemes               | Bookmark / un-bookmark, persisted list                                 |
| F-07 | Profile completeness        | Profile view with completeness meter                                   |
| F-08 | i18n                        | English ↔ Hindi toggle, persisted per user                             |
| F-09 | Dark mode                   | Theme toggle, OS-preference aware, persisted                            |
| F-10 | Auth (JWT)                  | Register / login / forgot + reset password                             |

## 8. User Flow (Happy Path)

```
Landing (index.html)
   │  Register / Login
   ▼
Profile capture (profile.html)
   │  business details, sector, location, category
   ▼
Questionnaire (questionnaire.html)
   │  9 adaptive questions + branching
   ▼
Results (results.html)
   │  ranked, eligibility-scored scheme cards + filters
   ├──▶ Scheme detail (scheme-details.html)
   └──▶ Save bookmark → saved-schemes.html
   ▼
Profile view (profile-view.html) with completeness meter
```

## 9. Success Metrics

| Metric                          | Target (post-launch)                    |
| ------------------------------- | --------------------------------------- |
| Questionnaire completion rate   | ≥ 70%                                   |
| Average time from start → results | ≤ 5 minutes                            |
| Users receiving ≥1 eligible scheme | ≥ 95%                                  |
| Hindi UI adoption               | ≥ 30% of sessions                       |
| Scheme detail page CTR          | ≥ 40%                                   |
| Saved schemes per active user   | ≥ 2                                     |
| API p95 latency for `/recommendations` | ≤ 300 ms                            |

## 10. Constraints & Assumptions

- Hackathon timelines: MVP in ~4 sprint weeks.
- Data source: publicly published government scheme pages (curated manually in seed data).
- Default deployment is localhost/dev; prod-ready config via PostgreSQL.
- Scheme data evolves; seed refresh is destructive to schemes only (users/profiles preserved).

## 11. Risks

| Risk                                  | Mitigation                                              |
| ------------------------------------- | ------------------------------------------------------- |
| Scheme data becomes stale             | Versioned seed data + `updated_at` + source URLs        |
| Rule data inaccurate                  | Eligibility rules stored per scheme, easily audITED     |
| Low-language coverage                 | i18n framework in place; Hindi shipped; more languages later |
| Matching feels arbitrary              | Transparent score breakdown + reasons on every card     |
| Abandonment at questionnaire          | Branching + short 9-question flow + progress bar        |

## 12. Release Plan

| Milestone     | Scope                                            |
| ------------- | ------------------------------------------------ |
| M0 · Foundation | Backend scaffold, auth, DB, serve scripts       |
| M1 · Catalog   | Scheme models v1/v2, seed 73 schemes, API list/detail |
| M2 · Profiling | Profile CRUD + questionnaire + sync              |
| M3 · Matching  | Eligibility engine + ranked recommendations       |
| M4 · UX polish | i18n, dark mode, responsive CSS, saved schemes    |
| M5 · Hardening | Tests, security pass, docs, demo runbook          |

See [`12-roadmap.md`](./12-roadmap.md) for dates and backlog.

## 13. Out of Scope / Future

- Google/Mobile OAuth login
- Document upload & verification
- AI assistant (chat) grounded on scheme data
- Mobile app wrapper (PWA)
- Multi-language beyond EN/Hindi (e.g., regional languages)
- Notifications & expiry alerts for deadlines