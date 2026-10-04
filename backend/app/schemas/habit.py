from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class HabitCreate(BaseModel):
    name: str
    target_value: Decimal
    target_unit: str | None = None
    frequency: str = "daily"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Habit name cannot be empty")

        return value

    @field_validator("target_value")
    @classmethod
    def validate_target_value(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Habit target must be greater than zero")

        return value

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: str) -> str:
        value = value.strip().lower()

        if value != "daily":
            raise ValueError("Only daily frequency is supported")

        return value


class HabitUpdate(BaseModel):
    name: str | None = None
    target_value: Decimal | None = None
    target_unit: str | None = None
    frequency: str | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Habit name cannot be empty")

        return value

    @field_validator("target_value")
    @classmethod
    def validate_target_value(cls, value: Decimal | None) -> Decimal | None:
        if value is None:
            return None

        if value <= 0:
            raise ValueError("Habit target must be greater than zero")

        return value

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip().lower()

        if value != "daily":
            raise ValueError("Only daily frequency is supported")

        return value


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    target_value: Decimal
    target_unit: str | None
    frequency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime