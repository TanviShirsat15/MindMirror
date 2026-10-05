from collections import defaultdict
from datetime import date, timedelta
from statistics import mean

from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.journal import Journal
from app.models.journal_analysis import JournalAnalysis
from app.models.user import User
from app.models.wellbeing_score import WellBeingScore


MAX_DAILY_RANGE_DAYS = 366
MIN_ASSOCIATION_DAYS = 7
BASELINE_NEAR_TOLERANCE = 5.0


def _validate_date_range(
    start_date: date | None,
    end_date: date | None,
) -> tuple[date, date]:
    today = date.today()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = end_date - timedelta(days=29)

    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    return start_date, end_date


def _validate_daily_range(
    start_date: date,
    end_date: date,
) -> None:
    range_days = (end_date - start_date).days + 1

    if range_days > MAX_DAILY_RANGE_DAYS:
        raise ValueError(
            f"Daily analytics range cannot exceed "
            f"{MAX_DAILY_RANGE_DAYS} days"
        )


def _date_rows(
    start_date: date,
    end_date: date,
) -> list[date]:
    total_days = (end_date - start_date).days + 1

    return [
        start_date + timedelta(days=offset)
        for offset in range(total_days)
    ]


def _iso_week_start(value: date) -> date:
    return value - timedelta(days=value.weekday())


def _iso_month_start(value: date) -> date:
    return value.replace(day=1)


def _next_month_start(value: date) -> date:
    if value.month == 12:
        return date(value.year + 1, 1, 1)

    return date(value.year, value.month + 1, 1)


def _period_end_for_week(
    week_start: date,
) -> date:
    return week_start + timedelta(days=6)


def _period_end_for_month(
    month_start: date,
) -> date:
    return _next_month_start(month_start) - timedelta(days=1)


def _build_periods(
    start_date: date,
    end_date: date,
    granularity: str,
) -> list[tuple[date, date]]:
    if granularity == "weekly":
        first_period = _iso_week_start(start_date)
        last_period = _iso_week_start(end_date)

        periods = []
        current = first_period

        while current <= last_period:
            periods.append(
                (
                    current,
                    _period_end_for_week(current),
                )
            )
            current += timedelta(days=7)

        return periods

    if granularity == "monthly":
        first_period = _iso_month_start(start_date)
        last_period = _iso_month_start(end_date)

        periods = []
        current = first_period

        while current <= last_period:
            periods.append(
                (
                    current,
                    _period_end_for_month(current),
                )
            )
            current = _next_month_start(current)

        return periods

    raise ValueError(
        "granularity must be daily, weekly, or monthly"
    )


def _period_is_partial(
    period_start: date,
    period_end: date,
    selected_start: date,
    selected_end: date,
) -> bool:
    return (
        period_start < selected_start
        or period_end > selected_end
    )


def _aggregate_numeric_values(
    values: list[float],
) -> dict:
    if not values:
        return {
            "average": None,
            "minimum": None,
            "maximum": None,
            "sample_size": 0,
        }

    return {
        "average": round(mean(values), 1),
        "minimum": min(values),
        "maximum": max(values),
        "sample_size": len(values),
    }


