from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models.user import User
from app.services.analytics_service import (
    get_habit_daily,
    get_nlp_daily,
    get_wellbeing_daily,
)
from app.insights.insight_config import INSIGHT_LOOKBACK_DAYS


@dataclass(frozen=True)
class InsightData:
    as_of: date
    window_start: date
    window_end: date
    wellbeing: list[dict[str, Any]]
    habits: list[dict[str, Any]]
    nlp: list[dict[str, Any]]


def load_insight_data(
    db: Session,
    current_user: User,
    as_of: date | None = None,
) -> InsightData:
    """
    Load one bounded historical window for Phase 13 insights.

    The loader reuses Phase 12 daily analytics and never returns
    raw journal content.
    """
    if as_of is None:
        as_of = date.today()

    if as_of > date.today():
        raise ValueError("as_of cannot be in the future")

    window_end = as_of
    window_start = as_of - timedelta(days=INSIGHT_LOOKBACK_DAYS - 1)

    wellbeing = get_wellbeing_daily(
        db=db,
        current_user=current_user,
        start_date=window_start,
        end_date=window_end,
    )

    habits = get_habit_daily(
        db=db,
        current_user=current_user,
        start_date=window_start,
        end_date=window_end,
    )

    nlp = get_nlp_daily(
        db=db,
        current_user=current_user,
        start_date=window_start,
        end_date=window_end,
    )

    return InsightData(
        as_of=as_of,
        window_start=window_start,
        window_end=window_end,
        wellbeing=wellbeing,
        habits=habits,
        nlp=nlp,
    )
