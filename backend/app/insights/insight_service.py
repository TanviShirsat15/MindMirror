from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.insights.insight_config import INSIGHT_MAX_DISPLAY
from app.insights.insight_data import load_insight_data
from app.insights.insight_ranking import (
    deduplicate_insights,
    insight_key,
    rank_insights,
)
from app.insights.insight_rules import (
    baseline_comparison_rule,
    recent_change_rule,
    recent_pattern_rule,
    trend_rule,
)
from app.insights.habit_rules import (
    consistency_rule,
    habit_association_rule,
)
from app.insights.nlp_rules import nlp_signal_trend_rule
from app.insights.insight_templates import render_insight
from app.insights.insight_types import (
    DataSufficiency,
    InsightCategory,
    InsightResult,
)
from app.models.insight_snapshot import InsightSnapshot
from app.models.user import User


def _supporting_value(result: Any) -> float | None:
    metrics = result.supporting_metrics

    for key in (
        "difference",
        "score_difference",
        "completion_gap",
        "rho",
        "standard_deviation",
    ):
        value = metrics.get(key)

        if isinstance(value, (int, float)):
            return float(value)

    return None


def _value_bucket(result: Any) -> int:
    value = _supporting_value(result)

    if value is None:
        return 0

    threshold = float(result.supporting_metrics.get("threshold", 1.0))

    if threshold <= 0:
        threshold = 1.0

    bucket_width = threshold / 2

    return int(abs(value) / bucket_width)


def _load_snapshot(
    db: Session,
    current_user: User,
    key: str,
) -> InsightSnapshot | None:
    return (
        db.query(InsightSnapshot)
        .filter(
            InsightSnapshot.user_id == current_user.id,
            InsightSnapshot.insight_key == key,
        )
        .first()
    )


def _is_new(
    snapshot: InsightSnapshot | None,
    result: Any,
) -> bool:
    if snapshot is None:
        return True

    if snapshot.direction != result.direction.value:
        return True

    return snapshot.value_bucket != _value_bucket(result)


def _persist_snapshot(
    db: Session,
    current_user: User,
    result: Any,
    as_of: date,
) -> bool:
    key = insight_key(result)
    now = datetime.utcnow()
    bucket = _value_bucket(result)
    value = _supporting_value(result)

    snapshot = _load_snapshot(db, current_user, key)

    try:
        if snapshot is None:
            snapshot = InsightSnapshot(
                user_id=current_user.id,
                insight_key=key,
                category=result.category.value,
                subject=result.subject,
                direction=result.direction.value,
                window_start=as_of - timedelta(days=59),
                window_end=as_of,
                supporting_value=value,
                value_bucket=bucket,
                sample_size=result.sample_size,
                first_generated_at=now,
                last_changed_at=now,
                last_generated_at=now,
            )
            db.add(snapshot)

        else:
            changed = (
                snapshot.direction != result.direction.value
                or snapshot.value_bucket != bucket
            )

            snapshot.window_start = as_of - timedelta(days=59)
            snapshot.window_end = as_of
            snapshot.supporting_value = value
            snapshot.value_bucket = bucket
            snapshot.sample_size = result.sample_size
            snapshot.last_generated_at = now

            if changed:
                snapshot.last_changed_at = now

        db.commit()
        return True

    except IntegrityError:
        db.rollback()
        return False


def generate_insights(
    db: Session,
    current_user: User,
    as_of: date | None = None,
) -> dict[str, Any]:
    if as_of is None:
        as_of = date.today()

    if as_of > date.today():
        raise ValueError("as_of cannot be in the future")

    data = load_insight_data(
        db=db,
        current_user=current_user,
        as_of=as_of,
    )

    results = []

    rule_calls = [
        lambda: baseline_comparison_rule(data.wellbeing, data.as_of),
        lambda: recent_pattern_rule(data.wellbeing, data.as_of),
        lambda: recent_change_rule(data.wellbeing, data.as_of),
        lambda: trend_rule(data.wellbeing, data.as_of),
        lambda: habit_association_rule(data.wellbeing, data.habits),
        lambda: consistency_rule(data.habits),
        lambda: nlp_signal_trend_rule(data.nlp, data.as_of),
    ]

    for rule in rule_calls:
        try:
            result = rule()

            if result is not None:
                results.append(result)

        except (ValueError, KeyError, TypeError):
            continue

    results = [
        result
        for result in results
        if result.data_sufficiency == DataSufficiency.SUFFICIENT_MEANINGFUL
    ]

    results = deduplicate_insights(results)
    results = rank_insights(results)

    selected = []
    seen_categories = set()

    for result in results:
        category = result.category.value

        if category in seen_categories:
            continue

        seen_categories.add(category)
        selected.append(result)

        if len(selected) >= INSIGHT_MAX_DISPLAY:
            break

    insights = []

    for result in selected:
        key = insight_key(result)
        snapshot = _load_snapshot(db, current_user, key)
        is_new = _is_new(snapshot, result)

        _persist_snapshot(
            db=db,
            current_user=current_user,
            result=result,
            as_of=as_of,
        )

        title, explanation = render_insight(result)

        insights.append(
        InsightResult(
        insight_key=key,
        category=result.category,
        subject=result.subject,
        title=title,
        explanation=explanation,
        direction=result.direction,
        supporting_metrics=result.supporting_metrics,
        comparison_period=result.comparison_period,
        data_sufficiency=result.data_sufficiency,
        sample_size=result.sample_size,
        is_new=is_new,
        first_generated_at=(
            snapshot.first_generated_at if snapshot else None
        ),
        generated_at=datetime.utcnow(),
    )
)

    return {
        "status": "success",
        "as_of": as_of,
        "generated_at": datetime.utcnow(),
        "insights": insights,
        "meta": {
            "disclaimer": (
                "Insights describe patterns in your own historical data "
                "and are not medical or clinical measurements or advice."
            ),
        },
    }