def get_wellbeing_daily(
    db: Session,
    current_user: User,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    start_date, end_date = _validate_date_range(
        start_date,
        end_date,
    )

    _validate_daily_range(start_date, end_date)

    scores = (
        db.query(WellBeingScore)
        .filter(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date >= start_date,
            WellBeingScore.score_date <= end_date,
        )
        .order_by(WellBeingScore.score_date)
        .all()
    )

    score_by_date = {
        score.score_date: score
        for score in scores
    }

    rows = []

    for current_date in _date_rows(start_date, end_date):
        score = score_by_date.get(current_date)

        if score is None:
            rows.append(
                {
                    "date": current_date,
                    "score": None,
                    "baseline": None,
                    "difference": None,
                    "comparison": None,
                    "baseline_status": "no_score",
                }
            )
            continue

        baseline = (
            float(score.baseline_value)
            if score.baseline_value is not None
            else None
        )

        difference = (
            round(float(score.score) - baseline, 1)
            if baseline is not None
            else None
        )

        if baseline is None:
            baseline_status = "insufficient_history"
            comparison = None
        elif difference is not None and difference > BASELINE_NEAR_TOLERANCE:
            baseline_status = "baseline_available"
            comparison = "above"
        elif difference is not None and difference < -BASELINE_NEAR_TOLERANCE:
            baseline_status = "baseline_available"
            comparison = "below"
        else:
            baseline_status = "baseline_available"
            comparison = "near"

        rows.append(
            {
                "date": current_date,
                "score": score.score,
                "baseline": baseline,
                "difference": difference,
                "comparison": comparison,
                "baseline_status": baseline_status,
            }
        )

    return rows


def get_wellbeing_aggregate(
    db: Session,
    current_user: User,
    start_date: date,
    end_date: date,
    granularity: str,
) -> list[dict]:
    periods = _build_periods(
        start_date,
        end_date,
        granularity,
    )

    scores = (
        db.query(WellBeingScore)
        .filter(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date >= start_date,
            WellBeingScore.score_date <= end_date,
            WellBeingScore.score >= 1,
            WellBeingScore.score <= 100,
        )
        .order_by(WellBeingScore.score_date)
        .all()
    )

    scores_by_date = {
        score.score_date: score
        for score in scores
    }

    rows = []

    for period_start, period_end in periods:
        selected_dates = [
            current_date
            for current_date in _date_rows(
                max(period_start, start_date),
                min(period_end, end_date),
            )
        ]

        period_scores = [
            scores_by_date[current_date].score
            for current_date in selected_dates
            if current_date in scores_by_date
        ]

        aggregate = _aggregate_numeric_values(
            [float(value) for value in period_scores]
        )

        rows.append(
            {
                "period": (
                    f"{period_start.year}-W"
                    f"{period_start.isocalendar().week:02d}"
                    if granularity == "weekly"
                    else period_start.strftime("%Y-%m")
                ),
                "period_start": max(period_start, start_date),
                "period_end": min(period_end, end_date),
                "average": aggregate["average"],
                "minimum": aggregate["minimum"],
                "maximum": aggregate["maximum"],
                "sample_size": aggregate["sample_size"],
                "is_partial_period": _period_is_partial(
                    period_start,
                    period_end,
                    start_date,
                    end_date,
                ),
            }
        )

    return rows


def get_wellbeing_summary(
    db: Session,
    current_user: User,
    start_date: date,
    end_date: date,
) -> dict:
    scores = (
        db.query(WellBeingScore)
        .filter(
            WellBeingScore.user_id == current_user.id,
            WellBeingScore.score_date >= start_date,
            WellBeingScore.score_date <= end_date,
            WellBeingScore.score >= 1,
            WellBeingScore.score <= 100,
        )
        .order_by(WellBeingScore.score_date)
        .all()
    )

    values = [score.score for score in scores]

    return {
        "count": len(values),
        "first_scored_date": (
            scores[0].score_date
            if scores
            else None
        ),
        "last_scored_date": (
            scores[-1].score_date
            if scores
            else None
        ),
        "latest_baseline": (
            float(scores[-1].baseline_value)
            if scores
            and scores[-1].baseline_value is not None
            else None
        ),
        "average": (
            round(sum(values) / len(values), 1)
            if values
            else None
        ),
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
        "sample_size": len(values),
    }


def _habit_applicable(
    habit: Habit,
    current_date: date,
) -> bool:
    created_date = habit.created_at.date()

    if created_date > current_date:
        return False

    if habit.deactivated_at is not None:
        if habit.deactivated_at.date() <= current_date:
            return False

    return True


def get_habit_daily(
    db: Session,
    current_user: User,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    start_date, end_date = _validate_date_range(
        start_date,
        end_date,
    )

    _validate_daily_range(start_date, end_date)

    habits = (
        db.query(Habit)
        .filter(Habit.user_id == current_user.id)
        .all()
    )

    logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.user_id == current_user.id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= end_date,
            HabitLog.is_completed.is_(True),
        )
        .all()
    )

    completed_by_date = defaultdict(set)

    for log in logs:
        completed_by_date[log.log_date].add(log.habit_id)

    rows = []

    for current_date in _date_rows(start_date, end_date):
        applicable_habits = [
            habit
            for habit in habits
            if _habit_applicable(habit, current_date)
        ]

        applicable_ids = {
            habit.id
            for habit in applicable_habits
        }

        completed_ids = (
            completed_by_date.get(current_date, set())
            & applicable_ids
        )

        applicable_count = len(applicable_ids)
        completed_count = len(completed_ids)

        completion_rate = (
            round(
                completed_count / applicable_count,
                4,
            )
            if applicable_count
            else None
        )

        rows.append(
            {
                "date": current_date,
                "completed_habits": completed_count,
                "applicable_habits": applicable_count,
                "completion_rate": completion_rate,
            }
        )

    return rows


