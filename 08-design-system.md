# 08 · Design System

**Project:** VittVanni — AI Scheme Analyzer for Marginalized Entrepreneurs

Frontend is a static site with a small design-token system. No frameworks, no
build step. All CSS lives in `frontend/css/`.

---

## 1. Files

| File                    | Responsibility                     |
| ----------------------- | ---------------------------------- |
| `variables.css`         | Design tokens (colors, spacing, type) |
| `global.css`            | Reset, base typography, utilities  |
| `layout.css`            | Page layout, container grid        |
| `components.css`        | Cards, buttons, forms, badges, toasts |
| `navigation.css`        | Navbar, toggles, links             |
| `responsive.css`        | Breakpoints, mobile-first tweaks   |

## 2. Design Tokens (`variables.css`)

```css
/* Light + dark via [data-theme="dark"] overrides */
--color-primary
--color-primary-hover
--color-bg
--color-surface
--color-text
--color-text-muted
--color-border
--color-success
--color-warning
--color-error
--radius-sm / --radius-md / --radius-lg
--space-1 … --space-8
--font-family-base / --font-size-sm/md/lg
```

## 3. Theming & i18n

- **Dark mode:** `js/theme.js` toggles `data-theme="dark"` on `<html>`; respects
  `localStorage: theme`, falls back to OS preference (`prefers-color-scheme`).
- **Language:**- **i18n:** `js/i18n.js` holds EN ⇄ Hindi dictionaries. UI strings use
  `data-i18n="key"`; the switcher re-renders text nodes and persists
  `localStorage: lang`. Scheme/business content stays in English (source data).

## 4. Core Components

| Component          | File                          | Behavior                              |
| ------------------ | ----------------------------- | ------------------------------------- |
| Navbar             | `js/components/navbar.js`     | Brand, nav links, theme + language toggles |
| Scheme card        | `js/components/scheme-card.js`| Renders normalized recommendation, score badge, reasons, save toggle |
| Progress bar       | `js/components/progress-bar.js`| Questionnaire completion indicator   |

## 5. Screen Inventory

| Page               | File                 | Key UI                                   |
| ------------------ | -------------------- | ---------------------------------------- |
| Landing            | `index.html`         | hero, featured schemes                   |
| Register / Login   | `register.html` / `login.html` | validated forms                    |
| Profile            | `profile.html`       | profile capture form                     |
| Profile view       | `profile-view.html`  | summary + completeness meter             |
| Questionnaire      | `questionnaire.html` | 1-question-at-a-time, branching, progress |
| Results            | `results.html`       | ranked cards, filters, score breakdown   |
| Scheme details     | `scheme-details.html`| Gov Data Structure detail layout         |
| Saved              | `saved-schemes.html` | bookmark list                            |
| Reset password     | `reset-password.html`| token + new password form                |

## 6. Usability Principles

1. **Mobile-first** — touch targets ≥ 44px; results cards stack on small screens.
2. **Clarity over density** — one primary action per screen.
3. **Explainable matching** — match reasons are visible on every card.
4. **Accessibility (WCAG AA)** — contrast in both themes, keyboard navigable,
   form fields with labels and inline validation (`js/validation.js`).
5. **Zero-cache dev** — `python serve.py` serves assets with no-cache so the UI
   always reflects latest changes.

## 7. Token Usage Rules

- Never hardcode colors/spacing in components; use variables.
- Theme-aware colors come from tokens, not page-specific overrides.
- New UI strings go through `i18n.js` dictionaries, not inline text only.
- API payloads are normalized by `js/matching.js` before rendering.