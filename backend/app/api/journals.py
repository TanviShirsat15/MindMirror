from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.journal import JournalCreate, JournalRead, JournalUpdate
from app.schemas.journal_analysis import JournalAnalysisRead
from app.services.journal_service import (
    create_journal,
    delete_journal,
    get_journal,
    get_journal_analysis,
    list_journals,
    update_journal,
)


router = APIRouter(
    prefix="/api/journals",
    tags=["Journals"],
)


@router.post(
    "",
    response_model=JournalRead,
    status_code=status.HTTP_201_CREATED,
)
def create_journal_endpoint(
    journal_data: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_journal(
        db=db,
        current_user=current_user,
        journal_data=journal_data,
    )


@router.get(
    "",
    response_model=list[JournalRead],
)
def get_journals(
    entry_date: date | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_journals(
        db=db,
        current_user=current_user,
        entry_date=entry_date,
        start_date=start_date,
        end_date=end_date,
    )


@router.get(
    "/{journal_id}",
    response_model=JournalRead,
)
def get_journal_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_journal(
            db=db,
            current_user=current_user,
            journal_id=journal_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.put(
    "/{journal_id}",
    response_model=JournalRead,
)
def update_journal_endpoint(
    journal_id: int,
    journal_data: JournalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_journal(
            db=db,
            current_user=current_user,
            journal_id=journal_id,
            journal_data=journal_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{journal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_journal_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_journal(
            db=db,
            current_user=current_user,
            journal_id=journal_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/{journal_id}/analysis",
    response_model=JournalAnalysisRead,
)
def get_journal_analysis_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_journal_analysis(
            db=db,
            current_user=current_user,
            journal_id=journal_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc