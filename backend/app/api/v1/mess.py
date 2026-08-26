from datetime import date as Date
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.postgres_mess_repository import PostgresMessRepository

from app.core.dummy_auth import CurrentStudentId
from app.models.mess import Meal, Registration
from app.schemas.mess import DayMenuOut, DishOut, MealOut, RegistrationCreate, RegistrationOut
from app.services.mess_service import MessService

router = APIRouter(prefix="/mess", tags=["mess"])


def get_mess_service(db: Session = Depends(get_db)) -> MessService:
    repo = PostgresMessRepository(db)
    return MessService(repo)


def _to_registration_out(registration: Registration) -> RegistrationOut:
    return RegistrationOut(
        id=registration.id,
        meal_id=registration.meal_id,
        status=registration.status,
        created_at=registration.created_at,
    )


def _to_meal_out(meal: Meal, registration: Registration | None) -> MealOut:
    is_open = datetime.now(timezone.utc) < meal.cutoff_at
    return MealOut(
        id=meal.id,
        mess_name=meal.mess_name,
        date=meal.date,
        meal_type=meal.meal_type,
        dishes=[DishOut(id=d.id, name=d.name, is_veg=d.is_veg) for d in meal.dishes],
        cutoff_at=meal.cutoff_at,
        is_open=is_open,
        registration=_to_registration_out(registration) if registration else None,
    )


@router.get("/menu", response_model=list[DayMenuOut])
def get_menu(
    student_id: CurrentStudentId,
    days: int = Query(7, ge=1, le=14, description="Number of days ahead to include, starting today"),
    service: MessService = Depends(get_mess_service)
) -> list[DayMenuOut]:
    today = Date.today()
    end = today + timedelta(days=days - 1)
    meals, registrations = service.get_day_menu(student_id, today, end)

    by_day: dict[Date, list[MealOut]] = {}
    for meal in meals:
        by_day.setdefault(meal.date, []).append(_to_meal_out(meal, registrations.get(meal.id)))

    return [DayMenuOut(date=d, meals=by_day[d]) for d in sorted(by_day)]


@router.get("/registrations/me", response_model=list[RegistrationOut])
def list_my_registrations(student_id: CurrentStudentId, service: MessService = Depends(get_mess_service)) -> list[RegistrationOut]:
    return [_to_registration_out(r) for r in service.list_registrations(student_id)]


@router.post("/registrations", response_model=RegistrationOut, status_code=status.HTTP_201_CREATED)
def create_registration(payload: RegistrationCreate, student_id: CurrentStudentId, service: MessService = Depends(get_mess_service)) -> RegistrationOut:
    registration = service.register_for_meal(student_id, payload.meal_id)
    return _to_registration_out(registration)


@router.delete("/registrations/{registration_id}", response_model=RegistrationOut)
def cancel_registration(registration_id: str, student_id: CurrentStudentId, service: MessService = Depends(get_mess_service)) -> RegistrationOut:
    registration = service.cancel_registration(student_id, registration_id)
    return _to_registration_out(registration)
