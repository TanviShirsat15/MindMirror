# MindMirror — Phase 1 Implementation Plan
## Development Environment & GitHub Setup

*Prerequisite: Phase 0 Specification (approved, source of truth). This document does not repeat Phase 0 content and does not implement any project code.*

**Global rule in effect for this phase and every phase after it:**
> If any error, bug, dependency problem, configuration issue, or unexpected behavior occurs, do not rebuild the entire project. Identify the specific problem and make only the necessary targeted fix. Do not modify working features or unrelated parts of the project. Preserve all existing functionality.

---

## A. Phase Objective

Set up a clean, correct, beginner-safe Windows development environment and an initialized Git/GitHub repository for MindMirror, with the exact top-level folder structure required by Phase 0's architecture (`frontend/`, `backend/`, `docs/`, `.gitignore`, `README.md`). At the end of this phase, no application code exists yet — only the environment, tooling, folder skeleton, and a version-controlled repository ready for the next phase. No unnecessary technologies (no MongoDB, Firebase, Redis, Docker, Kubernetes, TensorFlow, PyTorch, LangChain, OpenAI API) are introduced, since none are required by the approved spec.

This document is the instruction set Antigravity executes to carry out Phase 1 itself. Phases are executed sequentially, starting with this one — Phase 1 is not preparatory instructions for a human to hand off later; it is the phase currently being implemented.

### A.1 — What Phase 1 Does NOT Include

Phase 1 establishes the environment, repository, folder structure, documentation, virtual environment, `.gitignore`, README, and initial GitHub checkpoint only. Phase 1 must **not**:
- create the React/Vite application
- create FastAPI application code
- create SQLAlchemy models
- create database schemas or tables
- implement authentication
- implement journal functionality
- implement habit functionality
- implement NLP
- implement the Mamdani Fuzzy Inference System
- implement analytics
- implement dashboard functionality
- implement insights

Any of the above belongs to a later phase. If Antigravity finds itself writing code that does any of these things while executing this document, it should stop and treat that as outside this phase's scope.

---

## B. Prerequisites

- A Windows PC (Windows 10 or 11) with administrator access
- A working internet connection
- A GitHub account with access to the existing MindMirror repository (`https://github.com/TanviShirsat15/MindMirror`)
- At least ~5 GB free disk space (Node.js, Python, MySQL, and dependencies combined)
- No prior full-stack experience required — every step below is written for a first-time setup

---

## C. Required Software and Why Each Is Needed

| Software | Why it's needed |
|---|---|
| **Node.js (LTS)** | Runs the React/Vite/TypeScript frontend tooling (npm, Vite dev server, build process) |
| **Python 3.11+** | Runs the FastAPI backend, the NLP pipeline, and the scikit-fuzzy inference engine |
| **MySQL** | The project's database, storing users, journals, habits, and computed indices per Phase 0 |
| **Git** | Version control — required as an ongoing safety mechanism across all phases |
| **GitHub repository (already created: `https://github.com/TanviShirsat15/MindMirror`)** | Remote backup, checkpointing, and history for the project |
| **A code editor (VS Code recommended)** | Editing code and running integrated terminals; Antigravity will operate within this kind of environment |
| **Antigravity** | The AI development agent executing this Phase 1 plan, and every approved phase after it, inside this repository |

No other services are required. Do not install Docker, MongoDB, Redis, Firebase, or any ML framework beyond what Phase 0 specifies (scikit-fuzzy, standard Python NLP tooling) — none of these have a concrete requirement in the approved specification.

Before installing anything in Section D, check whether it is already present on the system. Install only what's missing, then verify. Do not reinstall or reconfigure software that is already correctly installed, and avoid unnecessary system-level changes.

---

## D. Exact Setup Sequence

### D.1 — Recommended Windows Development Environment
- Use **native Windows** (not WSL) for simplicity at this stage, since the developer is a beginner and Phase 0 does not require Linux-only tooling.
- Install and use **Visual Studio Code** as the primary editor — it is free, has strong Python/TypeScript support, and is a common environment for AI coding agents like Antigravity to operate in.
- Use **PowerShell** (or the terminal built into VS Code) for all commands below.

### D.2 — Node.js Setup
1. **Check first:** open a terminal and run `node -v` and `npm -v`. If both return version numbers (Node 18 or newer is fine), Node.js is already correctly installed — skip to Verify (step 4) and do not reinstall.
2. If missing or outdated, go to https://nodejs.org and download the **LTS** version for Windows, then run the installer, accepting defaults (this also installs `npm`).
3. Restart any open terminal windows after installation.
4. Verify with the commands in Section E.

