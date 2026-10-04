from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class JournalAnalysis(Base):
    __tablename__ = "journal_analysis"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    journal_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("journals.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    sentiment_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stress_indicator: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    positive_emotion_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    negative_emotion_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    journal = relationship(
        "Journal",
        back_populates="analysis",
    )