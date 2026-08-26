"""
Mess service layer.

Business rules live here, not in the API routes: "can't register after the
cutoff", "can't double-register for the same meal", "can't cancel a
registration that isn't yours". This is the layer an agent tool will call
in a later milestone (M6, Mess Assistant Agent) — the tool wraps
`MessService.register_for_meal`, so a natural-language registration goes
through exactly the same checks as a click in the UI, which is the whole
point of the service-layer pattern described in Section 10 of the plan.

Phase 1's uniqueness guard lives here, in application code, because the
in-memory repository has no database to enforce it at the constraint
level. When M2 introduces a real Postgres-backed repository, a unique
constraint on (student_id, meal_id) is added there too, as defense in
depth — this check should never actually be reached by a double-write in
production, but it must never be trusted to be reached first either.
"""
import uuid
from datetime import datetime, timezone

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.mess import Registration, RegistrationStatus
from app.repositories.mess_repository import MessRepository


class MessService:
    def __init__(self, repo: MessRepository) -> None:
        self._repo = repo

    def get_day_menu(self, student_id: str, start, end):
        meals = self._repo.list_meals_between(start, end)
        registrations = {
            r.meal_id: r
            for r in self._repo.list_registrations_for_student(student_id)
            if r.status == RegistrationStatus.CONFIRMED
        }
        return meals, registrations

    def list_registrations(self, student_id: str) -> list[Registration]:
        return [
            r
            for r in self._repo.list_registrations_for_student(student_id)
            if r.status == RegistrationStatus.CONFIRMED
        ]

    def register_for_meal(self, student_id: str, meal_id: str) -> Registration:
        meal = self._repo.get_meal(meal_id)
        if meal is None:
            raise NotFoundError(f"Meal '{meal_id}' does not exist.")

        now = datetime.now(timezone.utc)
        if now >= meal.cutoff_at:
            raise ValidationError(
                f"Registration for this {meal.meal_type.value} closed at "
                f"{meal.cutoff_at.strftime('%H:%M on %d %b')}."
            )

        existing = self._repo.get_active_registration_for_meal(student_id, meal_id)
        if existing is not None:
            raise ConflictError("You're already registered for this meal.")

        registration = Registration(
            id=f"reg_{uuid.uuid4().hex[:10]}",
            student_id=student_id,
            meal_id=meal_id,
            status=RegistrationStatus.CONFIRMED,
            created_at=now,
            updated_at=now,
        )
        self._repo.add_registration(registration)
        return registration

    def cancel_registration(self, student_id: str, registration_id: str) -> Registration:
        registration = self._repo.get_registration(registration_id)
        if registration is None or registration.student_id != student_id:
            raise NotFoundError(f"Registration '{registration_id}' does not exist.")

        if registration.status == RegistrationStatus.CANCELLED:
            return registration

        meal = self._repo.get_meal(registration.meal_id)
        now = datetime.now(timezone.utc)
        if meal is not None and now >= meal.cutoff_at:
            raise ValidationError(
                f"Cancellation for this {meal.meal_type.value} closed at "
                f"{meal.cutoff_at.strftime('%H:%M on %d %b')}."
            )

        registration.status = RegistrationStatus.CANCELLED
        registration.updated_at = now
        return registration
