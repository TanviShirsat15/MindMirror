# MindMirror — Phase 2 Architecture & Foundation Notes

## Overview
Phase 2 establishes the running, connected architectural foundation for MindMirror:
- **FastAPI Backend**: Python package structure with centralized configuration (`pydantic-settings`), SQLAlchemy database session handling, and CORS middleware configured for `http://localhost:5173`.
- **Database Connection**: MySQL connectivity via `pymysql` configured through local environment variables (`.env`).
- **Alembic Migration Foundation**: Initialized and wired to dynamic database settings (`alembic current` verified; no migrations generated yet).
- **Health Check & Error Handling**: `GET /api/health` testing real DB connectivity, with a global exception handler logging server-side and returning generic 500 JSON without exposing internal stack traces.
- **Frontend Scaffolding**: React + Vite + TypeScript with Tailwind CSS, Recharts, and Lucide React.
- **Frontend-Backend Integration**: Vite development proxy configured for `/api -> http://localhost:8000`, with a placeholder UI in `App.tsx` displaying live system status and handled failure states.

## Local Development Startup

### 1. Start Backend
In terminal 1:
```powershell
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend
In terminal 2:
```powershell
cd frontend
npm run dev
```

Open `http://localhost:5173` to view the application status.
