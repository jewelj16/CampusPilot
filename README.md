# CampusPilot

A campus mess registration platform. **Phase 1 + M1 (Auth)** is complete: a React frontend and a FastAPI backend with PostgreSQL and JWT authentication.

## Quick Start

Run the entire stack in Docker:

```bash
docker compose up --build
```
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Interactive API Docs:** http://localhost:8000/docs

### Default User
Use these credentials to log in, or sign up for a new account:
- **Roll Number:** `CS21B045`
- **Password:** `password`

## Database Management

The app uses a persistent PostgreSQL volume. To wipe the database and re-seed it on the next startup:
```bash
docker compose down -v
```

### Querying the Database
You can query the database directly by dropping into the `psql` shell inside the running container:
```bash
docker compose exec db psql -U campuspilot -d campuspilot
```
*Example queries once inside:*
- `\dt` (list tables)
- `SELECT * FROM students;` (view students)

Alternatively, connect a GUI client (like DBeaver or pgAdmin) to `localhost:5432` with user/password `campuspilot`.

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check |
| POST | `/api/v1/auth/signup` | Register a new student account |
| POST | `/api/v1/auth/login` | Log in with Roll Number & Password |
| GET | `/api/v1/auth/me` | Get the logged-in student's profile |
| GET | `/api/v1/mess/menu?days=7` | Menu grouped by day |
| GET | `/api/v1/mess/registrations/me` | Current student's registrations |
| POST | `/api/v1/mess/registrations` | Register for a meal |
| DELETE | `/api/v1/mess/registrations/{id}` | Cancel a registration |

## Testing
To run the automated tests locally:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```