def get_habit_aggregate(
    db: Session,
    current_user: User,
    start_date: date,
    end_date: date,
    granularity: str,
) -> list[dict]:
    daily_rows = get_habit_daily(
        db=db,
        current_user=current_user,
        start_date=start_date,
        end_date=end_date,
    )

    periods = _build_periods(
        start_date,
        end_date,
        granularity,
    )

    rows = []

    for period_start, period_end in periods:
        selected_rows = [
            row
            for row in daily_rows
            if period_start <= row["date"] <= period_end
        ]

        completed = sum(
            row["completed_habits"]
            for row in selected_rows
        )

        applicable = sum(
            row["applicable_habits"]
            for row in selected_rows
        )

        completion_rate = (
            round(completed / applicable, 4)
            if applicable
            else None
        )

        rows.append(
            {
                "period": (
                    f"{period_start.year}-W"
                    f"{period_start.isocalendar().week:02d}"
                    if granularity == "weekly"
                    else period_start.strftime("%Y-%m")
                ),
                "period_start": max(period_start, start_date),
                "period_end": min(period_end, end_date),
                "completed_habits": completed,
                "applicable_habits": applicable,
                "completion_rate": completion_rate,
                "is_partial_period": _period_is_partial(
                    period_start,
                    period_end,
                    start_date,
                    end_date,
                ),
            }
        )

    return rows


def get_habit_performance(
    db: Session,
    current_user: User,
    start_date: date,
    end_date: date,
) -> list[dict]:
    habits = (
        db.query(Habit)
        .filter(Habit.user_id == current_user.id)
        .order_by(Habit.created_at, Habit.id)
        .all()
    )

    completed_logs = (
        db.query(HabitLog)
        .filter(
            HabitLog.user_id == current_user.id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= end_date,
            HabitLog.is_completed.is_(True),
        )
        .all()
    )

    completed_dates_by_habit = defaultdict(set)

    for log in completed_logs:
        completed_dates_by_habit[log.habit_id].add(
            log.log_date
        )

    rows = []

    for habit in habits:
        applicable_dates = [
            current_date
            for current_date in _date_rows(
                start_date,
                end_date,
            )
            if _habit_applicable(habit, current_date)
        ]

        applicable_count = len(applicable_dates)

        completed_count = sum(
            current_date
            in completed_dates_by_habit.get(habit.id, set())
            for current_date in applicable_dates
        )

        rows.append(
            {
                "habit_id": habit.id,
                "name": habit.name,
                "days_applicable": applicable_count,
                "days_completed": completed_count,
                "completion_rate": (
                    round(
                        completed_count / applicable_count,
                        4,
                    )
                    if applicable_count
                    else None
                ),
            }
        )

    return rows


