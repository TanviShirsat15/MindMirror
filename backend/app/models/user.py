from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
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

    journals = relationship(
        "Journal",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    habits = relationship(
        "Habit",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    habit_logs = relationship(
        "HabitLog",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    wellbeing_scores = relationship(
        "WellBeingScore",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    insights = relationship(
        "Insight",
        back_populates="owner",
        cascade="all, delete-orphan",
    )