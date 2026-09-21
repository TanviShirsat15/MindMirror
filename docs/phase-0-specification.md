# MindMirror: AI-Based Personal Well-Being and Habit Intelligence System
## Phase 0 Project Specification — Source of Truth

### 1. Final Project Definition
MindMirror is a secure, web-based personal self-reflection and behavioral analytics application. Users maintain free-form journal entries and a customizable habit tracker. Natural Language Processing extracts numerical signals (sentiment, stress indicators, positive emotion, and related textual signals) from journal text, while the habit tracker produces behavioral metrics such as completion and consistency. These two signal streams are fused through a Mamdani Fuzzy Inference System to produce an interpretable, application-level Well-Being Index (1–100). The system builds a personal baseline over time, compares current results against that baseline, surfaces daily/weekly/monthly trends, and generates explainable, non-causal self-reflection insights.

MindMirror is explicitly not a diagnostic, therapeutic, or clinical tool. It does not perform mental-health diagnosis, does not offer chatbot counseling, and does not provide emergency intervention.

### 2. Problem Statement
People generate a large amount of unstructured personal data every day — journal entries, thoughts, moods — and separately track habits like sleep, exercise, or study, but rarely connect the two. Without a structured way to combine subjective reflection (what someone writes) with objective behavior (what someone does), it is hard to notice patterns, build self-awareness, or track well-being trends over time. Most existing tools either handle journaling or habit tracking, and few explain their scoring in an interpretable way. MindMirror addresses this gap by combining NLP-derived emotional signals with habit-based behavioral metrics through an explainable fuzzy logic engine, producing a transparent, personalized well-being indicator rather than a black-box score.

### 3. Objectives
1. Allow users to securely register, log in, and maintain private journal entries of any length.
2. Extract meaningful NLP-based signals (sentiment, stress indicators, positive emotion, etc.) from journal text.
3. Allow users to define and manage a fully customizable set of habits with targets.
4. Compute behavioral metrics (completion/consistency) from habit-tracking data.
5. Fuse NLP signals and habit metrics using a Mamdani Fuzzy Inference System to produce a 1–100 Well-Being Index.
6. Establish a personal historical baseline per user and compare current results against it.
7. Present daily, weekly, and monthly trends of the Well-Being Index and its contributing factors.
8. Generate explainable, pattern-based insights without asserting unproven causal claims.
9. Ensure the system is secure, since journal content is sensitive personal data.
10. Keep the scope realistic and achievable for a student mini-project team while remaining syllabus-relevant.

### 4. Target User and Use Case
**Target user**: An individual who wants a private, structured way to reflect on their emotional state and daily habits without using a clinical or therapy-branded product — e.g., a student or working professional interested in self-improvement and self-awareness.

**Primary use case**:
1. User logs in and writes a journal entry reflecting on their day (any length — one line or several paragraphs).
2. User logs habit completion for the day against their custom habit list (e.g., exercise: 30 min, sleep: 7 hrs, water: 2L).
3. The system processes the entry through NLP and combines it with the day's habit metrics via the fuzzy engine to generate a Well-Being Index.
4. The user views their current index alongside their personal baseline and recent trend.
5. Over days/weeks, the user reviews trend charts and reads explainable insights (e.g., "on days you log 7+ hours of sleep, your average sentiment score has tended to be higher") that are framed as observed associations, not medical or causal claims.

### 5. Core Features
- Secure user registration and authentication
- Unlimited journal entries, no fixed word minimum/maximum, no entry-count limit
- Free-form journal length (single sentence to multiple paragraphs)
- NLP-based extraction of sentiment, stress-related indicators, positive emotion, and other appropriate textual signals
- Fully customizable habit tracker (add/edit/rename/delete habits; user-defined targets)
- Behavioral metric computation (completion rate, consistency)
- Mamdani Fuzzy Inference System combining NLP + habit signals
- Well-Being Index (1–100) generation, clearly labeled as a self-reflection index
- Personal baseline construction over historical data
- Comparison of current results against personal baseline
- Daily/weekly/monthly trend views
- Explainable, non-causal, pattern-based insight generation
- Data security measures appropriate for sensitive personal journal content
- Data export/deletion functionality where practical

