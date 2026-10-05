import math

import pytest

from app.services.fuzzy.fuzzy_engine import calculate_wellbeing_index


def get_score(sentiment_score, stress_indicator, habit_consistency):
    result = calculate_wellbeing_index(
        sentiment_score,
        stress_indicator,
        habit_consistency,
    )
    return result["score"]


def test_favorable_inputs_produce_high_region():
    result = calculate_wellbeing_index(
        sentiment_score=0.8,
        stress_indicator=0.1,
        habit_consistency=0.9,
    )

    assert result["score"] >= 55
    assert result["score"] <= 100


def test_unfavorable_inputs_produce_low_region():
    result = calculate_wellbeing_index(
        sentiment_score=-0.8,
        stress_indicator=0.9,
        habit_consistency=0.1,
    )

    assert result["score"] >= 1
    assert result["score"] <= 45


def test_positive_sentiment_high_stress_low_habit_is_moderate():
    result = calculate_wellbeing_index(
        sentiment_score=0.8,
        stress_indicator=0.9,
        habit_consistency=0.1,
    )

    assert 30 <= result["score"] <= 70


def test_negative_sentiment_low_stress_high_habit_is_moderate():
    result = calculate_wellbeing_index(
        sentiment_score=-0.8,
        stress_indicator=0.1,
        habit_consistency=0.9,
    )

    assert 30 <= result["score"] <= 70


def test_balanced_neutral_inputs_are_moderate():
    result = calculate_wellbeing_index(
        sentiment_score=0.0,
        stress_indicator=0.5,
        habit_consistency=0.5,
    )

    assert 30 <= result["score"] <= 70


@pytest.mark.parametrize(
    "sentiment_score",
    [-1.0, 0.0, 1.0],
)
@pytest.mark.parametrize(
    "stress_indicator",
    [0.0, 0.5, 1.0],
)
@pytest.mark.parametrize(
    "habit_consistency",
    [0.0, 0.5, 1.0],
)
def test_boundary_inputs_do_not_crash(
    sentiment_score,
    stress_indicator,
    habit_consistency,
):
    result = calculate_wellbeing_index(
        sentiment_score=sentiment_score,
        stress_indicator=stress_indicator,
        habit_consistency=habit_consistency,
    )

    assert 1 <= result["score"] <= 100


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "sentiment_score": -1.1,
            "stress_indicator": 0.5,
            "habit_consistency": 0.5,
        },
        {
            "sentiment_score": 1.1,
            "stress_indicator": 0.5,
            "habit_consistency": 0.5,
        },
        {
            "sentiment_score": 0.0,
            "stress_indicator": -0.1,
            "habit_consistency": 0.5,
        },
        {
            "sentiment_score": 0.0,
            "stress_indicator": 1.1,
            "habit_consistency": 0.5,
        },
        {
            "sentiment_score": 0.0,
            "stress_indicator": 0.5,
            "habit_consistency": -0.1,
        },
        {
            "sentiment_score": 0.0,
            "stress_indicator": 0.5,
            "habit_consistency": 1.1,
        },
    ],
)
def test_out_of_range_inputs_are_rejected(kwargs):
    with pytest.raises(ValueError):
        calculate_wellbeing_index(**kwargs)


@pytest.mark.parametrize(
    "invalid_value",
    [None, float("nan"), float("inf"), float("-inf"), "0.5", "invalid"],
)
def test_invalid_sentiment_inputs_are_rejected(invalid_value):
    with pytest.raises(ValueError):
        calculate_wellbeing_index(
            sentiment_score=invalid_value,
            stress_indicator=0.5,
            habit_consistency=0.5,
        )


@pytest.mark.parametrize(
    "invalid_value",
    [None, float("nan"), float("inf"), float("-inf"), "0.5", "invalid"],
)
def test_invalid_stress_inputs_are_rejected(invalid_value):
    with pytest.raises(ValueError):
        calculate_wellbeing_index(
            sentiment_score=0.0,
            stress_indicator=invalid_value,
            habit_consistency=0.5,
        )


