from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class InsightCreate(BaseModel):
    insight_date: date | None = None
    content: str


class InsightUpdate(BaseModel):
    insight_date: date | None = None
    content: str | None = None


class InsightRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    insight_date: date | None
    content: str
    created_at: datetime
    updated_at: datetime