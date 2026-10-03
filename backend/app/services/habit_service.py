from sqlalchemy.orm import Session

from app.models.habit import Habit
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
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id,
    ).first()

    if habit is None:
        raise ValueError("Habit not found")

    return habit


def update_habit(
    db: Session,
    current_user: User,
    habit_id: int,
    habit_data: HabitUpdate,
) -> Habit:
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id,
    ).first()

    if habit is None:
        raise ValueError("Habit not found")

    if habit_data.name is not None:
        habit.name = habit_data.name

    if habit_data.target_value is not None:
        habit.target_value = habit_data.target_value

    if habit_data.target_unit is not None:
        habit.target_unit = habit_data.target_unit

    if habit_data.is_active is not None:
        habit.is_active = habit_data.is_active

    db.commit()
    db.refresh(habit)

    return habit


def delete_habit(
    db: Session,
    current_user: User,
    habit_id: int,
) -> None:
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id,
    ).first()

    if habit is None:
        raise ValueError("Habit not found")

    db.delete(habit)
    db.commit()