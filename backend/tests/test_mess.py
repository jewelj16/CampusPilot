"""
API-level tests for the Phase 1 mess module, now backed by a real Postgres
database spun up via testcontainers.
"""
from datetime import date, datetime, timedelta, timezone

import httpx
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.main import app
from app.models.mess import Dish, Meal, MealType
from app.core.db import Base, get_db
from app.repositories.postgres_mess_repository import PostgresMessRepository
from app.repositories.orm_models import MealORM, RegistrationORM, StudentORM
from app.seed import seed

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="session")
def postgres_engine():
    with PostgresContainer("postgres:16-alpine") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine


@pytest.fixture
def db_session(postgres_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)
    session = SessionLocal()
    
    # Clean up before test
    session.query(RegistrationORM).delete()
    session.query(MealORM).delete()
    session.query(StudentORM).delete()
    session.commit()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest_asyncio.fixture
async def client(db_session):
    seed(db_session)
    db_session.commit()

    def override_get_db():
        try:
            yield db_session
        except Exception:
            pass

    app.dependency_overrides[get_db] = override_get_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_get_menu_returns_days(client):
    resp = await client.get("/api/v1/mess/menu?days=7")
    assert resp.status_code == 200
    days = resp.json()
    assert len(days) == 7
    assert all(len(day["meals"]) == 4 for day in days)


async def test_register_then_appears_in_my_registrations(client):
    menu = (await client.get("/api/v1/mess/menu?days=14")).json()
    open_meal = next(
        m for day in menu for m in day["meals"] if m["is_open"] and m["registration"] is None
    )

    resp = await client.post("/api/v1/mess/registrations", json={"meal_id": open_meal["id"]})
    assert resp.status_code == 201
    registration = resp.json()
    assert registration["meal_id"] == open_meal["id"]
    assert registration["status"] == "confirmed"

    mine = (await client.get("/api/v1/mess/registrations/me")).json()
    assert any(r["id"] == registration["id"] for r in mine)


async def test_double_registration_is_rejected(client):
    menu = (await client.get("/api/v1/mess/menu?days=14")).json()
    open_meal = next(
        m for day in menu for m in day["meals"] if m["is_open"] and m["registration"] is None
    )

    first = await client.post("/api/v1/mess/registrations", json={"meal_id": open_meal["id"]})
    assert first.status_code == 201

    second = await client.post("/api/v1/mess/registrations", json={"meal_id": open_meal["id"]})
    assert second.status_code == 409


async def test_registration_after_cutoff_is_rejected(client, db_session):
    past_meal = Meal(
        id="meal_test_past",
        mess_name="Hostel Mess A",
        date=date.today(),
        meal_type=MealType.BREAKFAST,
        dishes=[Dish(id="d_test", name="Test Dish", is_veg=True)],
        cutoff_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    repo = PostgresMessRepository(db_session)
    repo.add_meal(past_meal)
    db_session.commit()

    resp = await client.post("/api/v1/mess/registrations", json={"meal_id": "meal_test_past"})
    assert resp.status_code == 400


async def test_cancel_registration(client):
    menu = (await client.get("/api/v1/mess/menu?days=14")).json()
    open_meal = next(
        m for day in menu for m in day["meals"] if m["is_open"] and m["registration"] is None
    )
    reg = (await client.post("/api/v1/mess/registrations", json={"meal_id": open_meal["id"]})).json()

    resp = await client.delete(f"/api/v1/mess/registrations/{reg['id']}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"

    mine = (await client.get("/api/v1/mess/registrations/me")).json()
    assert all(r["id"] != reg["id"] for r in mine)


async def test_register_nonexistent_meal_404(client):
    resp = await client.post("/api/v1/mess/registrations", json={"meal_id": "does-not-exist"})
    assert resp.status_code == 404
