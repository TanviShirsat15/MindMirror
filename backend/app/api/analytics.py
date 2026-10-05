from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.analytics_service import (
    get_habit_aggregate,
    get_habit_daily,
    get_habit_performance,
    get_nlp_aggregate,
    get_nlp_daily,
    get_wellbeing_aggregate,
    get_wellbeing_daily,
    get_wellbeing_summary,
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


def _resolve_range(
    start_date: date | None,
    end_date: date | None,
) -> tuple[date, date]:
    resolved_end = end_date or date.today()
    resolved_start = start_date or (
        resolved_end.fromordinal(resolved_end.toordinal() - 29)
    )

    return resolved_start, resolved_end


@router.get("/wellbeing")
def get_wellbeing_analytics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    granularity: Literal["daily", "weekly", "monthly"] = Query(
        default="daily"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        resolved_start, resolved_end = _resolve_range(
            start_date,
            end_date,
        )

        if granularity == "daily":
            data = get_wellbeing_daily(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
            )
        else:
            data = get_wellbeing_aggregate(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
                granularity=granularity,
            )

        summary = get_wellbeing_summary(
            db=db,
            current_user=current_user,
            start_date=resolved_start,
            end_date=resolved_end,
        )

        return {
            "meta": {
                "start_date": resolved_start,
                "end_date": resolved_end,
                "granularity": granularity,
            },
            "summary": summary,
            "data": data,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/habits")
def get_habit_analytics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    granularity: Literal["daily", "weekly", "monthly"] = Query(
        default="daily"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        resolved_start, resolved_end = _resolve_range(
            start_date,
            end_date,
        )

        if granularity == "daily":
            data = get_habit_daily(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
            )
        else:
            data = get_habit_aggregate(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
                granularity=granularity,
            )

        performance = get_habit_performance(
            db=db,
            current_user=current_user,
            start_date=resolved_start,
            end_date=resolved_end,
        )

        return {
            "meta": {
                "start_date": resolved_start,
                "end_date": resolved_end,
                "granularity": granularity,
            },
            "data": data,
            "habit_performance": performance,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/nlp")
def get_nlp_analytics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    granularity: Literal["daily", "weekly", "monthly"] = Query(
        default="daily"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        resolved_start, resolved_end = _resolve_range(
            start_date,
            end_date,
        )

        if granularity == "daily":
            data = get_nlp_daily(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
            )
        else:
            data = get_nlp_aggregate(
                db=db,
                current_user=current_user,
                start_date=resolved_start,
                end_date=resolved_end,
                granularity=granularity,
            )

        return {
            "meta": {
                "start_date": resolved_start,
                "end_date": resolved_end,
                "granularity": granularity,
            },
            "data": data,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc