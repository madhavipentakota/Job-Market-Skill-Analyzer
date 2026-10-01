# Job Market Skill Analyzer & Personalized Career Roadmap

A full-stack app that analyzes job-market data with NLP, identifies the skills companies
demand, compares them with a student's current skills, finds the gaps, and generates a
personalized learning roadmap.

**Flow:** Job Data → NLP Skill Extraction → Skill Demand Analysis → Skill Gap Analysis → Personalized Roadmap → Progress Tracking

> The bundled dataset (`data/jobs.csv`) is a small **demo/sample dataset**, clearly labeled
> as such in the UI. It is not a real market snapshot — swap in a larger CSV with the same
> columns to scale up. Skill percentages reflect coverage of *this dataset*, not a guarantee
> of employability.

---

## Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | React.js, React Router, Axios, Recharts, Lucide icons |
| Backend   | Python, FastAPI, Pydantic, Pandas, NumPy, Scikit-learn |
| Database  | SQLite (default, zero-config) / PostgreSQL (via `DATABASE_URL`) |
| ORM       | SQLAlchemy |

---

## Folder Structure

```
job-market-skill-analyzer/
├── frontend/                      # React app
│   ├── src/
│   │   ├── components/            # Sidebar.jsx, etc.
│   │   ├── pages/                 # One file per route (Home, Dashboard, ...)
│   │   ├── charts/                # (reserved for custom chart components)
│   │   ├── services/api.js        # Axios client — every backend call lives here
│   │   ├── hooks/                 # (reserved for custom React hooks)
│   │   ├── utils/                 # (reserved for frontend helpers)
│   │   ├── App.jsx                # Route definitions
│   │   └── main.jsx               # React entrypoint
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                       # FastAPI app
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, router registration
│   │   ├── database/db.py         # SQLAlchemy engine/session (SQLite/Postgres)
│   │   ├── models/models.py       # ORM tables: users, jobs, skills, roadmaps...
│   │   ├── schemas/schemas.py     # Pydantic request/response models
│   │   ├── routes/                # One file per resource (jobs, skills, roadmaps...)
│   │   ├── services/
│   │   │   ├── nlp/skill_extractor.py       # Dictionary-based skill detection + normalization
│   │   │   ├── analytics/skill_demand.py    # % of jobs requiring each skill, role comparison, combos
│   │   │   ├── analytics/skill_gap.py       # Current vs required skills → gap + readiness %
│   │   │   └── roadmap/
│   │   │       ├── roadmap_data.py          # Predefined roadmap templates (editable)
│   │   │       └── recommendation.py        # Combines demand + gap + roadmap order
│   │   └── utils/seed_data.py     # Loads CSV → runs NLP → populates DB + roadmaps
│   └── requirements.txt
│
├── data/
│   └── jobs.csv                   # Sample dataset (job_id, job_title, company, location,
│                                   #   experience, salary, job_description)
│
├── README.md
└── .env.example (in frontend/ and backend/)
```

---

## How the Core Logic Works (for your viva)

1. **NLP Skill Extraction** (`skill_extractor.py`): a controlled skill dictionary + an alias
   map (e.g. "ML" → "Machine Learning") is matched against each job description using
   whole-word regex, so extraction is transparent and easy to explain/extend — no black-box
   model required. It can later be swapped for spaCy's `PhraseMatcher` without touching
   any calling code.
2. **Skill Demand** (`skill_demand.py`): counts, per filtered set of jobs, how many mention
   each skill, divided by total jobs — nothing is hard-coded.
3. **Skill Gap** (`skill_gap.py`): takes the demand list for the target role, buckets each
   skill into *already have / missing / partially covered*, and flags *high priority* skills
   above a demand threshold. Readiness % = already-have ÷ (already-have + missing).
4. **Roadmap Engine** (`roadmap_data.py` + `roadmaps` routes): predefined, editable stage
   templates seeded into the DB — so roadmaps can be edited via the database without code
   changes after the first seed.
