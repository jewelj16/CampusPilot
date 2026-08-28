from datetime import datetime
from datetime import date as Date

from sqlalchemy import Column, String, Boolean, DateTime, Date as SQLDate, Enum, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.mess import MealType, RegistrationStatus

class StudentORM(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, nullable=False)
    hostel = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


class MealORM(Base):
    __tablename__ = 'meals'

    id = Column(String, primary_key=True)
    mess_name = Column(String, nullable=False)
    date = Column(SQLDate, nullable=False)
    meal_type = Column(Enum(MealType), nullable=False)
    
    # We use a JSON/JSONB column here for storing dishes in Phase 1 for simplicity.
    # A proper meal_dishes association table could be used later if we need to 
    # query dishes independently or share them across meals.
    dishes = Column(JSONB, nullable=False) 
    cutoff_at = Column(DateTime(timezone=True), nullable=False)


class RegistrationORM(Base):
    __tablename__ = 'registrations'

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    meal_id = Column(String, ForeignKey('meals.id'), nullable=False)
    status = Column(Enum(RegistrationStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Using a Postgres-specific partial unique index to enforce the business rule that
    # a student can only have one confirmed registration per meal at the database level.
    # This prevents race conditions where double-registration could occur.
    __table_args__ = (
        Index(
            'ix_unique_active_registration', 
            'student_id', 
            'meal_id', 
            unique=True, 
            postgresql_where=(status == RegistrationStatus.CONFIRMED.value)
        ),
    )