### 6. MVP Features
- User registration, login, logout (secure password hashing, session/token-based auth)
- Journal entry creation, editing, deletion, and listing (no word limits)
- Basic NLP pipeline producing at minimum: sentiment score and one additional signal (e.g., stress indicator or positive-emotion score)
- Customizable habit tracker: add, edit, rename, delete habits; set a target per habit; log daily completion
- Basic behavioral metrics: completion rate and simple consistency measure (e.g., rolling streak or % of target met)
- Mamdani Fuzzy Inference System with a small, well-justified set of input variables (e.g., sentiment, stress indicator, habit completion) and membership functions producing the 1–100 Well-Being Index
- Storage and display of the day's Well-Being Index
- Simple historical baseline (e.g., rolling average over available history) and a "current vs. baseline" comparison
- Basic trend visualization (line chart of Well-Being Index over time; daily view minimum, weekly/monthly as stretch)
- Minimal explainable insight output (e.g., which input variable most influenced today's score, or a simple observed-pattern statement over the available history)
- Core security baseline: password hashing (Argon2id), input validation, per-user data isolation/authorization, environment-variable-based secrets, basic CORS configuration

### 7. Explicitly Out of Scope for MVP
- Multiple/advanced NLP models beyond a small justified set (e.g., no ensemble of transformer models)
- Deep learning components (CNN, LSTM, Transformer-based fine-tuning) unless a specific syllabus requirement justifies one narrowly scoped addition
- Reinforcement learning or any adaptive/self-updating fuzzy rule learning
- Chatbot, conversational AI, or any counseling/coaching dialogue interface
- Any medical, clinical, diagnostic, or therapeutic claims or functionality
- Emergency intervention, crisis detection, or escalation features
- Third-party integrations (wearables, calendar sync, social sharing/community features)
- Multi-language NLP support (assume single-language input for MVP, e.g., English)
- Mobile native apps (web-responsive only)
- Advanced personalization such as per-user fuzzy rule tuning or ML-based rule weight learning
- Notifications/reminders system beyond what's trivially needed
- Team/social/comparison features between users
- Extensive admin dashboards or multi-tenant organization features

### 8. AI/DS Components
- **NLP module**: Extracts structured numerical features from unstructured journal text (sentiment polarity, stress-related lexical/pattern indicators, positive-emotion indicators, and any additional signals that are well-justified and explainable).
- **Fuzzy Inference module**: A Mamdani-type Fuzzy Inference System (using `scikit-fuzzy`) that takes NLP-derived signals and habit-derived behavioral metrics as crisp inputs, fuzzifies them via defined membership functions, applies a rule base, and defuzzifies to produce the 1–100 Well-Being Index.
- **Baseline/trend analytics**: Statistical summarization (via pandas/NumPy) of historical index values and component signals to build a rolling personal baseline and generate trend data for visualization.
- **Insight generation**: Rule-based or statistically-derived explanatory statements describing observed associations between inputs and the index, explicitly avoiding causal language unless scientifically supported.

The AI/DS scope is deliberately restricted to NLP and Fuzzy Logic; CNN/LSTM/Transformer fine-tuning/Reinforcement Learning/external LLM APIs are excluded unless a specific, syllabus-justified reason is identified and separately agreed on.

### 9. Role of NLP
NLP's role is limited to feature extraction, not generation or conversation. Given a journal entry's text, the NLP pipeline outputs a small set of interpretable numerical signals (e.g., a sentiment score, a stress indicator, a positive-emotion score). These signals become crisp inputs to the fuzzy inference system. NLP does not make well-being judgments itself — it only quantifies textual signal, which the fuzzy system then interprets.

### 10. Role of Fuzzy Logic
The Mamdani Fuzzy Inference System is the core reasoning engine that fuses heterogeneous inputs (subjective NLP-derived signals and objective habit-derived metrics) into a single interpretable output. Fuzzy logic is chosen specifically because:
- It handles imprecise, human-centric concepts (e.g., "moderately stressed," "highly consistent") naturally via linguistic membership functions.
- It is inherently explainable — each rule firing can be traced and reported, unlike a black-box ML model.
- It avoids requiring large labeled training datasets, which are impractical for a personal well-being index in a student project timeframe.

The fuzzy system's rule base and membership functions are the primary "intelligence" of the scoring mechanism and should be designed collaboratively and documented clearly, since they directly determine explainability.

### 11. Role of Personalization
Personalization in MindMirror centers on the user's own historical data, not on adapting the model itself. Specifically:
- Users fully customize their own habit list, targets, and tracking cadence.
- Each user's baseline is built solely from their own history — there is no cross-user comparison or population norming in MVP.
- The "current vs. baseline" comparison is inherently personalized: the same signal values could be interpreted differently for two different users depending on each user's own historical range.
- Adaptive/self-tuning fuzzy rules per user are explicitly out of MVP scope (see Section 7), keeping personalization data-driven rather than model-driven.

### 12. Role of Analytics
Analytics covers baseline construction, trend computation, and insight generation:
- **Baseline construction**: rolling statistical summary (e.g., rolling mean/median) of historical Well-Being Index and component signals.
- **Trend analysis**: aggregation of index and signal values into daily/weekly/monthly views for visualization (via Recharts on the frontend).
- **Insight generation**: identifying and reporting observed associations between habit/journal signals and the Well-Being Index over the user's own history, explicitly framed as descriptive/associative rather than causal, unless a claim is scientifically well-established.

### 13. Security Requirements
- Secure password hashing using Argon2id
- Authentication (login/session or token-based) and authorization (per-user access control)
- Environment variables for all secrets/config (no hardcoded credentials)
- Input validation on all endpoints, especially journal text and habit data
- Proper CORS configuration restricting allowed origins
- User-level data authorization: a user can only ever access their own journal entries, habits, and indices
- No sensitive journal content written to application logs
- HTTPS required for any deployed environment
- Rate limiting on sensitive endpoints (login, registration, password reset)
- Data export and data deletion functionality implemented where practical, given personal data sensitivity

### 14. Important Limitations
- The Well-Being Index is an application-level self-reflection index, not a medical, clinical, or psychologically validated measurement.
- The system must not claim to diagnose, treat, or assess any mental health condition.
- Insights must avoid causal language ("X causes Y") unless there is scientific justification; default framing should be associative/descriptive ("on days with X, Y has tended to be higher/lower for you").
- NLP sentiment/stress extraction is approximate and can misinterpret nuance, sarcasm, or context — this should be acknowledged as a system limitation.
- The fuzzy system's accuracy depends entirely on the quality of its manually designed membership functions and rule base, not on learned patterns from large datasets.
- Baseline quality improves with more historical data; early-stage users will have limited/noisy baselines.
- No crisis-detection or emergency-response capability exists; the system must not imply it can identify or respond to a mental health emergency.

### 15. Syllabus Mapping
Framed for a course such as **Artificial Intelligence and Data Science – II**, the project maps to:
- **NLP / Text Processing**: feature extraction from unstructured journal text (sentiment, stress, emotion indicators)
- **Fuzzy Logic / Fuzzy Inference Systems**: Mamdani-type FIS design — fuzzification, rule base, inference, defuzzification
- **Data Analytics**: baseline/trend computation, time-series style aggregation, descriptive statistics
- **Software Engineering practices**: secure full-stack application development, database design (MySQL/SQLAlchemy/Alembic), API design (FastAPI), version control (Git/GitHub)
- **Human-Centered/Explainable AI**: emphasis on interpretability of the fuzzy system and non-causal, transparent insight generation

This mapping should be adapted to whatever the actual syllabus document specifies, but the AI/DS core (NLP + Fuzzy Logic) is intentionally the anchor, since it is the most directly syllabus-relevant and scoped-appropriate combination for a team of 3–4 students.

### 16. High-Level System Data Flow
```
User
│
├──> Journal Entry (free text, any length)
│    │
│    ▼
│    NLP Feature Extraction
│    (sentiment, stress indicator, positive emotion, etc.)
│
├──> Custom Habit Tracker
│    │
│    ▼
│    Habit Metric Computation
│    (completion rate, consistency)
│
▼
NLP Signals + Habit Metrics
│
▼
Mamdani Fuzzy Inference System
│
▼
Well-Being Index (1–100)
│
▼
Personal Baseline Update
│
▼
Historical Trend Aggregation (daily/weekly/monthly)
│
▼
Explainable Insight Generation
│
▼
User-Facing Dashboard (index, trends, insights)
```

### 17. High-Level Architecture
- **Frontend**: React + Vite + TypeScript + Tailwind CSS, charts via Recharts, icons via Lucide React. Responsible for journal entry UI, habit tracker UI, dashboard visualizations (current index, baseline comparison, trends), and insight display.
- **Backend**: Python + FastAPI, exposing REST endpoints for auth, journal CRUD, habit CRUD, index computation, and analytics/trends. Hosts the NLP pipeline and the fuzzy inference engine (`scikit-fuzzy`), and orchestrates the baseline/trend computation (`pandas`/`NumPy`).
- **Database**: MySQL, managed via SQLAlchemy ORM and Alembic migrations. Stores users, journal entries, habits, habit logs, computed NLP signals, computed Well-Being Index history, and baseline data.
- **Security layer**: Argon2id password hashing, authentication/authorization middleware, environment-based secret management, input validation, CORS policy, rate limiting on sensitive endpoints — all implemented at the FastAPI layer.
- **Data flow between layers**: Frontend calls FastAPI REST endpoints → FastAPI validates/authenticates → business logic (NLP + fuzzy inference + analytics) executes → results persisted to MySQL via SQLAlchemy → response returned to frontend for visualization.

### 18. Development Boundaries (Keeping the Project Realistic)
- Limit AI/DS scope strictly to NLP feature extraction + Mamdani Fuzzy Inference; do not add deep learning, RL, or external LLM APIs unless a specific, agreed, syllabus-justified reason arises.
- Keep the NLP pipeline to a small, well-understood, explainable feature set rather than an exhaustive signal list.
- Keep the fuzzy rule base small and well-documented (a handful of input variables, clearly defined membership functions) rather than attempting an overly complex rule set.
- Treat MVP feature list (Section 6) as the actual build target; treat Section 5's full feature list as the north star for post-MVP iterations only if time allows.
- Avoid scope creep into clinical, therapeutic, or crisis-related functionality under any circumstances.
- Avoid building custom infrastructure (e.g., custom auth systems beyond standard, well-known libraries/patterns) where a standard, secure, well-documented approach exists.
- Favor incremental, testable delivery over big-bang implementation across all future phases.

### Global Development Rule (Applies to All Future Phases)
> If any error, bug, dependency problem, configuration issue, or unexpected behavior occurs, do not rebuild the entire project. Identify the specific problem and make only the necessary targeted fix. Do not modify working features or unrelated parts of the project. Preserve all existing functionality.

### Version Control Requirement (Applies to All Future Phases)
> Git/GitHub usage is a mandatory, ongoing requirement across all future development phases — every phase's work should be committed with clear, incremental commit history.

This document is the Phase 0 source of truth for MindMirror. No implementation has occurred at this stage — this specification is intended to guide and be referenced by all subsequent development phases.
