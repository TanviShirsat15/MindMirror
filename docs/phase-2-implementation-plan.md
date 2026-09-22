# MindMirror — Phase 2 Implementation Plan
## Project Architecture & Foundation

*Prerequisite: Phase 0 Specification (approved, source of truth) and Phase 1 (Development Environment & GitHub Setup, completed). This document does not repeat Phase 0 or Phase 1 content and builds strictly on top of the Phase 1 foundation.*

**Global rule in effect for this phase and every phase after it:**
> If any error, bug, dependency problem, configuration issue, or unexpected behavior occurs, do not rebuild the entire project. Identify the specific problem and make only the necessary targeted fix. Do not modify working features or unrelated parts of the project. Preserve all existing functionality.

---

## A. Phase Objective

Turn the empty `frontend/`, `backend/`, and `docs/` skeleton from Phase 1 into a running, connected, but still-empty-of-features foundation: a scaffolded React + Vite + TypeScript frontend, a scaffolded FastAPI backend with proper package structure, MySQL connectivity configured through environment variables, SQLAlchemy wired up, an Alembic foundation ready for future migrations, a working health-check endpoint, and confirmed frontend-to-backend communication. This document is the instruction set Antigravity executes to carry out Phase 2 itself, continuing the same sequential, phase-by-phase execution established in Phase 1.

### A.1 — What Phase 2 Does NOT Include

Phase 2 builds the architectural skeleton only. Phase 2 must **not**:
- implement authentication (no login, registration, password hashing, tokens/sessions)
- implement journal CRUD functionality
- implement habit tracking functionality
- implement NLP feature extraction
- implement the Mamdani Fuzzy Inference System
- implement analytics, baselines, or trend computation
- implement insight generation
- implement dashboard UI beyond a minimal placeholder needed to prove frontend-backend communication
- create the full application database schema (users, journals, habits, indices, baselines, etc.) — Alembic is initialized and capable of running a migration, but no application tables are defined or created in this phase

Any of the above belongs to a later phase. If Antigravity finds itself writing code that does any of these things while executing this document, it should stop and treat that as outside this phase's scope.

---

## B. Prerequisites

- Phase 1 completed and verified: Node.js, Python, MySQL, and Git installed; project at `C:\Dev\MindMirror`; `frontend/`, `backend/`, `docs/` exist; `.gitignore` and `README.md` in place; `backend/venv` created and activating; local repo connected to `https://github.com/TanviShirsat15/MindMirror` with an initial commit pushed
- A MySQL database (`mindmirror_db`) and dedicated database user already created and verified per Phase 1 (no application tables yet)
- The Phase 0 specification and Phase 1 plan present in `docs/`

### Step 0 — Inspect Phase 1 and Current Git Status First

Before making any changes, Antigravity must verify the starting state rather than assume it:
1. Confirm the working directory is `C:\Dev\MindMirror` and the folder structure matches Phase 1's completion criteria (`frontend/`, `backend/`, `docs/`, `.gitignore`, `README.md`).
2. Run `git status` and `git log --oneline` to confirm:
   - the working tree is clean (no uncommitted changes left over)
   - the Phase 1 baseline commit exists and has been pushed to `origin/main`
3. Run `git remote -v` to confirm `origin` still points to `https://github.com/TanviShirsat15/MindMirror.git`.
4. Confirm `backend/venv` exists and activates (`venv\Scripts\Activate.ps1`), and that `frontend/` and `backend/` are still otherwise empty (aside from any `.gitkeep` placeholders) — i.e., no partial/abandoned scaffolding from an earlier attempt.
5. Confirm the MySQL database and user from Phase 1 are reachable (`mysql -u <project_user> -p -h localhost mindmirror_db`).
6. If any of the above is missing or inconsistent, stop and apply the smallest targeted fix to restore the expected Phase 1 state before starting Phase 2 work — do not proceed on an unverified foundation, and do not rebuild Phase 1 wholesale to fix a small inconsistency.

Only once Step 0 passes does Phase 2 implementation begin.

---

## C. Exact Implementation Sequence

### C.1 — FastAPI Backend Initialization and Package Structure
Inside `backend/`, with `venv` activated, create the following structure (files, not just folders):

