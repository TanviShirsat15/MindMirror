from datetime import date

from sqlalchemy.orm import Session

from app.models.journal import Journal
from app.models.journal_analysis import JournalAnalysis
from app.models.user import User
from app.schemas.journal import JournalCreate, JournalUpdate
from app.services.nlp.analysis_service import analyze_journal_text
from app.services.wellbeing_service import recalculate_for_date


def _create_journal_analysis(
    db: Session,
    journal: Journal,
) -> None:
    """Create NLP analysis for a journal entry."""
    analysis_result = analyze_journal_text(journal.content)

    analysis = JournalAnalysis(
        journal_id=journal.id,
        sentiment_score=analysis_result["sentiment_score"],
        stress_indicator=analysis_result["stress_indicator"],
        positive_emotion_score=analysis_result["positive_emotion_score"],
        negative_emotion_score=analysis_result["negative_emotion_score"],
    )

    db.add(analysis)


def _update_journal_analysis(
    db: Session,
    journal: Journal,
) -> None:
    """Recalculate and update NLP analysis for a journal entry."""
    analysis_result = analyze_journal_text(journal.content)

    analysis = db.query(JournalAnalysis).filter(
        JournalAnalysis.journal_id == journal.id,
    ).first()

    if analysis is None:
        analysis = JournalAnalysis(
            journal_id=journal.id,
        )
        db.add(analysis)

    analysis.sentiment_score = analysis_result["sentiment_score"]
    analysis.stress_indicator = analysis_result["stress_indicator"]
    analysis.positive_emotion_score = analysis_result[
        "positive_emotion_score"
    ]
    analysis.negative_emotion_score = analysis_result[
        "negative_emotion_score"
    ]


def create_journal(
    db: Session,
    current_user: User,
    journal_data: JournalCreate,
) -> Journal:
    entry_date = journal_data.entry_date or date.today()

    journal = Journal(
        user_id=current_user.id,
        content=journal_data.content,
        entry_date=entry_date,
    )

    db.add(journal)
    db.flush()

    _create_journal_analysis(
        db=db,
        journal=journal,
    )

    db.commit()
    db.refresh(journal)

    recalculate_for_date(
        db=db,
        current_user=current_user,
        score_date=journal.entry_date,
    )

    return journal


def list_journals(
    db: Session,
    current_user: User,
    entry_date: date | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Journal]:
    query = db.query(Journal).filter(
        Journal.user_id == current_user.id
    )

    if entry_date is not None:
        query = query.filter(Journal.entry_date == entry_date)

    if start_date is not None:
        query = query.filter(Journal.entry_date >= start_date)

    if end_date is not None:
        query = query.filter(Journal.entry_date <= end_date)

    return query.order_by(
        Journal.entry_date.desc(),
        Journal.created_at.desc(),
    ).all()


def get_journal(
    db: Session,
    current_user: User,
    journal_id: int,
) -> Journal:
    journal = db.query(Journal).filter(
        Journal.id == journal_id,
        Journal.user_id == current_user.id,
    ).first()

    if journal is None:
        raise ValueError("Journal not found")

    return journal


def update_journal(
    db: Session,
    current_user: User,
    journal_id: int,
    journal_data: JournalUpdate,
) -> Journal:
    journal = get_journal(
        db=db,
        current_user=current_user,
        journal_id=journal_id,
    )

    old_entry_date = journal.entry_date

    if journal_data.content is not None:
        journal.content = journal_data.content

    if journal_data.entry_date is not None:
        journal.entry_date = journal_data.entry_date

    _update_journal_analysis(
        db=db,
        journal=journal,
    )

    db.commit()
    db.refresh(journal)

    recalculate_for_date(
        db=db,
        current_user=current_user,
        score_date=journal.entry_date,
    )

    if old_entry_date != journal.entry_date:
        recalculate_for_date(
            db=db,
            current_user=current_user,
            score_date=old_entry_date,
        )

    return journal


def delete_journal(
    db: Session,
    current_user: User,
    journal_id: int,
) -> None:
    journal = get_journal(
        db=db,
        current_user=current_user,
        journal_id=journal_id,
    )

    entry_date = journal.entry_date

    db.delete(journal)
    db.commit()

    recalculate_for_date(
        db=db,
        current_user=current_user,
        score_date=entry_date,
    )


def get_journal_analysis(
    db: Session,
    current_user: User,
    journal_id: int,
) -> JournalAnalysis:
    journal = get_journal(
        db=db,
        current_user=current_user,
        journal_id=journal_id,
    )

    analysis = db.query(JournalAnalysis).filter(
        JournalAnalysis.journal_id == journal.id,
    ).first()

    if analysis is None:
        raise ValueError("Journal analysis not found")

    return analysis