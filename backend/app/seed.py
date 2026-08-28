"""
Seeds the in-memory repository with one student and two weeks of meals so
the frontend has something real to register against on first boot.

Cutoff rule (dummy, for demo purposes): registration/cancellation closes
2 hours before the meal's serving time. Meals in the past relative to
`datetime.now()` are seeded already closed, so the UI has at least one
"closed" state to render without waiting a day.
"""
from datetime import date, datetime, time, timedelta, timezone

from app.core.auth import DUMMY_STUDENT_ID
from app.models.mess import Dish, Meal, MealType, Student
from sqlalchemy.orm import Session
from app.repositories.postgres_mess_repository import PostgresMessRepository
from app.repositories.orm_models import StudentORM

MESS_NAME = "Hostel Mess A"

# meal_type -> (serving time, menu of dishes)
_MENU_CYCLE: list[dict] = [
    {
        MealType.BREAKFAST: (time(8, 0), [("Idli & Sambar", True), ("Boiled Eggs", False), ("Filter Coffee", True)]),
        MealType.LUNCH: (time(13, 0), [("Veg Thali", True), ("Chicken Curry", False), ("Curd Rice", True)]),
        MealType.SNACKS: (time(17, 0), [("Samosa", True), ("Masala Chai", True)]),
        MealType.DINNER: (time(20, 30), [("Roti & Dal", True), ("Paneer Butter Masala", True), ("Egg Curry", False)]),
    },
    {
        MealType.BREAKFAST: (time(8, 0), [("Poha", True), ("Omelette", False), ("Filter Coffee", True)]),
        MealType.LUNCH: (time(13, 0), [("Veg Biryani", True), ("Mutton Curry", False), ("Raita", True)]),
        MealType.SNACKS: (time(17, 0), [("Bread Pakora", True), ("Masala Chai", True)]),
        MealType.DINNER: (time(20, 30), [("Fried Rice", True), ("Chilli Chicken", False), ("Manchurian", True)]),
    },
]


def _dish(name: str, is_veg: bool, idx: int) -> Dish:
    return Dish(id=f"dish_{idx}", name=name, is_veg=is_veg)


from app.services.auth_service import get_password_hash

def seed(session: Session) -> None:
    repo = PostgresMessRepository(session)
    # Check if DB is already seeded
    if session.query(StudentORM).first() is not None:
        return

    # Seed the dummy student with a default password directly using ORM
    session.add(
        StudentORM(
            id=DUMMY_STUDENT_ID,
            name="Aditi Rao",
            roll_no="CS21B045",
            hostel="Hostel A",
            hashed_password=get_password_hash("password")
        )
    )

    dish_counter = 0
    today = date.today()

    # Seed from 2 days ago through 12 days ahead, so there's at least one
    # closed/past meal visible alongside the open upcoming ones.
    for offset in range(-2, 13):
        the_date = today + timedelta(days=offset)
        day_menu = _MENU_CYCLE[offset % len(_MENU_CYCLE)]

        for meal_type, (serve_time, dishes) in day_menu.items():
            dish_objs = []
            for name, is_veg in dishes:
                dish_counter += 1
                dish_objs.append(_dish(name, is_veg, dish_counter))

            serve_at = datetime.combine(the_date, serve_time, tzinfo=timezone.utc)
            cutoff_at = serve_at - timedelta(hours=2)

            meal = Meal(
                id=f"meal_{the_date.isoformat()}_{meal_type.value}",
                mess_name=MESS_NAME,
                date=the_date,
                meal_type=meal_type,
                dishes=dish_objs,
                cutoff_at=cutoff_at,
            )
            repo.add_meal(meal)