### D.3 — Python Setup
1. **Check first:** run `python --version` and `pip --version`. If Python 3.11 or newer is already installed and on PATH, skip to Verify (step 4) and do not reinstall.
2. If missing or outdated, go to https://www.python.org/downloads/ and download **Python 3.11 or newer** for Windows. During installation, **check the box "Add python.exe to PATH"** before clicking Install — this is the single most common beginner mistake (see Section G). Complete installation with default options otherwise.
3. If Python is already installed but not on PATH, do not reinstall — instead re-run the installer, choose "Modify," and enable "Add python.exe to PATH" (see Section G).
4. Verify with the commands in Section E.

### D.4 — MySQL Setup
1. **Check first:** run `mysql --version`. If MySQL is already installed, confirm the service is running (see Section E) and identify the existing root credentials before doing anything else — do not reinstall over an existing instance.
2. If missing, go to https://dev.mysql.com/downloads/installer/ and download MySQL Installer for Windows. Run it and choose the "Server only" (or "Developer Default") setup type. When prompted:
   - Set and remember a password for the `root` user.
   - Keep the default port `3306`.
   - Use the default authentication method offered by the installer.
3. After installation (or against an existing installation), use **MySQL Workbench** (installed alongside MySQL) or the `mysql` command line to create a dedicated database for the project, e.g. `mindmirror_db`, and a dedicated database user with privileges scoped to that database, rather than using the `root` user directly.
4. Keep the database name, username, and password noted somewhere private (these will later go into a `.env` file — never into source code or Git).
5. **Scope boundary:** this step only creates the empty database and a database user, and verifies the connection works. It does not create any application tables, SQLAlchemy models, Alembic migrations, or schema — that work belongs to the phase where the backend is built.

### D.5 — Git Setup
1. **Check first:** run `git --version`. If Git is already installed, skip installation and go straight to setting your identity (step 3) if it isn't already configured.
2. If missing, go to https://git-scm.com/download/win and download Git for Windows, then run the installer with default options (default options are fine for a beginner).
3. Set your identity (used for every commit) if not already set — check first with `git config --global user.name` and `git config --global user.email`; only set them if they come back empty:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"
   ```
4. Verify with the commands in Section E.

### D.6 — GitHub Setup (Repository Already Created)
1. The required GitHub repository already exists: `https://github.com/TanviShirsat15/MindMirror` — this step connects the local project to it, it does not create a new repository.
2. Confirm you can access the repository in a browser and note whether it currently has any commits (it should be empty or near-empty at this stage).
3. Note the repository's HTTPS (or SSH) URL for use in D.11: `https://github.com/TanviShirsat15/MindMirror.git`
4. Authenticate Git with GitHub the first time you push (Git for Windows will prompt a browser-based sign-in, or you can set up a Personal Access Token — either is fine for a beginner).

### D.7 — Recommended Project Location on the Windows PC
- The standardized project location is: `C:\Dev\MindMirror`
- If `C:\Dev` doesn't exist, create it first. This keeps the path short (helps avoid Windows path-length issues) and keeps development work separate from personal documents.
- Create the project **outside** any cloud-synced folder that auto-syncs file-by-file (avoid OneDrive-synced Desktop/Documents if possible, since large `node_modules` folders and file locks can cause sync conflicts and slowdowns).
- An equivalent short, non-cloud-synced path is acceptable **only if `C:\Dev\MindMirror` genuinely cannot be used** on this machine (e.g., a permissions restriction). If a different path is used, it must be used consistently for every command and reference in this document from that point on — do not mix paths.

### D.8 — Exact Initial Project Folder Structure
Create this exact structure under `C:\Dev\MindMirror`:
```
MINDMIRROR/
├── frontend/
├── backend/
├── docs/
├── .gitignore
└── README.md
```
- `frontend/` — will later hold the React + Vite + TypeScript app (Phase 2+)
- `backend/` — will later hold the FastAPI app, including its own Python virtual environment (Phase 2+)
- `docs/` — holds the Phase 0 specification and this Phase 1 plan, plus any future phase documents, so the whole project history lives in the repo
- `.gitignore` — see Section on Initial `.gitignore` Requirements below
- `README.md` — a short project description (title, one-paragraph summary from Phase 0, and a note that development follows a phased plan)

No files inside `frontend/` or `backend/` are created in this phase — they exist as empty folders only. Git does not track empty folders by default; to make Git aware of them at this stage, add a placeholder file such as `.gitkeep` inside each (e.g., `frontend/.gitkeep`, `backend/.gitkeep`), to be removed once real files land in Phase 2.

### D.9 — How Antigravity Should Open/Work with the Project
- Antigravity should be pointed at the **root folder** `C:\Dev\MindMirror` as its working directory/workspace — not at `frontend/` or `backend/` individually — so it has full visibility of:
  - `frontend/`
  - `backend/`
  - `docs/`
  - `.gitignore`
  - `README.md`