```
backend/
├── venv/                  (already exists from Phase 1, git-ignored)
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI entry point
│   ├── config.py          # Settings/configuration handling
│   ├── database.py        # SQLAlchemy engine/session setup
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py      # Health-check endpoint router
│   └── core/
│       └── __init__.py    # Reserved for later shared utilities (empty in Phase 2)
├── alembic/
│   ├── versions/          # Empty in Phase 2 — no migrations generated yet
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── requirements.txt
├── .env.example           # Documents required variables; no real secrets
└── .env                   # Actual local values; git-ignored (already covered by Phase 1's .gitignore)
```

1. Install the minimum required packages into the activated venv:
   ```
   pip install fastapi uvicorn[standard] sqlalchemy pymysql alembic python-dotenv pydantic-settings
   ```
2. Freeze them into `requirements.txt`:
   ```
   pip freeze > requirements.txt
   ```
3. This package list is intentionally minimal — no NLP libraries, no scikit-fuzzy, no auth libraries yet. Those are introduced only in the phase that implements the feature that needs them, per the approved spec's phased scope.

### C.2 — MySQL Configuration Through Environment Variables
1. Create `backend/.env.example` documenting the required variables (no real values):
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=mindmirror_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   APP_ENV=development
   ```
2. Create `backend/.env` with the actual local values matching the database and user created in Phase 1. This file must never be committed (already excluded by Phase 1's `.gitignore`).
3. No hardcoded credentials may appear anywhere in `app/` — every credential is read from environment variables, consistent with Phase 0's security requirements.

### C.3 — Configuration/Settings Handling
In `backend/app/config.py`, define a settings object (using `pydantic-settings`) that reads the environment variables above and exposes a single `settings` instance the rest of the app imports, rather than reading `os.environ` directly in multiple places. This centralizes configuration and makes future settings additions (in later phases) a targeted change to one file.

### C.4 — SQLAlchemy Setup
In `backend/app/database.py`:
- Build the MySQL connection string from `settings` (e.g., using the `mysql+pymysql://` driver).
- Create the SQLAlchemy `engine`.
- Create a `SessionLocal` session factory.
- Create a `Base` declarative base, ready for future models — but define no models in this phase.
- Provide a simple `get_db()` dependency function for later use by endpoints, even though no data-bearing endpoint exists yet.

### C.5 — Alembic Foundation
1. From `backend/`, with `venv` active, initialize Alembic:
   ```
   alembic init alembic
   ```
2. Edit `alembic.ini` and `alembic/env.py` so Alembic reads the database URL from the same `settings` / `.env` source as the app, instead of a hardcoded URL — this keeps a single source of truth for the connection string.
3. Confirm Alembic can talk to the database with a no-op check:
   ```
   alembic current
   ```
   This should run without error and report no current revision — it does not generate or apply any migration, since there is no schema yet.
4. Leave `alembic/versions/` empty. The first real migration (creating application tables) belongs to the phase that defines the data model.

