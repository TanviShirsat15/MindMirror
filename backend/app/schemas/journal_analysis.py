from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JournalAnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    journal_id: int
    sentiment_score: float
    stress_indicator: float
    positive_emotion_score: float | None
    created_at: datetime
    updated_at: datetime