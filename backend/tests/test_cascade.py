from sqlalchemy import select

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.insight import Insight
from app.models.journal import Journal
from app.models.user import User
from app.models.wellbeing_score import WellBeingScore


def test_user_cascade_deletes_related_data(db_session):
    user = User(
        email="cascade_test@mindmirror.com",
        password_hash="test_hash",
        full_name="Cascade Test User",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    journal = Journal(
        user_id=user.id,
        content="Cascade test journal",
        entry_date="2026-10-03",
    )

    habit = Habit(
        user_id=user.id,
        name="Cascade Habit",
        target_value=1,
        target_unit="time",
        is_active=True,
    )

    score = WellBeingScore(
        user_id=user.id,
        score_date="2026-10-03",
        score=75,
    )

    insight = Insight(
        user_id=user.id,
        insight_date="2026-10-03",
        content="Cascade test insight",
    )

    db_session.add_all([
        journal,
        habit,
        score,
        insight,
    ])
    db_session.commit()
    db_session.refresh(habit)

    habit_log = HabitLog(
        habit_id=habit.id,
        user_id=user.id,
        log_date="2026-10-03",
        completed_value=1,
        is_completed=True,
    )

    db_session.add(habit_log)
    db_session.commit()

    user_id = user.id

    db_session.delete(user)
    db_session.commit()

    assert db_session.scalar(
        select(Journal).where(Journal.user_id == user_id)
    ) is None

    assert db_session.scalar(
        select(Habit).where(Habit.user_id == user_id)
    ) is None

    assert db_session.scalar(
        select(HabitLog).where(HabitLog.user_id == user_id)
    ) is None

    assert db_session.scalar(
        select(WellBeingScore).where(WellBeingScore.user_id == user_id)
    ) is None

    assert db_session.scalar(
        select(Insight).where(Insight.user_id == user_id)
    ) is None