5. **Recommendation Engine** (`recommendation.py`): reorders the skill-gap's "missing" list
   to match the order skills first appear across the target role's roadmap stages, so
   prerequisite skills are recommended before advanced ones.

---

## Authentication

Basic email/password auth is implemented (`POST /api/auth/register`, `POST /api/auth/login`).
Passwords are hashed with PBKDF2-HMAC-SHA256 from Python's standard library (no fragile
third-party crypto dependency). There's no JWT/session cookie — login simply returns the
user's id, which the React app stores in `localStorage` and sends as `user_id` on
skill-save / progress calls. This is intentionally minimal for a college project; swap in
proper JWT/session auth before using this anywhere real.

Logging in is required to save current skills and to track roadmap progress — browsing
jobs, skill demand, role comparisons, and skill combinations works without an account.

## Setup Instructions

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # defaults to SQLite — no extra setup needed

# Seed the database from data/jobs.csv (creates tables + runs NLP extraction)
python -m app.utils.seed_data

# Run the API
uvicorn app.main:app --reload --port 8000
```

API docs (Swagger UI): **http://localhost:8000/docs**

### 2. Frontend (React)

```bash
cd frontend
npm install
cp .env.example .env              # points VITE_API_BASE_URL at the backend
npm run dev
```

App: **http://localhost:5173**

### 3. Using PostgreSQL instead of SQLite

In `backend/.env`, uncomment and set:

```
DATABASE_URL=postgresql://user:password@localhost:5432/job_market_db
```

Create the database first (`createdb job_market_db`), then re-run
`python -m app.utils.seed_data`.

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Log in, returns `user_id` |
| GET  | `/api/jobs` | List jobs, filterable by role/location/experience/skill/company/search |
| GET  | `/api/jobs/{id}` | Single job detail |
| GET  | `/api/roles` | Distinct job titles in the dataset |
| GET  | `/api/locations` | Distinct locations |
| GET  | `/api/skills` | Master skill list |
| GET  | `/api/skills/demand` | % of jobs requiring each skill (filterable) |
| GET  | `/api/skills/combinations` | Top co-occurring skill pairs |
| POST | `/api/roles/compare` | Skill-demand comparison across 2+ roles |
| POST | `/api/skill-gap` | Compare current skills vs a target role's requirements |
| GET  | `/api/roadmaps` | All roadmap templates |
| GET  | `/api/roadmaps/{role}` | One roadmap's full stage list |
| POST | `/api/user/skills` | Save a user's current skills |
| GET  | `/api/user/progress` | A user's stage-by-stage progress + overall % |
| POST | `/api/user/progress` | Mark a stage not_started / in_progress / completed |
| GET  | `/api/recommendations` | Prioritized "learn next" skill list |

Full interactive documentation is auto-generated at `/docs` once the backend is running.

---

## Database Tables

`users`, `jobs`, `skills`, `job_skills`, `career_roadmaps`, `roadmap_stages`,
`user_skills`, `user_progress` — see `backend/app/models/models.py` for full schema
and relationships.

---

## Extending the Project

- **Bigger dataset:** replace `data/jobs.csv` with a larger file using the same columns,
  delete the local `job_market.db`, and re-run the seed script.
- **More skills:** add entries to `SKILL_DICTIONARY` / `NORMALIZATION_MAP` in
  `skill_extractor.py` — the whole pipeline (extraction, demand, gap, recommendations)
  picks them up automatically.
- **More roadmaps:** add a new dict to `roadmap_data.py` following the existing stage
  structure and append it to `ALL_ROADMAPS`.
- **Authentication:** the backend already models `users` and scopes `user_skills` /
  `user_progress` by `user_id`, so JWT-based login can be layered on
  (`python-jose` is already in `requirements.txt`) without restructuring the schema.

---

## Notes & Honesty Constraints

- All analytics (skill %, comparisons, combinations, readiness) are **computed from the
  dataset currently in the database** — nothing is hard-coded.
- The app does **not** claim to predict whether a person will get hired.
- Demo data is labeled as such in the UI (`is_demo_data` flag on each job) and should not
  be presented as representing the full real-world job market.
