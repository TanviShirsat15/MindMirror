# MindMirror: AI-Based Personal Well-Being and Habit Intelligence System

MindMirror is a secure, web-based personal self-reflection and behavioral analytics application. Users maintain free-form journal entries and a customizable habit tracker. Natural Language Processing extracts numerical signals (sentiment, stress indicators, positive emotion, and related textual signals) from journal text, while the habit tracker produces behavioral metrics such as completion and consistency. These two signal streams are fused through a Mamdani Fuzzy Inference System to produce an interpretable, application-level Well-Being Index (1–100). The system builds a personal baseline over time, compares current results against that baseline, surfaces daily/weekly/monthly trends, and generates explainable, non-causal self-reflection insights.

> **Disclaimer**: MindMirror is explicitly not a diagnostic, therapeutic, or clinical tool. It does not perform mental-health diagnosis, does not offer chatbot counseling, and does not provide emergency intervention.

## Development & Roadmap

MindMirror development follows a structured, sequential phased implementation plan:

- **Phase 0**: Project Specification & Source of Truth
- **Phase 1**: Development Environment & GitHub Setup *(Completed)*
- **Phase 2**: Project Architecture & Foundation *(Completed)*
- **Phase 3+**: Core Models, Authentication, and Feature Modules

Full documentation is tracked within the [`docs/`](./docs) directory.

---

## Development & Startup Commands

Run the backend and frontend in separate terminals during development:

### Backend

```powershell
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

The backend health check is accessible at `http://localhost:8000/api/health`.

### Frontend

```powershell
cd frontend
npm run dev
```

Visiting the frontend development server at `http://localhost:5173` will display the health-check placeholder and confirm live connectivity with the backend and MySQL database.
