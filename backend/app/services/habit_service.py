from datetime import UTC, date, datetime, timedelta

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate


def create_habit(
    db: Session,
    current_user: User,
    habit_data: HabitCreate,
) -> Habit:
    habit = Habit(
        user_id=current_user.id,
        name=habit_data.name,
        target_value=habit_data.target_value,
        target_unit=habit_data.target_unit,
        frequency=habit_data.frequency,
        is_active=True,
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)

    return habit


def list_habits(
    db: Session,
    current_user: User,
) -> list[Habit]:
    return (
        db.query(Habit)
        .filter(Habit.user_id == current_user.id)
        .order_by(Habit.id.desc())
        .all()
    )


def get_habit(
    db: Session,
    current_user: User,
    habit_id: int,
) -> Habit:
    habit = (
        db.query(Habit)
        .filter(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
        .first()
    )

    if habit is None:
        raise ValueError("Habit not found")

    return habit


def update_habit(
    db: Session,
    current_user: User,
    habit_id: int,
    habit_data: HabitUpdate,
) -> Habit:
    habit = get_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    if habit_data.name is not None:
        habit.name = habit_data.name

    if habit_data.target_value is not None:
        habit.target_value = habit_data.target_value

    if habit_data.target_unit is not None:
        habit.target_unit = habit_data.target_unit

    if habit_data.frequency is not None:
        habit.frequency = habit_data.frequency

    if habit_data.is_active is not None:
        if habit_data.is_active:
            habit.is_active = True
            habit.deactivated_at = None
        else:
            habit.is_active = False
            habit.deactivated_at = datetime.now(UTC)

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(
    db: Session,
    current_user: User,
    habit_id: int,
) -> None:
    habit = get_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    db.delete(habit)
    db.commit()


def get_habit_metrics(
    db: Session,
    current_user: User,
    habit_id: int,
    window: str = "weekly",
) -> dict:
    habit = get_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    if window not in {"weekly", "historical"}:
        raise ValueError("Invalid metrics window")

    today = date.today()

    if window == "weekly":
        start_date = today - timedelta(days=6)
    else:
        start_date = habit.created_at.date()

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.user_id == current_user.id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= today,
        )
        .order_by(HabitLog.log_date.asc())
        .all()
    )

    completed_dates = {
        log.log_date
        for log in logs
        if log.is_completed
    }

    expected_days = (today - start_date).days + 1
    completed_days = len(completed_dates)

    completion_rate = (
        (completed_days / expected_days) * 100
        if expected_days > 0
        else 0.0
    )

    # Current streak:
    # Start from the most recent completed day and count
    # consecutive completed days backwards.
    current_streak = 0

    if completed_dates:
        streak_date = max(completed_dates)

        while streak_date in completed_dates:
            current_streak += 1
            streak_date -= timedelta(days=1)

    # Longest consecutive completed-day streak.
    longest_streak = 0
    streak = 0
    current_date = start_date

    while current_date <= today:
        if current_date in completed_dates:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

        current_date += timedelta(days=1)

    return {
        "habit_id": habit.id,
        "window": window,
        "start_date": start_date,
        "end_date": today,
        "expected_days": expected_days,
        "completed_days": completed_days,
        "completion_rate": round(completion_rate, 2),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    }