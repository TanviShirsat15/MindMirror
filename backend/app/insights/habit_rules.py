from statistics import mean, pstdev
from typing import Any

from app.insights.insight_config import (
    ASSOC_MIN_ABS_RHO,
    ASSOC_MIN_COMPLETION_GAP,
    ASSOC_MIN_GROUP_DAYS,
    ASSOC_MIN_PAIRED_DAYS,
    CONSISTENCY_MIN_DAYS,
    CONSISTENCY_WINDOW_DAYS,
    CONSISTENT_SD_MAX,
    VARIED_SD_MIN,
)
from app.insights.insight_types import (
    DataSufficiency,
    InsightCategory,
    InsightDirection,
    InsightReason,
    RuleResult,
)


def _paired_rows(
    wellbeing_rows: list[dict[str, Any]],
    habit_rows: list[dict[str, Any]],
) -> list[tuple[float, float]]:
    wellbeing_by_date = {
        row["date"]: float(row["score"])
        for row in wellbeing_rows
        if row.get("score") is not None
    }

    pairs = []

    for row in habit_rows:
        completion = row.get("completion_rate")
        score = wellbeing_by_date.get(row["date"])

        if score is not None and completion is not None:
            pairs.append((float(completion), score))

    return pairs


def _spearman_rho(
    pairs: list[tuple[float, float]],
) -> float:
    if len(pairs) < 2:
        return 0.0

    def ranks(values: list[float]) -> list[float]:
        ordered = sorted(
            enumerate(values),
            key=lambda item: item[1],
        )

        result = [0.0] * len(values)
        index = 0

        while index < len(ordered):
            end = index

            while (
                end + 1 < len(ordered)
                and ordered[end + 1][1] == ordered[index][1]
            ):
                end += 1

            rank = (index + end) / 2 + 1

            for position in range(index, end + 1):
                result[ordered[position][0]] = rank

            index = end + 1

        return result

    x = [pair[0] for pair in pairs]
    y = [pair[1] for pair in pairs]

    rx = ranks(x)
    ry = ranks(y)

    mean_x = mean(rx)
    mean_y = mean(ry)

    numerator = sum(
        (a - mean_x) * (b - mean_y)
        for a, b in zip(rx, ry)
    )

    denominator_x = sum(
        (a - mean_x) ** 2
        for a in rx
    )

    denominator_y = sum(
        (b - mean_y) ** 2
        for b in ry
    )

    denominator = (denominator_x * denominator_y) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator


def habit_association_rule(
    wellbeing_rows: list[dict[str, Any]],
    habit_rows: list[dict[str, Any]],
) -> RuleResult:
    pairs = _paired_rows(
        wellbeing_rows,
        habit_rows,
    )

    if len(pairs) < ASSOC_MIN_PAIRED_DAYS:
        return RuleResult(
            category=InsightCategory.HABIT_ASSOCIATION,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(pairs),
            supporting_metrics={},
            reason=InsightReason.INSUFFICIENT_HABIT_OBSERVATIONS,
        )

    median_completion = sorted(
        pair[0] for pair in pairs
    )[len(pairs) // 2]

    lower = [
        pair for pair in pairs
        if pair[0] <= median_completion
    ]

    higher = [
        pair for pair in pairs
        if pair[0] > median_completion
    ]

    if (
        len(lower) < ASSOC_MIN_GROUP_DAYS
        or len(higher) < ASSOC_MIN_GROUP_DAYS
    ):
        return RuleResult(
            category=InsightCategory.HABIT_ASSOCIATION,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(pairs),
            supporting_metrics={
                "lower_group_size": len(lower),
                "higher_group_size": len(higher),
            },
            reason=InsightReason.INSUFFICIENT_HABIT_OBSERVATIONS,
        )

    lower_completion = mean(pair[0] for pair in lower)
    higher_completion = mean(pair[0] for pair in higher)

    completion_gap = higher_completion - lower_completion

    if completion_gap < ASSOC_MIN_COMPLETION_GAP:
        return RuleResult(
            category=InsightCategory.HABIT_ASSOCIATION,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE,
            sample_size=len(pairs),
            supporting_metrics={
                "completion_gap": round(completion_gap, 4),
                "lower_group_size": len(lower),
                "higher_group_size": len(higher),
            },
            reason=InsightReason.NO_MEANINGFUL_ASSOCIATION,
        )

    lower_score = mean(pair[1] for pair in lower)
    higher_score = mean(pair[1] for pair in higher)
    score_difference = higher_score - lower_score

    rho = _spearman_rho(pairs)

    if (
        abs(score_difference) < 5.0
        or abs(rho) < ASSOC_MIN_ABS_RHO
    ):
        return RuleResult(
            category=InsightCategory.HABIT_ASSOCIATION,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE,
            sample_size=len(pairs),
            supporting_metrics={
                "completion_gap": round(completion_gap, 4),
                "score_difference": round(score_difference, 1),
                "spearman_rho": round(rho, 3),
            },
            reason=InsightReason.NO_MEANINGFUL_ASSOCIATION,
        )

    direction = (
        InsightDirection.HIGHER
        if score_difference > 0
        else InsightDirection.LOWER
    )

    return RuleResult(
        category=InsightCategory.HABIT_ASSOCIATION,
        subject="habits_overall",
        direction=direction,
        data_sufficiency=DataSufficiency.SUFFICIENT_MEANINGFUL,
        sample_size=len(pairs),
        supporting_metrics={
            "completion_gap": round(completion_gap, 4),
            "lower_group_score": round(lower_score, 1),
            "higher_group_score": round(higher_score, 1),
            "score_difference": round(score_difference, 1),
            "spearman_rho": round(rho, 3),
        },
    )


def consistency_rule(
    habit_rows: list[dict[str, Any]],
) -> RuleResult:
    applicable = [
        row
        for row in habit_rows
        if row.get("completion_rate") is not None
    ][-CONSISTENCY_WINDOW_DAYS:]

    values = [
        float(row["completion_rate"])
        for row in applicable
    ]

    if len(values) < CONSISTENCY_MIN_DAYS:
        return RuleResult(
            category=InsightCategory.CONSISTENCY,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.INSUFFICIENT_HISTORY,
            sample_size=len(values),
            supporting_metrics={},
            reason=InsightReason.INSUFFICIENT_HABIT_OBSERVATIONS,
        )

    sd = pstdev(values)

    if sd <= CONSISTENT_SD_MAX:
        direction = InsightDirection.STABLE
    elif sd >= VARIED_SD_MIN:
        direction = InsightDirection.NOT_APPLICABLE
    else:
        return RuleResult(
            category=InsightCategory.CONSISTENCY,
            subject="habits_overall",
            direction=InsightDirection.NOT_APPLICABLE,
            data_sufficiency=DataSufficiency.SUFFICIENT_NO_MEANINGFUL_CHANGE,
            sample_size=len(values),
            supporting_metrics={
                "completion_sd": round(sd, 4),
            },
            reason=InsightReason.NO_MEANINGFUL_PATTERN,
        )

    return RuleResult(
        category=InsightCategory.CONSISTENCY,
        subject="habits_overall",
        direction=direction,
        data_sufficiency=DataSufficiency.SUFFICIENT_MEANINGFUL,
        sample_size=len(values),
        supporting_metrics={
            "completion_sd": round(sd, 4),
            "mean_completion": round(mean(values), 4),
        },
    )
