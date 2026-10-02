from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict,field_validator


class WellBeingScoreCreate(BaseModel):
    score_date: date
    score: int
    baseline_value: Decimal | None = None

    @field_validator("score")
    @classmethod
    def validate_score(cls, value: int) -> int:
        if value < 1 or value > 100:
            raise ValueError("Well-being score must be between 1 and 100")

        return value


class WellBeingScoreUpdate(BaseModel):
    score_date: date | None = None
    score: int | None = None
    baseline_value: Decimal | None = None

    @field_validator("score")
    @classmethod
    def validate_score(cls, value: int | None) -> int | None:
        if value is None:
            return None

        if value < 1 or value > 100:
            raise ValueError("Well-being score must be between 1 and 100")

        return value


class WellBeingScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    score_date: date
    score: int
    baseline_value: Decimal | None
    created_at: datetime
    updated_at: datetime