- Before Antigravity begins Phase 1 work, it should be given: (a) the approved Phase 0 specification, (b) this Phase 1 plan, and (c) the global fix-forward rule, so every action in this phase — and every phase after it — is scoped against approved documents rather than improvised.
- Antigravity should be instructed to make small, targeted commits as it works (see Section F) rather than large, sweeping, multi-feature commits.

### D.10 — How Git Repository Initialization Works
From inside `C:\Dev\MindMirror` (via terminal):
```
git init
```
This creates a hidden `.git` folder that turns the directory into a Git repository. Nothing is committed yet — `git init` only starts tracking capability; it does not save any files until you explicitly `add` and `commit` them.

### D.11 — How the Local Repository Connects to GitHub
1. Link the local repo to the existing GitHub repository noted in D.6:
   ```
   git remote add origin https://github.com/TanviShirsat15/MindMirror.git
   ```
2. Confirm the link:
   ```
   git remote -v
   ```
3. Before pushing, check whether the GitHub repository already has any commits (e.g., an auto-created README) by running:
   ```
   git fetch origin
   ```
   If `origin/main` exists with commits, pull it first with `git pull origin main --allow-unrelated-histories` and resolve any conflict, rather than force-pushing over it.
4. The first push (after the initial commit in Section H) will look like:
   ```
   git branch -M main
   git push -u origin main
   ```
   The `-u` flag links your local `main` branch to GitHub's `main` branch so future pushes can simply use `git push`.

### D.12 — Initial `.gitignore` Requirements
The `.gitignore` file at the project root must, at minimum, exclude:
```
# Python
backend/venv/
backend/__pycache__/
backend/**/__pycache__/
*.pyc

# Environment/secrets
.env
backend/.env
frontend/.env

# Node
frontend/node_modules/
frontend/dist/

# Editor/OS
.vscode/
.idea/
.DS_Store
Thumbs.db

# Logs
*.log
```
This is critical because Phase 0's security requirements state that secrets must live in environment variables and never be committed — `.env` files must never reach GitHub. `node_modules/` and Python virtual environments are excluded because they are large, machine-specific, and regenerable from `package.json`/`requirements.txt` rather than something to version-control.

### D.13 — Python Virtual Environment Requirements
The backend must use an isolated Python virtual environment so its dependencies never mix with system-wide Python packages.
1. From inside `backend/`:
   ```
   python -m venv venv
   ```
2. Activate it (Windows PowerShell):
   ```
   venv\Scripts\Activate.ps1
   ```
   (If PowerShell blocks script execution, see Section G.)
3. Once activated, the terminal prompt should show `(venv)` — this confirms the virtual environment is active before installing any Python packages.
4. The `venv/` folder itself is excluded via `.gitignore` (Section D.12) — only a `requirements.txt` (created in a later phase, once backend dependencies exist) is committed.

---

## E. Verification Checklist

Run each command and confirm the expected output before moving on:

| Step | Command | Expected Output |
|---|---|---|
| Node.js installed | `node -v` | A version number, e.g. `v20.x.x` |
| npm installed | `npm -v` | A version number, e.g. `10.x.x` |
| Python installed | `python --version` | `Python 3.11.x` (or newer) |
| pip installed | `pip --version` | A pip version tied to your Python install |
| Git installed | `git --version` | `git version 2.x.x` |
| Git identity set | `git config --global user.name` and `git config --global user.email` | Your configured name and email print back |
| MySQL installed | `mysql --version` | A MySQL version string |
| MySQL service running | Open MySQL Workbench and connect, or run `mysql -u root -p` and enter your password | Successful connection / `mysql>` prompt |
| Repo initialized | `git status` (from `C:\Dev\MindMirror`) | `On branch main` / `No commits yet` (or similar) |
| Remote linked | `git remote -v` | Shows `origin` pointing to your GitHub URL (fetch and push) |
| venv working | With `(venv)` active, run `python -m pip list` | A short list with just `pip` and `setuptools` (nothing extra yet) |

If any command is "not recognized," see Section G before proceeding further.

---

## F. Git/GitHub Checkpoint Strategy

Git/GitHub is treated as an **ongoing safety mechanism**, not a one-time setup step. Going forward:

- **Create a checkpoint commit whenever a discrete, working unit of progress is reached** — e.g., "backend environment created and verified," "frontend scaffolding runs successfully," "database connection confirmed working." Never wait until an entire phase is "fully done" to commit — commit at each stable, working milestone within a phase.
- **Never commit broken/non-running code as a checkpoint.** A checkpoint should represent a state you could safely return to.
- **Before attempting any risky or exploratory change** (e.g., trying a new library, restructuring a folder, upgrading a dependency), commit the current working state first, so the fix-forward rule can be honored: if something breaks, you roll back to the last checkpoint and apply a targeted fix instead of rebuilding.
- Use short, descriptive commit messages that state what changed and why (e.g., `git commit -m "Add backend/frontend/docs folder skeleton and .gitignore"`), not generic messages like "update."
- Push to GitHub after every meaningful checkpoint commit, not just at the end of a session — this ensures the remote repository is always close to your local safety net.

---

## G. Common Beginner Errors and Targeted Fixes

| Error | Cause | Targeted Fix (do not rebuild anything) |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python wasn't added to PATH during install | Re-run the Python installer, choose "Modify," and enable "Add python.exe to PATH"; restart terminal |
| `'node' is not recognized...` | Terminal opened before Node.js install finished, or PATH not refreshed | Close and reopen the terminal (or restart VS Code); reinstall Node.js if it persists |
| `running scripts is disabled on this system` (when activating venv) | PowerShell's default execution policy blocks script activation | Run PowerShell as Administrator once and execute: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry activation |
| `ERROR 2003 (HY000): Can't connect to MySQL server` | MySQL service isn't running, or wrong port/credentials | Check the MySQL service is running in Windows Services (`MySQL80` or similar); confirm port `3306` and the root/user password set during install |
| `fatal: remote origin already exists` | `git remote add origin` was run twice | Run `git remote set-url origin <url>` instead of adding it again — do not delete and reinitialize the repo |
| `fatal: refusing to merge unrelated histories` on first push | The existing GitHub repository already has a commit (e.g., an auto-created README) that predates your local history | Pull once with `git pull origin main --allow-unrelated-histories` and resolve the single conflict — do not delete the existing repository or your local work |
| `.env` accidentally committed | `.gitignore` was added after the first commit, or `.env` was already tracked | Add `.env` to `.gitignore`, then run `git rm --cached .env` to untrack it (without deleting the file locally); commit that targeted fix |
| `npm error` about missing `package.json` | Trying to run `npm` commands before the frontend app is scaffolded (Phase 2) | Not an error at this stage — `frontend/` is intentionally empty until Phase 2; no fix needed yet |

In every case above: fix only the specific misconfiguration named — do not delete and recreate the whole project, environment, or repository unless the table explicitly says to.

---

## H. Initial Git Commit Strategy

1. Stage and make the first commit only once the folder skeleton, `.gitignore`, and `README.md` exist:
   ```
   git add .
   git commit -m "Initial project skeleton: frontend, backend, docs folders, .gitignore, README"
   ```
2. Push this first commit to GitHub as described in Section D.11.
3. After pushing, run `git status` and confirm it reports a clean working tree — this confirms Phase 1 ends in a clean, verified repository state.
4. This first commit is the **baseline checkpoint** for the entire project — everything in later phases builds forward from it, and it's the fallback point if scaffolding in the next phase needs to be rolled back.
5. From here on, follow the checkpoint strategy in Section F for every subsequent phase.

---

## Completion Criteria

Phase 1 is complete when **all** of the following are true:
- [ ] Required development tools (Node.js, Python, MySQL, Git) are installed and verified per Section E — pre-existing installations were checked and reused rather than blindly reinstalled
- [ ] Git is configured with a user identity
- [ ] The local project is connected to the existing GitHub repository (`https://github.com/TanviShirsat15/MindMirror`) as the `origin` remote
- [ ] The project root exists at `C:\Dev\MindMirror` (or the documented equivalent, used consistently)
- [ ] `frontend/`, `backend/`, and `docs/` exist at the project root
- [ ] The approved Phase 0 specification is stored in `docs/`
- [ ] This Phase 1 plan is stored in `docs/`
- [ ] `.gitignore` exists at the project root and correctly excludes secrets (`.env`), virtual environments (`venv/`), `node_modules/`, build output (`dist/`), and editor/OS files
- [ ] `README.md` exists at the project root
- [ ] `backend/venv` exists and activates successfully
- [ ] The local Git repository is initialized, the initial project skeleton is committed, and that commit has been pushed to GitHub's `main` branch
- [ ] `git status` shows a clean working tree (nothing uncommitted, nothing untracked that should be tracked)
- [ ] A MySQL database and dedicated database user exist and the connection has been verified — with no application tables, SQLAlchemy models, migrations, or schema created
- [ ] No application functionality has been implemented — no React/Vite app, no FastAPI code, no authentication, journal, habit, NLP, fuzzy inference, analytics, dashboard, or insight functionality
- [ ] No technologies beyond those listed in Section C have been introduced
- [ ] Antigravity understands and will follow the checkpoint commit strategy for every phase that follows

At this point, the project has a clean, verified, version-controlled foundation, ready for the next approved phase.
