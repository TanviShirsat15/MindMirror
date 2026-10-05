from statistics import mean, stdev
from typing import Any

from app.insights.insight_config import (
    BASELINE_NEAR_TOLERANCE,
    INSIGHT_RECENCY_DAYS,
    MATERIAL_RANGE_FRACTION,
    MATERIAL_SD_FRACTION,
    MIN_VALUES_FOR_SD,
    RECENT_CHANGE_MIN_PER_WINDOW,
    RECENT_WINDOW_DAYS,
    TREND_MIN_PER_HALF,
    TREND_WINDOW_DAYS,
    VALID_SCORE_MAX,
    VALID_SCORE_MIN,
)
from app.insights.insight_types import (
    DataSufficiency,
    InsightCategory,
    InsightDirection,
    InsightReason,
    RuleResult,
)


def _valid_scores(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row.get("score") is not None
        and VALID_SCORE_MIN <= float(row["score"]) <= VALID_SCORE_MAX
    ]


def _material_threshold(values: list[float]) -> float:
    if not values:
        return MATERIAL_RANGE_FRACTION * (
            VALID_SCORE_MAX - VALID_SCORE_MIN
        )

    if len(values) >= MIN_VALUES_FOR_SD:
        sd = stdev(values)
        return max(
            MATERIAL_SD_FRACTION * sd,
            MATERIAL_RANGE_FRACTION * (
                VALID_SCORE_MAX - VALID_SCORE_MIN
            ),
        )

    return MATERIAL_RANGE_FRACTION * (
        VALID_SCORE_MAX - VALID_SCORE_MIN
    )


def _direction_from_difference(
    difference: float,
    threshold: float,
) -> InsightDirection:
    if difference >= threshold:
        return InsightDirection.HIGHER

    if difference <= -threshold:
        return InsightDirection.LOWER

    return InsightDirection.STABLE


def baseline_comparison_rule(
    wellbeing_rows: list[dict[str, Any]],
    as_of,
) -> RuleResult:
    valid = _valid_scores(wellbeing_rows)

    recent = [
        row
        for row in valid
        if 0 <= (as_of - row["date"]).days < INSIGHT_RECENCY_DAYS
    ]

    if not recent:
        return RuleResult(
            category=InsightCategory.BASELINE_COMPARISON,
            subject="wellbeing",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.NO_DATA,
            sample_size=0,
            supporting_metrics={},
            reason=InsightReason.NO_RECENT_SCORES,
        )

    latest = max(recent, key=lambda row: row["date"])

    baseline = latest.get("baseline")

    if baseline is None:
        return RuleResult(
            category=InsightCategory.BASELINE_COMPARISON,
            subject="wellbeing",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(recent),
            supporting_metrics={
                "latest_score": latest["score"],
            },
            reason=InsightReason.INSUFFICIENT_SCORES,
        )

    difference = float(latest["score"]) - float(baseline)

    direction = _direction_from_difference(
        difference,
        BASELINE_NEAR_TOLERANCE,
    )

    if direction == InsightDirection.STABLE:
        sufficiency = DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE
    else:
        sufficiency = DataSufficiency.SUFFICIENT_MEANINGFUL

    return RuleResult(
        category=InsightCategory.BASELINE_COMPARISON,
        subject="wellbeing",
        direction=direction,
        data_sufficiency=sufficiency,
        sample_size=len(recent),
        supporting_metrics={
            "latest_score": float(latest["score"]),
            "personal_baseline": float(baseline),
            "difference": round(difference, 1),
        },
        comparison_period={
            "start": min(row["date"] for row in recent),
            "end": max(row["date"] for row in recent),
        },
    )


def recent_change_rule(
    wellbeing_rows: list[dict[str, Any]],
    as_of,
) -> RuleResult:
    valid = _valid_scores(wellbeing_rows)

    recent = [
        row
        for row in valid
        if 0 <= (as_of - row["date"]).days < RECENT_WINDOW_DAYS
    ]

    previous = [
        row
        for row in valid
        if RECENT_WINDOW_DAYS
        <= (as_of - row["date"]).days
        < RECENT_WINDOW_DAYS * 2
    ]

    if (
        len(recent) < RECENT_CHANGE_MIN_PER_WINDOW
        or len(previous) < RECENT_CHANGE_MIN_PER_WINDOW
    ):
        return RuleResult(
            category=InsightCategory.RECENT_CHANGE,
            subject="wellbeing",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(recent) + len(previous),
            supporting_metrics={
                "recent_sample_size": len(recent),
                "previous_sample_size": len(previous),
            },
            reason=InsightReason.INSUFFICIENT_SCORES,
        )

    recent_mean = mean(float(row["score"]) for row in recent)
    previous_mean = mean(float(row["score"]) for row in previous)
    difference = recent_mean - previous_mean

    threshold = _material_threshold(
        [float(row["score"]) for row in valid]
    )

    direction = _direction_from_difference(difference, threshold)

    sufficiency = (
        DataSufficiency.SUFFICIENT_MEANINGFUL
        if direction != InsightDirection.STABLE
        else DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE
    )

    return RuleResult(
        category=InsightCategory.RECENT_CHANGE,
        subject="wellbeing",
        direction=direction,
        data_sufficiency=sufficiency,
        sample_size=len(recent) + len(previous),
        supporting_metrics={
            "recent_mean": round(recent_mean, 1),
            "previous_mean": round(previous_mean, 1),
            "difference": round(difference, 1),
            "threshold": round(threshold, 2),
        },
        comparison_period={
            "recent_days": RECENT_WINDOW_DAYS,
            "previous_days": RECENT_WINDOW_DAYS,
        },
    )


