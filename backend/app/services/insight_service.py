from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.insight import Insight
from app.models.user import User
from app.schemas.insight import InsightCreate, InsightUpdate


def create_insight(
    db: Session,
    current_user: User,
    insight_data: InsightCreate,
) -> Insight:
    insight_date = insight_data.insight_date or date.today()

    insight = Insight(
        user_id=current_user.id,
        insight_date=insight_date,
        content=insight_data.content,
    )

    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight


def list_insights(
    db: Session,
    current_user: User,
) -> list[Insight]:
    query = (
        select(Insight)
        .where(Insight.user_id == current_user.id)
        .order_by(Insight.created_at.desc(), Insight.id.desc())
    )

    return list(db.scalars(query).all())


def get_insight(
    db: Session,
    current_user: User,
    insight_id: int,
) -> Insight:
    insight = db.scalar(
        select(Insight).where(
            Insight.id == insight_id,
            Insight.user_id == current_user.id,
        )
    )

    if insight is None:
        raise ValueError("Insight not found")

    return insight


def update_insight(
    db: Session,
    current_user: User,
    insight_id: int,
    insight_data: InsightUpdate,
) -> Insight:
    insight = get_insight(
        db=db,
        current_user=current_user,
        insight_id=insight_id,
    )

    if insight_data.insight_date is not None:
        insight.insight_date = insight_data.insight_date

    if insight_data.content is not None:
        insight.content = insight_data.content

    db.commit()
    db.refresh(insight)

    return insight


def delete_insight(
    db: Session,
    current_user: User,
    insight_id: int,
) -> None:
    insight = get_insight(
        db=db,
        current_user=current_user,
        insight_id=insight_id,
    )

    db.delete(insight)
    db.commit()