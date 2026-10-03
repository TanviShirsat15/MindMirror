from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogRead, HabitLogUpdate
from app.services.habit_log_service import (
    create_habit_log,
    delete_habit_log,
    list_habit_logs,
    update_habit_log,
)

router = APIRouter(
    prefix="/api/habit-logs",
    tags=["Habit Logs"],
)


@router.post(
    "/{habit_id}",
    response_model=HabitLogRead,
    status_code=status.HTTP_201_CREATED,
)
def create_habit_log_endpoint(
    habit_id: int,
    log_data: HabitLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_habit_log(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            log_data=log_data,
        )
    except ValueError as exc:
        if str(exc).startswith("A log already exists"):
            raise HTTPException(
                status_code=409,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/{habit_id}",
    response_model=list[HabitLogRead],
)
def get_habit_logs(
    habit_id: int,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return list_habit_logs(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put(
    "/{habit_id}/{log_id}",
    response_model=HabitLogRead,
)
def update_habit_log_endpoint(
    habit_id: int,
    log_id: int,
    log_data: HabitLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_habit_log(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            log_id=log_id,
            log_data=log_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{habit_id}/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_habit_log_endpoint(
    habit_id: int,
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_habit_log(
            db=db,
            current_user=current_user,
            habit_id=habit_id,
            log_id=log_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

