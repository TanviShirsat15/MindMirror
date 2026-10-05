from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.wellbeing_service import (
    _calculate_personal_baseline,
    _get_baseline_comparison,
    get_score_for_date,
    list_scores,
)

router = APIRouter(
    prefix="/api/wellbeing",
    tags=["Well-being"],
)


@router.get("/{score_date}")
def get_wellbeing_for_date(
    score_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return the user's well-being score and personal baseline information
    for a specific date.
    """

    score = get_score_for_date(
        db=db,
        current_user=current_user,
        score_date=score_date,
    )

    if score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Well-being analysis is not available for this date",
        )

    baseline, sample_size = _calculate_personal_baseline(
        db=db,
        current_user=current_user,
        score_date=score_date,
    )

    comparison_status, comparison, difference = _get_baseline_comparison(
        score=float(score.score),
        baseline=baseline,
        sample_size=sample_size,
    )

    history = list_scores(
        db=db,
        current_user=current_user,
    )

    compact_history = [
        {
            "date": item.score_date.isoformat(),
            "score": int(item.score),
        }
        for item in history[:7]
    ]

    return {
        "date": score.score_date.isoformat(),
        "status": comparison_status,
        "score": int(score.score),
        "baseline": baseline,
        "difference": difference,
        "comparison": comparison,
        "baseline_sample_size": sample_size,
        "history": compact_history,
    }