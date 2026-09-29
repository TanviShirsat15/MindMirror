# MindMirror — Phase 3 Implementation Plan
## Frontend UI & Application Shell

*Prerequisite: Phase 0 Specification (approved), Phase 1 (Development Environment & GitHub Setup, completed), Phase 2 (Project Architecture & Foundation, completed and approved). This document does not repeat their content and builds strictly on top of them.*

**Global rule in effect for this phase and every phase after it:**
> If any error, bug, dependency problem, configuration issue, or unexpected behavior occurs, do not rebuild the entire project. Identify the specific problem and make only the necessary targeted fix. Do not modify working features or unrelated parts of the project. Preserve all existing functionality.

---

## A. Phase Objective

Build the complete frontend application shell for MindMirror: routing, layout, navigation, a consistent design system, and static/placeholder versions of every required screen, all backed by isolated mock data. At the end of this phase, a user can click through the entire app and see every screen with realistic-looking placeholder content, loading/empty/error/success states, and working navigation — but no real authentication, no database-backed journal or habit data, no NLP, no fuzzy inference, and no production analytics exist yet. The architecture must be organized so that later phases plug real functionality into this shell without restructuring it.

### A.1 — What Phase 3 Does NOT Include

Phase 3 is frontend UI and shell only. Phase 3 must **not**:
- implement real authentication or an authentication backend
- implement database-backed journal CRUD
- implement database-backed habit CRUD
- implement NLP or NLP analysis
- implement the Mamdani Fuzzy Inference System or any well-being score calculation
- implement personal baseline calculation
- implement production analytics or trend calculations
- implement insight-generation logic
- create the full application database schema
- implement API business logic beyond what Phase 2 already established (the health-check endpoint)
- implement production user/account management

It must also not:
- change or remove any Phase 1 work (environment, repo structure, `.gitignore`, `README`)
- change or remove any Phase 2 backend work (FastAPI structure, MySQL configuration, SQLAlchemy foundation, Alembic foundation, health-check endpoint, or the existing frontend-backend health-check communication)
- introduce PostgreSQL, MongoDB, Firebase, Redis, Docker, Kubernetes, TensorFlow, PyTorch, LangChain, OpenAI API, external LLM APIs, or unnecessary UI libraries
- silently change any approved requirement from Phase 0, Phase 1, or Phase 2

If Antigravity finds itself writing code that does any of the above while executing this document, it should stop and treat that as outside this phase's scope.

---

## B. Prerequisites

- Phase 2 completed and approved: `backend/app/` scaffolded (`main.py`, `config.py`, `database.py`, `api/health.py`), MySQL connected via env vars, SQLAlchemy engine/session in place (no models), Alembic foundation initialized (no migrations), `GET /api/health` working, and the existing `frontend/` scaffold (React + Vite + TypeScript + Tailwind + Recharts + Lucide React) calling that endpoint successfully.
- Node.js, npm, and the existing `frontend/` dependencies from Phase 2 already installed and working.

---

## C. Exact Implementation Sequence

### C.1 — Dependencies
Add only what routing requires; everything else needed is already installed from Phase 2:
```bash
npm install react-router-dom
```
No other new libraries are introduced. Tailwind, Recharts, and Lucide React remain exactly as configured in Phase 2.

### C.2 — React Application Structure and Organization
Reorganize `frontend/src/` into a maintainable structure:
```
frontend/src/
├── main.tsx
├── App.tsx                        # Router + top-level providers only
├── routes/
│   └── AppRoutes.tsx              # Central route definitions
├── layouts/
│   ├── AppLayout.tsx              # Authenticated shell: sidebar/header + content
│   └── AuthLayout.tsx             # Minimal shell for Login/Sign Up
├── pages/
│   ├── auth/
│   │   ├── LoginPage.tsx
│   │   └── SignUpPage.tsx
│   ├── dashboard/
│   │   └── DashboardPage.tsx
│   ├── journal/
│   │   └── JournalPage.tsx
│   ├── habits/
│   │   └── HabitsPage.tsx
│   ├── wellbeing/
│   │   └── WellBeingAnalysisPage.tsx
│   ├── analytics/
│   │   └── AnalyticsHistoryPage.tsx
│   ├── insights/
│   │   └── InsightsPage.tsx
│   └── settings/
│       └── ProfileSettingsPage.tsx
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── PageContainer.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── TextArea.tsx
│   │   ├── Badge.tsx
│   │   ├── Modal.tsx
│   │   ├── LoadingState.tsx
│   │   ├── EmptyState.tsx
│   │   └── ErrorState.tsx
│   └── charts/
│       └── ChartContainer.tsx
├── mock/
│   ├── mockJournalEntries.ts
│   ├── mockHabits.ts
│   ├── mockWellBeing.ts
│   ├── mockAnalytics.ts
│   ├── mockInsights.ts
│   └── mockUser.ts
├── styles/
│   └── index.css                  # Tailwind directives + design tokens
└── types/
    └── mockTypes.ts               # TypeScript types for mock data shapes only
```

### C.3 — React Router Setup and Route Structure
| Path | Page | Layout |
|---|---|---|
| `/login` | `LoginPage` | `AuthLayout` |
| `/signup` | `SignUpPage` | `AuthLayout` |
| `/` (redirects to `/dashboard`) | — | `AppLayout` |
| `/dashboard` | `DashboardPage` | `AppLayout` |
| `/journal` | `JournalPage` | `AppLayout` |
| `/habits` | `HabitsPage` | `AppLayout` |
| `/wellbeing` | `WellBeingAnalysisPage` | `AppLayout` |
| `/analytics` | `AnalyticsHistoryPage` | `AppLayout` |
| `/insights` | `InsightsPage` | `AppLayout` |
| `/settings` | `ProfileSettingsPage` | `AppLayout` |

- Use `react-router-dom`'s nested routes: an `AppLayout` route element wrapping the authenticated pages, and an `AuthLayout` route element wrapping Login/Sign Up.
- No route guarding/redirect-on-auth-failure logic is implemented in Phase 3, since there is no real authentication yet — all routes are reachable directly for UI demonstration purposes. A clearly marked placeholder comment should note that route protection is added once real authentication exists.
- Sidebar/header navigation links use React Router's `<Link>` / `<NavLink>` so navigation between all screens works without full page reloads.

---

## D. Git Checkpoints
1. `Phase 3: add React Router and base route/layout structure`
2. `Phase 3: add design tokens and shared UI components`
3. `Phase 3: add mock data modules and types`
4. `Phase 3: implement Login and Sign Up UI`
5. `Phase 3: implement Dashboard UI`
6. `Phase 3: implement Journal UI`
7. `Phase 3: implement Habits UI`
8. `Phase 3: implement Well-Being Analysis, Analytics/History, and Insights UI`
9. `Phase 3: implement Profile/Settings UI and accessibility pass`
Final: `Phase 3 complete: frontend UI and application shell verified`
