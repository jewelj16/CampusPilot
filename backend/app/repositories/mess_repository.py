"""
In-memory repository for meals and registrations.

NOTE: Retained for fast unit tests / as a reference implementation, but is no longer used by the running app. The running app now uses PostgresMessRepository.

This is Phase 1's "dummy backend": no Postgres, no SQLAlchemy — just
process-local dicts, seeded on startup. The public methods here are the
same shape a real `SQLAlchemyMessRepository` will have at M2 (get, list,
add, update), so `MessService` (which only talks to this interface) won't
need to change when the in-memory store is swapped for a real one.

Not thread-safe beyond what Python's GIL gives you for free, and state
resets every time the process restarts — both fine and expected for a
Phase 1 demo backend.
"""
from datetime import date as Date

from app.models.mess import Meal, Registration, RegistrationStatus, Student


class MessRepository:
    def __init__(self) -> None:
        self._meals: dict[str, Meal] = {}
        self._registrations: dict[str, Registration] = {}
        self._students: dict[str, Student] = {}

    # ---- meals -----------------------------------------------------
    def add_meal(self, meal: Meal) -> None:
        self._meals[meal.id] = meal

    def get_meal(self, meal_id: str) -> Meal | None:
        return self._meals.get(meal_id)

    def list_meals_between(self, start: Date, end: Date) -> list[Meal]:
        return sorted(
            (m for m in self._meals.values() if start <= m.date <= end),
            key=lambda m: (m.date, m.meal_type.value),
        )

    # ---- students ----------------------------------------------------
    def add_student(self, student: Student) -> None:
        self._students[student.id] = student

    def get_student(self, student_id: str) -> Student | None:
        return self._students.get(student_id)

    # ---- registrations ------------------------------------------------
    def add_registration(self, registration: Registration) -> None:
        self._registrations[registration.id] = registration

    def get_registration(self, registration_id: str) -> Registration | None:
        return self._registrations.get(registration_id)

    def get_active_registration_for_meal(
        self, student_id: str, meal_id: str
    ) -> Registration | None:
        for reg in self._registrations.values():
            if (
                reg.student_id == student_id
                and reg.meal_id == meal_id
                and reg.status == RegistrationStatus.CONFIRMED
            ):
                return reg
        return None

    def list_registrations_for_student(self, student_id: str) -> list[Registration]:
        return [r for r in self._registrations.values() if r.student_id == student_id]


# Process-wide singleton — one shared in-memory "database" for the app's
# lifetime, mirroring how a real connection pool would be a singleton too.
mess_repository = MessRepository()
