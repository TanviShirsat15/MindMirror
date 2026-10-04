from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_log import HabitLogRead
from app.services.habit_log_service import complete_habit, undo_habit
from app.services.habit_service import (
    create_habit,
    delete_habit,
    get_habit,
    get_habit_metrics,
    list_habits,
    update_habit,
)

router = APIRouter(
    prefix="/api/habits",
    tags=["Habits"],
)


@router.post(
    "",
    response_model=HabitRead,
    status_code=status.HTTP_201_CREATED,
)
def create_habit_endpoint(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_habit(
        db=db,
        current_user=current_user,
        habit_data=habit_data,
    )


@router.get(
    "",
    response_model=list[HabitRead],
)
def get_habits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_habits(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{habit_id}",
    response_model=HabitRead,
)
def get_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_habit(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/{habit_id}/metrics",
)
def get_habit_metrics_endpoint(
    habit_id: int,
    window: str = Query(default="weekly"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_habit_metrics(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            window=window,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.post(
    "/{habit_id}/complete",
    response_model=HabitLogRead,
)
def complete_habit_endpoint(
    habit_id: int,
    log_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return complete_habit(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            log_date=log_date or date.today(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.post(
    "/{habit_id}/undo",
    response_model=HabitLogRead,
)
def undo_habit_endpoint(
    habit_id: int,
    log_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return undo_habit(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            log_date=log_date or date.today(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put(
    "/{habit_id}",
    response_model=HabitRead,
)
def update_habit_endpoint(
    habit_id: int,
    habit_data: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_habit(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            habit_data=habit_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_habit(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc