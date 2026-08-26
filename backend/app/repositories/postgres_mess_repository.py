from datetime import date as Date
from typing import Optional

from sqlalchemy.orm import Session

from app.models.mess import Meal, Registration, RegistrationStatus, Student, Dish, MealType
from app.repositories.orm_models import MealORM, RegistrationORM, StudentORM

class PostgresMessRepository:
    """
    PostgreSQL-backed implementation of the MessRepository interface.
    This class is instantiated per-request and passed an active database Session.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    # ---- mapping helpers -------------------------------------------
    def _map_meal_orm_to_model(self, orm: MealORM) -> Meal:
        dishes = [Dish(id=d["id"], name=d["name"], is_veg=d["is_veg"]) for d in orm.dishes]
        return Meal(
            id=orm.id,
            mess_name=orm.mess_name,
            date=orm.date,
            meal_type=orm.meal_type,
            dishes=dishes,
            cutoff_at=orm.cutoff_at
        )

    def _map_registration_orm_to_model(self, orm: RegistrationORM) -> Registration:
        return Registration(
            id=orm.id,
            student_id=orm.student_id,
            meal_id=orm.meal_id,
            status=orm.status,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )

    def _map_student_orm_to_model(self, orm: StudentORM) -> Student:
        return Student(
            id=orm.id,
            name=orm.name,
            roll_no=orm.roll_no,
            hostel=orm.hostel
        )

    # ---- meals -----------------------------------------------------
    def add_meal(self, meal: Meal) -> None:
        # Convert domain models to dictionaries for JSONB
        dishes_json = [{"id": d.id, "name": d.name, "is_veg": d.is_veg} for d in meal.dishes]
        
        orm = MealORM(
            id=meal.id,
            mess_name=meal.mess_name,
            date=meal.date,
            meal_type=meal.meal_type,
            dishes=dishes_json,
            cutoff_at=meal.cutoff_at
        )
        self.session.add(orm)

    def get_meal(self, meal_id: str) -> Optional[Meal]:
        orm = self.session.query(MealORM).filter(MealORM.id == meal_id).first()
        if orm:
            return self._map_meal_orm_to_model(orm)
        return None

    def list_meals_between(self, start: Date, end: Date) -> list[Meal]:
        orms = (
            self.session.query(MealORM)
            .filter(MealORM.date >= start, MealORM.date <= end)
            .all()
        )
        
        # Sort in python, or could do it in DB via order_by.
        # Following the existing implementation sorting.
        # Enums in python sorting: meal_type.value is string, so it relies on string sorting or custom logic.
        # Actually it's better to just map and sort like before to maintain exact behavior.
        meals = [self._map_meal_orm_to_model(orm) for orm in orms]
        return sorted(
            meals,
            key=lambda m: (m.date, m.meal_type.value),
        )

    # ---- students ----------------------------------------------------
    def add_student(self, student: Student) -> None:
        orm = StudentORM(
            id=student.id,
            name=student.name,
            roll_no=student.roll_no,
            hostel=student.hostel
        )
        self.session.add(orm)

    def get_student(self, student_id: str) -> Optional[Student]:
        orm = self.session.query(StudentORM).filter(StudentORM.id == student_id).first()
        if orm:
            return self._map_student_orm_to_model(orm)
        return None

    # ---- registrations ------------------------------------------------
    def add_registration(self, registration: Registration) -> None:
        orm = RegistrationORM(
            id=registration.id,
            student_id=registration.student_id,
            meal_id=registration.meal_id,
            status=registration.status,
            created_at=registration.created_at,
            updated_at=registration.updated_at
        )
        self.session.merge(orm) # Merge handles both inserts and updates (cancellation)

    def get_registration(self, registration_id: str) -> Optional[Registration]:
        orm = self.session.query(RegistrationORM).filter(RegistrationORM.id == registration_id).first()
        if orm:
            return self._map_registration_orm_to_model(orm)
        return None

    def get_active_registration_for_meal(
        self, student_id: str, meal_id: str
    ) -> Optional[Registration]:
        orm = (
            self.session.query(RegistrationORM)
            .filter(
                RegistrationORM.student_id == student_id,
                RegistrationORM.meal_id == meal_id,
                RegistrationORM.status == RegistrationStatus.CONFIRMED
            )
            .first()
        )
        if orm:
            return self._map_registration_orm_to_model(orm)
        return None

    def list_registrations_for_student(self, student_id: str) -> list[Registration]:
        orms = (
            self.session.query(RegistrationORM)
            .filter(RegistrationORM.student_id == student_id)
            .all()
        )
        return [self._map_registration_orm_to_model(orm) for orm in orms]
