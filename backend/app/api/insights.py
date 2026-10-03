from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.insight import (
    InsightCreate,
    InsightRead,
    InsightUpdate,
)
from app.services.insight_service import (
    create_insight,
    delete_insight,
    get_insight,
    list_insights,
    update_insight,
)


router = APIRouter(
    prefix="/api/insights",
    tags=["Insights"],
)


@router.post(
    "",
    response_model=InsightRead,
    status_code=status.HTTP_201_CREATED,
)
def create_insight_endpoint(
    insight_data: InsightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_insight(
        db=db,
        current_user=current_user,
        insight_data=insight_data,
    )


@router.get(
    "",
    response_model=list[InsightRead],
)
def get_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_insights(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{insight_id}",
    response_model=InsightRead,
)
def get_insight_endpoint(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_insight(
            db=db,
            current_user=current_user,
            insight_id=insight_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put(
    "/{insight_id}",
    response_model=InsightRead,
)
def update_insight_endpoint(
    insight_id: int,
    insight_data: InsightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_insight(
            db=db,
            current_user=current_user,
            insight_id=insight_id,
            insight_data=insight_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{insight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_insight_endpoint(
    insight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_insight(
            db=db,
            current_user=current_user,
            insight_id=insight_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc