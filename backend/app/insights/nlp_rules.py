from statistics import mean
from typing import Any

from app.insights.insight_config import (
    MATERIAL_RANGE_FRACTION,
    NLP_MIN_PER_HALF,
    TREND_WINDOW_DAYS,
)
from app.insights.insight_types import (
    DataSufficiency,
    InsightCategory,
    InsightDirection,
    InsightReason,
    RuleResult,
)


NLP_SIGNAL_RANGES = {
    "sentiment": (-1.0, 1.0),
    "positive_emotion": (0.0, 1.0),
    "negative_emotion": (0.0, 1.0),
    "stress": (0.0, 1.0),
}


def nlp_signal_trend_rule(
    nlp_rows: list[dict[str, Any]],
    as_of,
) -> RuleResult:
    half = TREND_WINDOW_DAYS // 2

    candidates = []

    for signal, (scale_min, scale_max) in NLP_SIGNAL_RANGES.items():
        recent = [
            float(row[signal])
            for row in nlp_rows
            if row.get(signal) is not None
            and 0 <= (as_of - row["date"]).days < half
        ]

        previous = [
            float(row[signal])
            for row in nlp_rows
            if row.get(signal) is not None
            and half <= (as_of - row["date"]).days < TREND_WINDOW_DAYS
        ]

        if (
            len(recent) < NLP_MIN_PER_HALF
            or len(previous) < NLP_MIN_PER_HALF
        ):
            continue

        recent_mean = mean(recent)
        previous_mean = mean(previous)
        difference = recent_mean - previous_mean

        threshold = MATERIAL_RANGE_FRACTION * (
            scale_max - scale_min
        )

        if abs(difference) < threshold:
            continue

        candidates.append(
            {
                "signal": signal,
                "recent_mean": recent_mean,
                "previous_mean": previous_mean,
                "difference": difference,
                "threshold": threshold,
                "sample_size": len(recent) + len(previous),
                "magnitude": abs(difference) / threshold,
            }
        )

    if not candidates:
        has_any_nlp = any(
            any(row.get(signal) is not None for signal in NLP_SIGNAL_RANGES)
            for row in nlp_rows
        )

        return RuleResult(
            category=InsightCategory.NLP_SIGNAL_TREND,
            subject="nlp_signals",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=(
                DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE
                if has_any_nlp
                else DataSufficiency.NO_DATA
            ),
            sample_size=0,
            supporting_metrics={},
            reason=(
                InsightReason.NO_MEANINGFUL_TREND
                if has_any_nlp
                else InsightReason.NO_NLP_DATA
            ),
        )

    strongest = max(
        candidates,
        key=lambda item: item["magnitude"],
    )

    direction = (
        InsightDirection.HIGHER
        if strongest["difference"] > 0
        else InsightDirection.LOWER
    )

    return RuleResult(
        category=InsightCategory.NLP_SIGNAL_TREND,
        subject=strongest["signal"],
        direction=direction,
        data_sufficiency=DataSufficiency.SUFFICIENT_MEANINGFUL,
        sample_size=strongest["sample_size"],
        supporting_metrics={
            "recent_mean": round(strongest["recent_mean"], 4),
            "previous_mean": round(strongest["previous_mean"], 4),
            "difference": round(strongest["difference"], 4),
            "threshold": round(strongest["threshold"], 4),
        },
        comparison_period={
            "window_days": TREND_WINDOW_DAYS,
            "half_days": half,
        },
    )
