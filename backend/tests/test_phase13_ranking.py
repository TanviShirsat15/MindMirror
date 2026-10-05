from app.insights.insight_ranking import (
    deduplicate_insights,
    insight_key,
    rank_insights,
)
from app.insights.insight_types import (
    DataSufficiency,
    InsightCategory,
    InsightDirection,
    RuleResult,
)


def make_result(category, subject, direction, difference, threshold=5.0):
    return RuleResult(
        category=category,
        subject=subject,
        direction=direction,
        data_sufficiency=DataSufficiency.SUFFICIENT_MEANINGFUL,
        sample_size=10,
        supporting_metrics={
            "difference": difference,
            "threshold": threshold,
        },
    )


def test_higher_weight_category_ranks_first():
    baseline = make_result(
        InsightCategory.BASELINE_COMPARISON,
        "wellbeing",
        InsightDirection.HIGHER,
        5,
    )
    consistency = make_result(
        InsightCategory.CONSISTENCY,
        "habits",
        InsightDirection.NOT_APPLICABLE,
        10,
    )

    ranked = rank_insights([consistency, baseline])

    assert ranked[0].category == InsightCategory.BASELINE_COMPARISON


def test_duplicate_insight_keys_are_removed():
    first = make_result(
        InsightCategory.TREND,
        "wellbeing",
        InsightDirection.HIGHER,
        10,
    )
    duplicate = make_result(
        InsightCategory.TREND,
        "wellbeing",
        InsightDirection.HIGHER,
        8,
    )

    unique = deduplicate_insights([first, duplicate])

    assert len(unique) == 1
    assert insight_key(unique[0]) == "trend:wellbeing:higher:60d"


def test_different_directions_are_not_duplicates():
    higher = make_result(
        InsightCategory.TREND,
        "wellbeing",
        InsightDirection.HIGHER,
        10,
    )
    lower = make_result(
        InsightCategory.TREND,
        "wellbeing",
        InsightDirection.LOWER,
        -10,
    )

    unique = deduplicate_insights([higher, lower])

    assert len(unique) == 2
