"""
Basic API-level tests for the Phase 1 mess module.

These hit the FastAPI app directly via httpx's ASGI transport — no real
server, no real DB, just the app + its in-memory repository, seeded fresh
for each test via the `client` fixture.
"""
from datetime import date, datetime, timedelta, timezone

import httpx
import pytest
import pytest_asyncio

from app.main import app
from app.models.mess import Dish, Meal, MealType
from app.repositories.mess_repository import mess_repository
from app.seed import seed

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def client():
    # Reset and reseed the in-memory store before every test so tests
    # don't leak state into each other.
    mess_repository._meals.clear()
    mess_repository._registrations.clear()
    mess_repository._students.clear()
    seed(mess_repository)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_get_menu_returns_days(client):
    resp = await client.get("/api/v1/mess/menu?days=7")
    assert resp.status_code == 200
    days = resp.json()
    assert len(days) == 7
    assert all(len(day["meals"]) == 4 for day in days)  # breakfast/lunch/snacks/dinner


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


async def test_registration_after_cutoff_is_rejected(client):
    # Seed a meal whose cutoff is already in the past.
    past_meal = Meal(
        id="meal_test_past",
        mess_name="Hostel Mess A",
        date=date.today(),
        meal_type=MealType.BREAKFAST,
        dishes=[Dish(id="d_test", name="Test Dish", is_veg=True)],
        cutoff_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    mess_repository.add_meal(past_meal)

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
