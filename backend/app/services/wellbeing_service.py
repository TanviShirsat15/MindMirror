from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.journal import Journal
from app.models.journal_analysis import JournalAnalysis
from app.models.user import User
from app.models.wellbeing_score import WellBeingScore
from app.schemas.wellbeing_score import (
    WellBeingScoreCreate,
    WellBeingScoreUpdate,
)
from app.services.fuzzy.fuzzy_engine import calculate_wellbeing_index


def _get_daily_journal_signals(
    db: Session,
    current_user: User,
    score_date: date,
) -> tuple[float, float] | None:
    """Return average sentiment and stress for journals on a date."""

    rows = (
        db.query(JournalAnalysis.sentiment_score, JournalAnalysis.stress_indicator)
        .join(Journal, JournalAnalysis.journal_id == Journal.id)
        .filter(
            Journal.user_id == current_user.id,
            Journal.entry_date == score_date,
        )
        .all()
    )

    if not rows:
        return None

    daily_sentiment = sum(row.sentiment_score for row in rows) / len(rows)
    daily_stress = sum(row.stress_indicator for row in rows) / len(rows)

    return daily_sentiment, daily_stress


def _get_habit_consistency(
    db: Session,
    current_user: User,
    score_date: date,
) -> float | None:
    """
    Calculate same-day habit consistency.

    completed active habits on the date /
    active habits that existed as of that date
    """

    active_habits = (
        db.query(Habit)
        .filter(
            Habit.user_id == current_user.id,
            Habit.is_active.is_(True),
        )
        .all()
    )

    habits_existing_on_date = [
        habit
        for habit in active_habits
        if habit.created_at.date() <= score_date
    ]

    if not habits_existing_on_date:
        return None

    habit_ids = {habit.id for habit in habits_existing_on_date}

    completed_count = (
        db.query(HabitLog)
        .filter(
            HabitLog.user_id == current_user.id,
            HabitLog.log_date == score_date,
            HabitLog.habit_id.in_(habit_ids),
            HabitLog.is_completed.is_(True),
        )
        .count()
    )

    return completed_count / len(habits_existing_on_date)


def recalculate_for_date(
    db: Session,
    current_user: User,
    score_date: date,
) -> WellBeingScore | None:
    """
    Recalculate the Well-Being Index for one user/date.

    Returns None when the required source data is unavailable.
    """

    journal_signals = _get_daily_journal_signals(
        db=db,
        current_user=current_user,
        score_date=score_date,
    )

    existing_score = db.scalar(
        select(WellBeingScore).where(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date == score_date,
        )
    )

    if journal_signals is None:
        if existing_score is not None:
            db.delete(existing_score)
            db.commit()
        return None

    habit_consistency = _get_habit_consistency(
        db=db,
        current_user=current_user,
        score_date=score_date,
    )

    if habit_consistency is None:
        if existing_score is not None:
            db.delete(existing_score)
            db.commit()
        return None

    daily_sentiment, daily_stress = journal_signals

    result = calculate_wellbeing_index(
        sentiment_score=daily_sentiment,
        stress_indicator=daily_stress,
        habit_consistency=habit_consistency,
    )

    score_value = int(round(result["score"]))

    if existing_score is None:
        existing_score = WellBeingScore(
            user_id=current_user.id,
            score_date=score_date,
            score=score_value,
            baseline_value=None,
        )
        db.add(existing_score)
    else:
        existing_score.score = score_value

    db.commit()
    db.refresh(existing_score)

    return existing_score


def create_score(
    db: Session,
    current_user: User,
    score_data: WellBeingScoreCreate
) -> WellBeingScore:
    existing = db.scalar(
        select(WellBeingScore).where(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date == score_data.score_date,
        )
    )

    if existing is not None:
        raise ValueError("A well-being score already exists for this date")

    score = WellBeingScore(
        user_id=current_user.id,
        score_date=score_data.score_date,
        score=score_data.score,
        baseline_value=score_data.baseline_value,
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    return score


def list_scores(
    db: Session,
    current_user: User,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[WellBeingScore]:
    query = select(WellBeingScore).where(
        WellBeingScore.user_id == current_user.id
    )

    if start_date is not None:
        query = query.where(WellBeingScore.score_date >= start_date)

    if end_date is not None:
        query = query.where(WellBeingScore.score_date <= end_date)

    query = query.order_by(WellBeingScore.score_date.desc())

    return list(db.scalars(query).all())


def get_score(
    db: Session,
    current_user: User,
    score_id: int,
) -> WellBeingScore:
    score = db.scalar(
        select(WellBeingScore).where(
            WellBeingScore.id == score_id,
            WellBeingScore.user_id == current_user.id,
        )
    )

    if score is None:
        raise ValueError("Well-being score not found")

    return score


def get_score_for_date(
    db: Session,
    current_user: User,
    score_date: date,
) -> WellBeingScore | None:
    return db.scalar(
        select(WellBeingScore).where(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date == score_date,
        )
    )


def update_score(
    db: Session,
    current_user: User,
    score_id: int,
    score_data: WellBeingScoreCreate,
) -> WellBeingScore:
    score = get_score(db, current_user, score_id)

    if score_data.score_date is not None:
        score.score_date = score_data.score_date

    if score_data.score is not None:
        score.score = score_data.score

    if score_data.baseline_value is not None:
        score.baseline_value = score_data.baseline_value

    db.commit()
    db.refresh(score)

    return score


def delete_score(
    db: Session,
    current_user: User,
    score_id: int,
) -> None:
    score = get_score(db, current_user, score_id)

    db.delete(score)
    db.commit()