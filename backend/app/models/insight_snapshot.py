from datetime import datetime, date

from sqlalchemy import Date, DateTime, Float, Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InsightSnapshot(Base):
    __tablename__ = "insight_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    insight_key: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    direction: Mapped[str] = mapped_column(String(30), nullable=False)

    window_start: Mapped[date] = mapped_column(Date, nullable=False)
    window_end: Mapped[date] = mapped_column(Date, nullable=False)

    supporting_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_bucket: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    first_generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    last_changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    last_generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "insight_key",
            name="uq_insight_snapshot_user_key",
        ),
        Index(
            "ix_insight_snapshot_user_last_changed",
            "user_id",
            "last_changed_at",
        ),
    )
