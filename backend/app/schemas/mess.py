from datetime import date as Date
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.mess import MealType, RegistrationStatus


class DishOut(BaseModel):
    id: str
    name: str
    is_veg: bool

    model_config = ConfigDict(from_attributes=True)


class MealOut(BaseModel):
    id: str
    mess_name: str
    date: Date
    meal_type: MealType
    dishes: list[DishOut]
    cutoff_at: datetime

    # Derived, convenience fields for the frontend — computed in the service
    # layer so the UI never has to duplicate "is this still open" logic.
    is_open: bool
    registration: "RegistrationOut | None" = None

    model_config = ConfigDict(from_attributes=True)


class DayMenuOut(BaseModel):
    date: Date
    meals: list[MealOut]


class RegistrationOut(BaseModel):
    id: str
    meal_id: str
    status: RegistrationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RegistrationCreate(BaseModel):
    meal_id: str = Field(..., description="ID of the meal to register for")


class ErrorResponse(BaseModel):
    detail: str
