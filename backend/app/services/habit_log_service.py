from datetime import date

from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate
from app.services.wellbeing_service import recalculate_for_date


def get_user_habit(
    db: Session,
    current_user: User,
    habit_id: int,
) -> Habit:
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id,
    ).first()

    if habit is None:
        raise ValueError("Habit not found")

    return habit


def create_habit_log(
    db: Session,
    current_user: User,
    habit_id: int,
    log_data: HabitLogCreate,
) -> HabitLog:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    existing_log = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.log_date == log_data.log_date,
    ).first()

    if existing_log is not None:
        raise ValueError(
            "A log already exists for this habit and date. "
            "Use the update endpoint instead."
        )

    habit_log = HabitLog(
        habit_id=habit_id,
        user_id=current_user.id,
        log_date=log_data.log_date,
        completed_value=log_data.completed_value,
        is_completed=log_data.is_completed,
    )

    db.add(habit_log)
    db.commit()
    db.refresh(habit_log)

    return habit_log


def list_habit_logs(
    db: Session,
    current_user: User,
    habit_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[HabitLog]:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    query = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.user_id == current_user.id,
    )

    if start_date is not None:
        query = query.filter(HabitLog.log_date >= start_date)

    if end_date is not None:
        query = query.filter(HabitLog.log_date <= end_date)

    return query.order_by(HabitLog.log_date.desc()).all()


def update_habit_log(
    db: Session,
    current_user: User,
    habit_id: int,
    log_id: int,
    log_data: HabitLogUpdate,
) -> HabitLog:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    habit_log = db.query(HabitLog).filter(
        HabitLog.id == log_id,
        HabitLog.habit_id == habit_id,
        HabitLog.user_id == current_user.id,
    ).first()

    if habit_log is None:
        raise ValueError("Habit log not found")

    if log_data.completed_value is not None:
        habit_log.completed_value = log_data.completed_value

    if log_data.is_completed is not None:
        habit_log.is_completed = log_data.is_completed

    db.commit()
    db.refresh(habit_log)

    return habit_log


def delete_habit_log(
    db: Session,
    current_user: User,
    habit_id: int,
    log_id: int,
) -> None:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    habit_log = db.query(HabitLog).filter(
        HabitLog.id == log_id,
        HabitLog.habit_id == habit_id,
        HabitLog.user_id == current_user.id,
    ).first()

    if habit_log is None:
        raise ValueError("Habit log not found")

    db.delete(habit_log)
    db.commit()


def complete_habit(
    db: Session,
    current_user: User,
    habit_id: int,
    log_date: date,
) -> HabitLog:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    habit_log = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.user_id == current_user.id,
        HabitLog.log_date == log_date,
    ).first()

    if habit_log is None:
        habit_log = HabitLog(
            habit_id=habit_id,
            user_id=current_user.id,
            log_date=log_date,
            is_completed=True,
        )
        db.add(habit_log)
    else:
        habit_log.is_completed = True

    db.commit()
    db.refresh(habit_log)

    recalculate_for_date(
        db=db,
        current_user=current_user,
        score_date=log_date,
    )

    return habit_log


def undo_habit(
    db: Session,
    current_user: User,
    habit_id: int,
    log_date: date,
) -> HabitLog:
    get_user_habit(
        db=db,
        current_user=current_user,
        habit_id=habit_id,
    )

    habit_log = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.user_id == current_user.id,
        HabitLog.log_date == log_date,
    ).first()

    if habit_log is None:
        habit_log = HabitLog(
            habit_id=habit_id,
            user_id=current_user.id,
            log_date=log_date,
            is_completed=False,
        )
        db.add(habit_log)
    else:
        habit_log.is_completed = False

    db.commit()
    db.refresh(habit_log)

    recalculate_for_date(
        db=db,
        current_user=current_user,
        score_date=log_date,
    )

    return habit_log