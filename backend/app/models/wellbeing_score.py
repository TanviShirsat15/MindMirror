from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Numeric, SmallInteger, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Numeric, SmallInteger, UniqueConstraint

from app.database import Base


class WellBeingScore(Base):
    __tablename__ = "wellbeing_scores"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    score_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    baseline_value: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
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

    owner = relationship(
        "User",
        back_populates="wellbeing_scores",
    )

    __table_args__ = (
        Index("ix_wellbeing_scores_user_id", "user_id"),
        Index("ix_wellbeing_scores_score_date", "score_date"),
        CheckConstraint(
            "score >= 1 AND score <= 100",
            name="ck_wellbeing_scores_score_range",
        ),
        UniqueConstraint(
    "user_id",
    "score_date",
    name="uq_wellbeing_scores_user_date",
),
    )