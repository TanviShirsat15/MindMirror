from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.wellbeing_service import get_score_for_date


router = APIRouter(
    prefix="/api/wellbeing",
    tags=["Well-Being"],
)


@router.get("/{score_date}")
def get_wellbeing_by_date(
    score_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    score = get_score_for_date(
        db=db,
        current_user=current_user,
        score_date=score_date,
    )

    if score is None:
        raise HTTPException(
            status_code=404,
            detail="Well-being analysis is unavailable for this date",
        )

    return {
        "date": score.score_date,
        "score": score.score,
    }