from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HabitLogCreate(BaseModel):
    log_date: date
    completed_value: Decimal | None = None
    is_completed: bool = False


class HabitLogUpdate(BaseModel):
    log_date: date | None = None
    completed_value: Decimal | None = None
    is_completed: bool | None = None


class HabitLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    user_id: int
    log_date: date
    completed_value: Decimal | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime