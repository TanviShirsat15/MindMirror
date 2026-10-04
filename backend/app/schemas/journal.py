from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator


class JournalCreate(BaseModel):
    content: str
    entry_date: date | None = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Journal content cannot be empty")

        return value


class JournalUpdate(BaseModel):
    content: str | None = None
    entry_date: date | None = None

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if not value.strip():
            raise ValueError("Journal content cannot be empty")

        return value


class JournalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    content: str
    entry_date: date
    created_at: datetime
    updated_at: datetime