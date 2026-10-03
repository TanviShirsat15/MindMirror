from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.wellbeing_score import (
    WellBeingScoreCreate,
    WellBeingScoreRead,
    WellBeingScoreUpdate,
)
from app.services.wellbeing_service import (
    create_score,
    delete_score,
    get_score,
    list_scores,
    update_score,
)


router = APIRouter(
    prefix="/api/wellbeing-scores",
    tags=["Well-Being Scores"],
)


@router.post(
    "",
    response_model=WellBeingScoreRead,
    status_code=status.HTTP_201_CREATED,
)
def create_score_endpoint(
    score_data: WellBeingScoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_score(
            db=db,
            current_user=current_user,
            score_data=score_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[WellBeingScoreRead],
)
def get_scores(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_scores(
        db=db,
        current_user=current_user,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/{score_id}",
    response_model=WellBeingScoreRead,
)
def get_score_endpoint(
    score_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_score(
            db=db,
            current_user=current_user,
            score_id=score_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put(
    "/{score_id}",
    response_model=WellBeingScoreRead,
)
def update_score_endpoint(
    score_id: int,
    score_data: WellBeingScoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_score(
            db=db,
            current_user=current_user,
            score_id=score_id,
            score_data=score_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{score_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_score_endpoint(
    score_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_score(
            db=db,
            current_user=current_user,
            score_id=score_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
