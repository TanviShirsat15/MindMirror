from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    habit_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    log_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    completed_value: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
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

    habit = relationship(
        "Habit",
        back_populates="logs",
    )

    owner = relationship(
        "User",
        back_populates="habit_logs",
    )

    __table_args__ = (
        Index("ix_habit_logs_habit_id", "habit_id"),
        Index("ix_habit_logs_user_id", "user_id"),
        Index("ix_habit_logs_log_date", "log_date"),
        UniqueConstraint(
            "habit_id",
            "log_date",
            name="uq_habit_logs_habit_date",
        ),
    )