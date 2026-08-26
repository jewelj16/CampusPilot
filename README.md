# CampusPilot

A campus mess + student-life platform. This repo is **Phase 1**: a complete
UI for mess registration, backed by a dummy (in-memory) API. No database,
no auth, no AI yet — those come in later milestones (see the full
implementation plan this was scoped from).

## What's real vs. dummy in Phase 1

| Piece | Status |
|---|---|
| Frontend UI (menu, register, cancel) | **Real**, fully working against the API |
| REST API (`/api/v1/mess/...`) | **Real** FastAPI app, real validation, real business rules |
| Business rules (cutoff enforcement, no double-booking) | **Real**, enforced in the service layer |
| Data storage | **Real** — PostgreSQL in Docker |
| Auth | **Dummy** — every request acts as one seeded student (`Aditi Rao`) |
| AI/agents | **Not built yet** — Phase 1 is deliberately AI-free |

The backend is laid out in the same layers (`api → schemas → services →
repositories → models`) it'll have once a real Postgres-backed repository
replaces the in-memory one — swapping the storage layer later shouldn't
require touching the API routes or business logic.


## Database

This project uses PostgreSQL running in a Docker container (`db` service). 

- **Schema Setup**: The schema is automatically created on startup via SQLAlchemy (`Base.metadata.create_all`). Alembic migrations should be introduced in a future milestone when schema evolution without dropping data is needed.
- **Seeding**: On startup, if the `students` table is empty, the backend automatically seeds ~2 weeks of dummy menu data and one student (`Aditi Rao`). This operation is idempotent.
- **Resetting Data**: To wipe the database and start fresh, run:
  ```bash
  docker compose down -v
  ```
  This destroys the `pgdata` volume. Next time you run `docker compose up`, it will recreate the schema and re-seed the dummy data.

## Project structure

```
campuspilot/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # FastAPI routers (thin — call services, nothing else)
│   │   ├── core/             # config, typed exceptions, dummy auth stand-in
│   │   ├── models/            # domain dataclasses (Meal, Dish, Registration, Student)
│   │   ├── schemas/            # Pydantic request/response contracts
│   │   ├── repositories/        # in-memory data access (swap for Postgres later)
│   │   ├── services/             # business rules — cutoff checks, dupe prevention
│   │   ├── seed.py                # seeds ~2 weeks of dummy menu data on startup
│   │   └── main.py                # app wiring: CORS, exception handlers, routers
│   ├── tests/                       # pytest, async httpx client, 7 passing tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/client.ts            # typed fetch wrapper for the mess API
│   │   ├── components/               # Header, DaySelector, MealCard, ErrorToast
│   │   ├── hooks/useMessMenu.ts       # menu state + register/cancel actions
│   │   ├── pages/Dashboard.tsx         # the one Phase 1 screen
│   │   ├── types/mess.ts                # TS types mirroring the Pydantic schemas
│   │   └── styles/index.css              # design tokens, ticket-perforation motif
│   ├── package.json
│   ├── vite.config.ts                     # dev-server proxy to the backend
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## Design direction

The UI leans into what a mess registration actually *is* on Indian
campuses — a physical coupon you'd tear off a booklet — rather than a
generic dashboard. Each meal card has a perforated tear-line between the
menu and a status "stub" (Register / Booked), veg/non-veg items are marked
with the same green-square / brown-square dots used on real Indian food
packaging (not just color, so it's legible without relying on color
alone), and the type pairs a slab serif (menu-board feel) with Inter for
body text and IBM Plex Mono for times and status labels.

## Running it

### Option A — Docker Compose (one command)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (docs at `/docs`)

### Option B — run each side manually

**Backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # or your preferred env tool
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**Frontend** (in a second terminal):
```bash
cd frontend
npm install
npm run dev
```

Vite's dev server proxies `/api/*` to `http://localhost:8000`, so no CORS
setup is needed for local dev — the backend's CORS config is there for
when you eventually open it up to a non-proxied origin.

### Running tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

7 tests cover: menu retrieval, successful registration, double-registration
rejection, cutoff enforcement, cancellation, and a 404 on an unknown meal.

## API quick reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/api/v1/mess/menu?days=7` | Menu grouped by day, next N days |
| GET | `/api/v1/mess/registrations/me` | Current student's active registrations |
| POST | `/api/v1/mess/registrations` | Register for a meal (`{"meal_id": "..."}`) |
| DELETE | `/api/v1/mess/registrations/{id}` | Cancel a registration |

Full interactive docs at `/docs` once the backend is running (FastAPI's
auto-generated OpenAPI UI).

## What's next (not in this phase)

- **M1 — Auth**: replace `app/core/dummy_auth.py` with real JWT-based login
- **M2 (rest)**: Done — PostgreSQL is now integrated!
- **M3+**: diet profiles, PYQ RAG, the natural-language mess agent, and
  everything else in the full roadmap

This repo intentionally stops here for Phase 1 — a working, testable,
honestly-scoped slice rather than a shell UI over fake promises of AI
features that aren't built yet.