### C.6 — FastAPI Entry Point
In `backend/app/main.py`:
- Create the FastAPI `app` instance.
- Configure CORS using `settings` (allow the frontend's local dev origin, e.g. `http://localhost:5173`, and nothing wider than necessary), per Phase 0's security requirement for proper CORS configuration.
- Include the health-check router from `app/api/health.py`.
- Add a baseline global exception handler (see Section C.11) so unhandled errors return a consistent JSON error shape instead of leaking a raw stack trace.

### C.7 — Basic Health-Check Endpoint
In `backend/app/api/health.py`, define a single `GET /api/health` endpoint that:
- Returns a small JSON payload, e.g. `{"status": "ok", "db": "connected"}`.
- Performs a trivial database check (e.g., `SELECT 1` through the SQLAlchemy engine) to confirm the DB connection works, and reflects that in the response (`"db": "connected"` or `"db": "unreachable"`), without exposing internal error detail to the client.
- This is the only backend endpoint created in Phase 2.

### C.8 — React + Vite + TypeScript Frontend Initialization
1. From `frontend/`, scaffold the app:
   ```
   npm create vite@latest . -- --template react-ts
   ```
   (Run this inside the existing `frontend/` folder — accept prompts to scaffold into the current directory.)
2. Install dependencies:
   ```
   npm install
   ```
3. Install the additional packages named in Phase 0's architecture, so later phases don't need to revisit setup:
   ```
   npm install -D tailwindcss postcss autoprefixer
   npm install recharts lucide-react
   npx tailwindcss init -p
   ```
4. Configure Tailwind (`tailwind.config.js` content paths, `index.css` directives) so it's ready to use, without yet building any real UI beyond the Phase 2 placeholder in C.9.
5. Confirm `frontend/.gitignore`-relevant folders (`node_modules/`, `dist/`) are already covered by the root `.gitignore` from Phase 1 — do not duplicate a second `.gitignore` unless the root one is missing frontend-specific patterns.

### C.9 — Basic Frontend-Backend Communication
1. In the scaffolded `App.tsx` (or a small dedicated component), add a minimal placeholder UI that:
   - On load, calls the backend's `GET /api/health` endpoint (via `fetch`).
   - Displays the returned status (e.g., "Backend: ok / DB: connected") somewhere visible on the page.
2. This is the only frontend behavior implemented in Phase 2 — no journal UI, no habit UI, no dashboard, no charts wired to real data yet, even though Recharts/Lucide are installed and ready for later phases.
3. Configure the Vite dev server (`vite.config.ts`) with a proxy for `/api` to the backend's local address (e.g., `http://localhost:8000`), so the frontend can call `/api/health` without hardcoding the backend's full URL or running into CORS friction during development.

### C.10 — Development/Startup Commands
Document these in `README.md` (update, don't replace, the Phase 1 README) and/or a short `docs/phase2-notes.md`:

Backend:
```powershell
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Frontend:
```powershell
cd frontend
npm run dev
```

Both should be run in separate terminals during development. Visiting the frontend's local URL (typically `http://localhost:5173`) should show the health-check placeholder successfully reporting the backend and DB status.

### C.11 — Baseline Error Handling
- **Backend**: a single global exception handler in `main.py` catches unhandled exceptions and returns a generic `{"detail": "Internal server error"}` with a 500 status, logging the real exception server-side without exposing internal detail to the client — consistent with Phase 0's requirement that sensitive detail not leak, and with not writing sensitive journal-style content to logs (none exists yet, but the pattern is established now).
- **Frontend**: the health-check fetch call wraps its request in a `try`/`catch` and displays a simple "Backend unreachable" message on failure instead of an unhandled promise rejection or blank page.
- No feature-specific error handling (e.g., journal validation errors, auth errors) is implemented yet — only this general baseline.

---

## D. Verification and Tests

| Check | Command / Action | Expected Result |
|---|---|---|
| Backend dependencies installed | `pip list` (venv active) | Shows fastapi, uvicorn, sqlalchemy, pymysql, alembic, python-dotenv, pydantic-settings |
| Backend starts | `uvicorn app.main:app --reload --port 8000` | Starts without error; no stack trace on startup |
| Health endpoint responds | Visit `http://localhost:8000/api/health` or `curl` it | Returns `{"status": "ok", "db": "connected"}` |
| DB connectivity confirmed | Same health-check response | `"db": "connected"` (not `"unreachable"`) |
| Alembic wired up | `alembic current` (from `backend/`, venv active) | Runs without error; reports no current revision (expected — no migrations yet) |
| Frontend installs | `npm install` (from `frontend/`) | Completes without error |
| Frontend starts | `npm run dev` | Vite dev server starts, prints a local URL |
| Frontend-backend communication | Open the frontend URL in a browser | Page displays the health-check result from the backend (not an error state, assuming backend is also running) |
| No premature scope | Manual review of `app/` and `src/` | No auth, journal, habit, NLP, fuzzy, analytics, or insight code present anywhere |
| Secrets not committed | `git status` after all changes | `.env` (backend and frontend, if present) does not appear as a tracked/staged file |

If any check fails, apply the smallest targeted fix rather than re-scaffolding the frontend or backend from scratch.

---

## E. Git Checkpoint

Suggested checkpoint commits within this phase, in order:
1. `git commit -m "Phase 2: scaffold backend package structure, config, and database setup"`
2. `git commit -m "Phase 2: add Alembic foundation (no migrations yet)"`
3. `git commit -m "Phase 2: add health-check endpoint"`
4. `git commit -m "Phase 2: scaffold React + Vite + TypeScript frontend with Tailwind"`
5. `git commit -m "Phase 2: confirm frontend-backend health-check communication"`

After each commit, push to `origin main`. Before the final commit, re-run the full checklist in Section D to confirm nothing is broken, then commit and push the final Phase 2 state:
```bash
git add .
git commit -m "Phase 2 complete: architecture and foundation verified"
git push
```

Confirm `git status` reports a clean working tree afterward, and that `backend/.env` and `frontend/node_modules/` do not appear in the commit history.
