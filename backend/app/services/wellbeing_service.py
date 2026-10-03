from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.wellbeing_score import WellBeingScore
from app.schemas.wellbeing_score import (
    WellBeingScoreCreate,
    WellBeingScoreUpdate,
)


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