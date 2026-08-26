"""
Domain models for the mess module.

These are plain dataclasses, not SQLAlchemy models — Phase 1 has no
database (see repositories/mess_repository.py). They're kept in their own
`models/` layer anyway so the shape matches Section 21 of the plan
(api -> schemas -> services -> repositories -> models) and swapping in
real SQLAlchemy models at M2 doesn't change any layer above this one.
"""
from dataclasses import dataclass, field
from datetime import date as Date
from datetime import datetime
from enum import Enum


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    SNACKS = "snacks"
    DINNER = "dinner"


class RegistrationStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Dish:
    id: str
    name: str
    is_veg: bool


@dataclass(frozen=True)
class Meal:
    id: str
    mess_name: str
    date: Date
    meal_type: MealType
    dishes: list[Dish]
    cutoff_at: datetime  # registrations/cancellations must happen before this


@dataclass
class Registration:
    id: str
    student_id: str
    meal_id: str
    status: RegistrationStatus
    created_at: datetime
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class Student:
    id: str
    name: str
    roll_no: str
    hostel: str