@pytest.mark.parametrize(
    "invalid_value",
    [None, float("nan"), float("inf"), float("-inf"), "0.5", "invalid"],
)
def test_invalid_habit_inputs_are_rejected(invalid_value):
    with pytest.raises(ValueError):
        calculate_wellbeing_index(
            sentiment_score=0.0,
            stress_indicator=0.5,
            habit_consistency=invalid_value,
        )


def test_boolean_inputs_are_rejected():
    with pytest.raises(ValueError):
        calculate_wellbeing_index(
            sentiment_score=True,
            stress_indicator=0.5,
            habit_consistency=0.5,
        )


def test_increasing_sentiment_moves_in_favorable_direction():
    lower = get_score(
        sentiment_score=0.2,
        stress_indicator=0.5,
        habit_consistency=0.5,
    )

    higher = get_score(
        sentiment_score=0.8,
        stress_indicator=0.5,
        habit_consistency=0.5,
    )

    assert higher >= lower


def test_decreasing_stress_moves_in_favorable_direction():
    higher_stress = get_score(
        sentiment_score=0.0,
        stress_indicator=0.8,
        habit_consistency=0.5,
    )

    lower_stress = get_score(
        sentiment_score=0.0,
        stress_indicator=0.2,
        habit_consistency=0.5,
    )

    assert lower_stress >= higher_stress


def test_increasing_habit_consistency_moves_in_favorable_direction():
    lower_habit = get_score(
        sentiment_score=0.0,
        stress_indicator=0.5,
        habit_consistency=0.2,
    )

    higher_habit = get_score(
        sentiment_score=0.0,
        stress_indicator=0.5,
        habit_consistency=0.8,
    )

    assert higher_habit >= lower_habit


def test_identical_inputs_are_deterministic():
    first = calculate_wellbeing_index(
        sentiment_score=0.35,
        stress_indicator=0.4,
        habit_consistency=0.7,
    )

    second = calculate_wellbeing_index(
        sentiment_score=0.35,
        stress_indicator=0.4,
        habit_consistency=0.7,
    )

    assert first == second


def test_result_contains_required_structure():
    result = calculate_wellbeing_index(
        sentiment_score=0.8,
        stress_indicator=0.1,
        habit_consistency=0.9,
    )

    assert set(result.keys()) == {
        "score",
        "inputs",
        "fuzzified_inputs",
        "rule_firing_strengths",
    }

    assert set(result["inputs"].keys()) == {
        "sentiment_score",
        "stress_indicator",
        "habit_consistency",
    }

    assert set(result["fuzzified_inputs"].keys()) == {
        "sentiment",
        "stress",
        "habit",
    }

    assert set(result["fuzzified_inputs"]["sentiment"].keys()) == {
        "negative",
        "neutral",
        "positive",
    }

    assert set(result["fuzzified_inputs"]["stress"].keys()) == {
        "low",
        "medium",
        "high",
    }

    assert set(result["fuzzified_inputs"]["habit"].keys()) == {
        "low",
        "medium",
        "high",
    }


def test_all_27_rules_are_present():
    result = calculate_wellbeing_index(
        sentiment_score=0.25,
        stress_indicator=0.35,
        habit_consistency=0.75,
    )

    assert len(result["rule_firing_strengths"]) == 27


def test_rule_firing_strengths_are_valid():
    result = calculate_wellbeing_index(
        sentiment_score=0.25,
        stress_indicator=0.35,
        habit_consistency=0.75,
    )

    assert all(
        0.0 <= strength <= 1.0
        for strength in result["rule_firing_strengths"].values()
    )


def test_at_least_one_rule_fires_for_representative_input():
    result = calculate_wellbeing_index(
        sentiment_score=0.25,
        stress_indicator=0.35,
        habit_consistency=0.75,
    )

    assert any(
        strength > 0
        for strength in result["rule_firing_strengths"].values()
    )


def test_score_is_finite_and_rounded():
    result = calculate_wellbeing_index(
        sentiment_score=0.63,
        stress_indicator=0.28,
        habit_consistency=0.82,
    )

    assert math.isfinite(result["score"])
    assert 1 <= result["score"] <= 100

    decimal_part = str(result["score"]).split(".")

    if len(decimal_part) == 2:
        assert len(decimal_part[1]) <= 2