def trend_rule(
    wellbeing_rows: list[dict[str, Any]],
    as_of,
) -> RuleResult:
    valid = _valid_scores(wellbeing_rows)

    half = TREND_WINDOW_DAYS // 2

    recent_half = [
        row
        for row in valid
        if 0 <= (as_of - row["date"]).days < half
    ]

    previous_half = [
        row
        for row in valid
        if half <= (as_of - row["date"]).days < TREND_WINDOW_DAYS
    ]

    if (
        len(recent_half) < TREND_MIN_PER_HALF
        or len(previous_half) < TREND_MIN_PER_HALF
    ):
        return RuleResult(
            category=InsightCategory.TREND,
            subject="wellbeing",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(recent_half) + len(previous_half),
            supporting_metrics={
                "recent_half_sample_size": len(recent_half),
                "previous_half_sample_size": len(previous_half),
            },
            reason=InsightReason.INSUFFICIENT_SCORES,
        )

    recent_mean = mean(float(row["score"]) for row in recent_half)
    previous_mean = mean(float(row["score"]) for row in previous_half)
    difference = recent_mean - previous_mean

    threshold = _material_threshold(
        [float(row["score"]) for row in valid]
    )

    direction = _direction_from_difference(difference, threshold)

    sufficiency = (
        DataSufficiency.SUFFICIENT_MEANINGFUL
        if direction != InsightDirection.STABLE
        else DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE
    )

    return RuleResult(
        category=InsightCategory.TREND,
        subject="wellbeing",
        direction=direction,
        data_sufficiency=sufficiency,
        sample_size=len(recent_half) + len(previous_half),
        supporting_metrics={
            "recent_mean": round(recent_mean, 1),
            "previous_mean": round(previous_mean, 1),
            "difference": round(difference, 1),
            "threshold": round(threshold, 2),
        },
        comparison_period={
            "window_days": TREND_WINDOW_DAYS,
            "half_days": half,
        },
    )

def recent_pattern_rule(
    wellbeing_rows: list[dict[str, Any]],
    as_of,
) -> RuleResult:
    valid = _valid_scores(wellbeing_rows)

    recent = [
        row
        for row in valid
        if 0 <= (as_of - row["date"]).days < RECENT_WINDOW_DAYS
    ]

    if len(recent) < 3:
        return RuleResult(
            category=InsightCategory.RECENT_CHANGE,
            subject="wellbeing_recent_pattern",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(recent),
            supporting_metrics={
                "recent_sample_size": len(recent),
            },
            reason=InsightReason.INSUFFICIENT_SCORES,
        )

    recent = sorted(recent, key=lambda row: row["date"], reverse=True)[:3]

    baselines = [
        row.get("baseline")
        for row in recent
        if row.get("baseline") is not None
    ]

    if len(baselines) < 3:
        return RuleResult(
            category=InsightCategory.RECENT_CHANGE,
            subject="wellbeing_recent_pattern",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(recent),
            supporting_metrics={
                "recent_sample_size": len(recent),
                "baseline_count": len(baselines),
            },
            reason=InsightReason.INSUFFICIENT_SCORES,
        )

    above = all(
        float(row["score"]) > float(row["baseline"])
        for row in recent
    )

    below = all(
        float(row["score"]) < float(row["baseline"])
        for row in recent
    )

    if above:
        direction = InsightDirection.HIGHER
    elif below:
        direction = InsightDirection.LOWER
    else:
        return RuleResult(
            category=InsightCategory.RECENT_CHANGE,
            subject="wellbeing_recent_pattern",
            direction=InsightDirection.STABLE,
            data_sufficiency=DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE,
            sample_size=3,
            supporting_metrics={
                "recent_scores": [float(row["score"]) for row in recent],
                "baselines": [float(row["baseline"]) for row in recent],
            },
            reason=InsightReason.NO_MEANINGFUL_PATTERN,
        )

    return RuleResult(
        category=InsightCategory.RECENT_CHANGE,
        subject="wellbeing_recent_pattern",
        direction=direction,
        data_sufficiency=DataSufficiency.SUFFICIENT_MEANINGFUL,
        sample_size=3,
        supporting_metrics={
            "recent_scores": [float(row["score"]) for row in recent],
            "baselines": [float(row["baseline"]) for row in recent],
            "pattern": "above_baseline" if above else "below_baseline",
        },
        comparison_period={
            "window_days": RECENT_WINDOW_DAYS,
            "scores_used": 3,
        },
    )