def get_nlp_daily(
    db: Session,
    current_user: User,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    start_date, end_date = _validate_date_range(
        start_date,
        end_date,
    )

    _validate_daily_range(start_date, end_date)

    analyses = (
        db.query(
            Journal.entry_date,
            JournalAnalysis.sentiment_score,
            JournalAnalysis.positive_emotion_score,
            JournalAnalysis.negative_emotion_score,
            JournalAnalysis.stress_indicator,
        )
        .join(
            JournalAnalysis,
            JournalAnalysis.journal_id == Journal.id,
        )
        .filter(
            Journal.user_id == current_user.id,
            Journal.entry_date >= start_date,
            Journal.entry_date <= end_date,
        )
        .all()
    )

    signals_by_date = defaultdict(list)

    for analysis in analyses:
        signals_by_date[analysis.entry_date].append(
            {
                "sentiment": analysis.sentiment_score,
                "positive_emotion": analysis.positive_emotion_score,
                "negative_emotion": analysis.negative_emotion_score,
                "stress": analysis.stress_indicator,
            }
        )

    rows = []

    for current_date in _date_rows(start_date, end_date):
        values = signals_by_date.get(current_date, [])

        if not values:
            rows.append(
                {
                    "date": current_date,
                    "sentiment": None,
                    "positive_emotion": None,
                    "negative_emotion": None,
                    "stress": None,
                    "sample_size": 0,
                }
            )
            continue

        def mean_signal(key: str):
            signal_values = [
                float(item[key])
                for item in values
                if item[key] is not None
            ]

            if not signal_values:
                return None

            return round(
                sum(signal_values) / len(signal_values),
                4,
            )

        rows.append(
            {
                "date": current_date,
                "sentiment": mean_signal("sentiment"),
                "positive_emotion": mean_signal("positive_emotion"),
                "negative_emotion": mean_signal("negative_emotion"),
                "stress": mean_signal("stress"),
                "sample_size": len(values),
            }
        )

    return rows


def get_nlp_aggregate(
    db: Session,
    current_user: User,
    start_date: date,
    end_date: date,
    granularity: str,
) -> list[dict]:
    daily_rows = get_nlp_daily(
        db=db,
        current_user=current_user,
        start_date=start_date,
        end_date=end_date,
    )

    periods = _build_periods(
        start_date,
        end_date,
        granularity,
    )

    signal_names = [
        "sentiment",
        "positive_emotion",
        "negative_emotion",
        "stress",
    ]

    rows = []

    for period_start, period_end in periods:
        selected_rows = [
            row
            for row in daily_rows
            if period_start <= row["date"] <= period_end
        ]

        row = {
            "period": (
                f"{period_start.year}-W"
                f"{period_start.isocalendar().week:02d}"
                if granularity == "weekly"
                else period_start.strftime("%Y-%m")
            ),
            "period_start": max(period_start, start_date),
            "period_end": min(period_end, end_date),
            "sample_size": sum(
                row["sample_size"]
                for row in selected_rows
            ),
            "is_partial_period": _period_is_partial(
                period_start,
                period_end,
                start_date,
                end_date,
            ),
        }

        for signal_name in signal_names:
            values = [
                float(row[signal_name])
                for row in selected_rows
                if row[signal_name] is not None
            ]

            row[signal_name] = (
                round(mean(values), 4)
                if values
                else None
            )

        rows.append(row)

    return rows


def build_association_message(
    scored_habit_days: int,
    positive_association: bool | None,
) -> str:
    if scored_habit_days < MIN_ASSOCIATION_DAYS:
        return "Not enough data to describe a pattern yet."

    if positive_association is True:
        return (
            "Higher habit completion has been associated with "
            "higher well-being scores."
        )

    if positive_association is False:
        return (
            "Higher habit completion has been associated with "
            "lower well-being scores."
        )

    return "No clear pattern was observed in the selected data."