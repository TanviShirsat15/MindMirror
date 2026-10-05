from app.insights.insight_config import CATEGORY_WEIGHTS
from app.insights.insight_types import (
    InsightCategory,
    InsightDirection,
    RuleResult,
)


def _magnitude_ratio(result: RuleResult) -> float:
    metrics = result.supporting_metrics
    difference = abs(float(metrics.get("difference", 0)))
    threshold = float(metrics.get("threshold", 0))

    if threshold <= 0:
        return 0.0

    return min(difference / threshold, 3.0)


def _recent_change_difference(result: RuleResult) -> float:
    return abs(float(result.supporting_metrics.get("difference", 0)))


def _recent_change_threshold(result: RuleResult) -> float:
    return float(result.supporting_metrics.get("threshold", 0))


def insight_rank_key(result: RuleResult) -> tuple:
    return (
        CATEGORY_WEIGHTS.get(result.category.value, 0),
        _magnitude_ratio(result),
        result.sample_size,
        result.category.value,
        result.subject,
        result.direction.value,
    )


def rank_insights(results: list[RuleResult]) -> list[RuleResult]:
    return sorted(results, key=insight_rank_key, reverse=True)


def insight_key(result: RuleResult) -> str:
    return (
        f"{result.category.value}:"
        f"{result.subject}:"
        f"{result.direction.value}:60d"
    )


def _apply_trend_recent_change_rule(
    results: list[RuleResult],
) -> list[RuleResult]:
    trend_results = [
        result
        for result in results
        if result.category == InsightCategory.TREND
    ]

    recent_results = [
        result
        for result in results
        if result.category == InsightCategory.RECENT_CHANGE
    ]

    if not trend_results or not recent_results:
        return results

    remove_recent_change: set[int] = set()

    for trend in trend_results:
        for recent in recent_results:
            if trend.direction != recent.direction:
                continue

            threshold = _recent_change_threshold(recent)

            if threshold <= 0:
                remove_recent_change.add(id(recent))
                continue

            difference = _recent_change_difference(recent)

            if difference < (2 * threshold):
                remove_recent_change.add(id(recent))

    return [
        result
        for result in results
        if id(result) not in remove_recent_change
    ]


def deduplicate_insights(
    results: list[RuleResult],
) -> list[RuleResult]:
    results = _apply_trend_recent_change_rule(results)

    seen: set[str] = set()
    unique: list[RuleResult] = []

    for result in rank_insights(results):
        key = insight_key(result)

        if key in seen:
            continue

        seen.add(key)
        unique.append(result)

    return unique