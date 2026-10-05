"""Standalone Mamdani fuzzy inference engine for MindMirror."""

from __future__ import annotations

import math
from itertools import product
from numbers import Real

import numpy as np
import skfuzzy as fuzz


# ---------------------------------------------------------------------------
# Input and output ranges
# ---------------------------------------------------------------------------

SENTIMENT_MIN = -1.0
SENTIMENT_MAX = 1.0

STRESS_MIN = 0.0
STRESS_MAX = 1.0

HABIT_MIN = 0.0
HABIT_MAX = 1.0

WELLBEING_MIN = 1.0
WELLBEING_MAX = 100.0


# ---------------------------------------------------------------------------
# Membership function definitions
# ---------------------------------------------------------------------------

SENTIMENT_TERMS = {
    "negative": (-1.0, -1.0, -0.5, 0.0),
    "neutral": (-0.5, 0.0, 0.5),
    "positive": (0.0, 0.5, 1.0, 1.0),
}

STRESS_TERMS = {
    "low": (0.0, 0.0, 0.2, 0.4),
    "medium": (0.2, 0.5, 0.8),
    "high": (0.6, 0.8, 1.0, 1.0),
}

HABIT_TERMS = {
    "low": (0.0, 0.0, 0.2, 0.4),
    "medium": (0.2, 0.5, 0.8),
    "high": (0.6, 0.8, 1.0, 1.0),
}

OUTPUT_TERMS = {
    "low": (1.0, 1.0, 25.0, 45.0),
    "moderate": (30.0, 50.0, 70.0),
    "high": (55.0, 75.0, 100.0, 100.0),
}


# ---------------------------------------------------------------------------
# Rule direction definitions
# ---------------------------------------------------------------------------

# +1 = favorable
#  0 = neutral
# -1 = unfavorable
SENTIMENT_DIRECTION = {
    "negative": -1,
    "neutral": 0,
    "positive": 1,
}

STRESS_DIRECTION = {
    "low": 1,
    "medium": 0,
    "high": -1,
}

HABIT_DIRECTION = {
    "low": -1,
    "medium": 0,
    "high": 1,
}


def _validate_input(
    name: str,
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """Validate one fuzzy-engine input and return it as a float."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(
            f"{name} must be numeric; received {type(value).__name__}"
        )

    value = float(value)

    if not math.isfinite(value):
        raise ValueError(
            f"{name} must be finite; received {value}"
        )

    if value < minimum or value > maximum:
        raise ValueError(
            f"{name} must be in the range "
            f"{minimum} to {maximum}; received {value}"
        )

    return value


def _fuzzify_sentiment(value: float) -> dict[str, float]:
    """Return membership degrees for the three sentiment terms."""

    return {
        "negative": float(
            fuzz.interp_membership(
                np.array([-1.0, -0.5, 0.0, 1.0]),
                fuzz.trapmf(
                    np.array([-1.0, -0.5, 0.0, 1.0]),
                    SENTIMENT_TERMS["negative"],
                ),
                value,
            )
        ),
        "neutral": float(
            fuzz.interp_membership(
                np.array([-1.0, -0.5, 0.0, 0.5, 1.0]),
                fuzz.trimf(
                    np.array([-1.0, -0.5, 0.0, 0.5, 1.0]),
                    SENTIMENT_TERMS["neutral"],
                ),
                value,
            )
        ),
        "positive": float(
            fuzz.interp_membership(
                np.array([-1.0, 0.0, 0.5, 1.0]),
                fuzz.trapmf(
                    np.array([-1.0, 0.0, 0.5, 1.0]),
                    SENTIMENT_TERMS["positive"],
                ),
                value,
            )
        ),
    }


def _fuzzify_stress(value: float) -> dict[str, float]:
    """Return membership degrees for the three stress terms."""

    universe = np.linspace(0.0, 1.0, 1001)

    return {
        "low": float(
            fuzz.interp_membership(
                universe,
                fuzz.trapmf(
                    universe,
                    STRESS_TERMS["low"],
                ),
                value,
            )
        ),
        "medium": float(
            fuzz.interp_membership(
                universe,
                fuzz.trimf(
                    universe,
                    STRESS_TERMS["medium"],
                ),
                value,
            )
        ),
        "high": float(
            fuzz.interp_membership(
                universe,
                fuzz.trapmf(
                    universe,
                    STRESS_TERMS["high"],
                ),
                value,
            )
        ),
    }


def _fuzzify_habit(value: float) -> dict[str, float]:
    """Return membership degrees for the three habit terms."""

    universe = np.linspace(0.0, 1.0, 1001)

    return {
        "low": float(
            fuzz.interp_membership(
                universe,
                fuzz.trapmf(
                    universe,
                    HABIT_TERMS["low"],
                ),
                value,
            )
        ),
        "medium": float(
            fuzz.interp_membership(
                universe,
                fuzz.trimf(
                    universe,
                    HABIT_TERMS["medium"],
                ),
                value,
            )
        ),
        "high": float(
            fuzz.interp_membership(
                universe,
                fuzz.trapmf(
                    universe,
                    HABIT_TERMS["high"],
                ),
                value,
            )
        ),
    }


def _output_membership_function(
    term: str,
    universe: np.ndarray,
) -> np.ndarray:
    """Build one output membership function."""

    parameters = OUTPUT_TERMS[term]

    if len(parameters) == 3:
        return fuzz.trimf(universe, parameters)

    return fuzz.trapmf(universe, parameters)


def _output_term_from_direction_sum(total: int) -> str:
    """Map a direction sum from -3..+3 to an output linguistic term."""

    if total >= 2:
        return "high"

    if total <= -2:
        return "low"

    return "moderate"


def _generate_rules() -> list[dict]:
    """
    Generate the complete 27-rule base.

    Each rule is classified using the documented direction-sum formula:
        favorable = +1
        neutral = 0
        unfavorable = -1

    Sum the three directions:
        sum >= 2  -> high
        sum <= -2 -> low
        otherwise -> moderate
    """

    rules = []

    for sentiment_term, stress_term, habit_term in product(
        SENTIMENT_TERMS,
        STRESS_TERMS,
        HABIT_TERMS,
    ):
        direction_sum = (
            SENTIMENT_DIRECTION[sentiment_term]
            + STRESS_DIRECTION[stress_term]
            + HABIT_DIRECTION[habit_term]
        )

        output_term = _output_term_from_direction_sum(direction_sum)

        rules.append(
            {
                "sentiment": sentiment_term,
                "stress": stress_term,
                "habit": habit_term,
                "direction_sum": direction_sum,
                "output": output_term,
            }
        )

    return rules


RULES = _generate_rules()


def _evaluate_rules(
    fuzzified_inputs: dict[str, dict[str, float]],
) -> dict[str, float]:
    """Evaluate all 27 rules using minimum as the AND operator."""

    rule_firing_strengths = {}

    for rule in RULES:
        sentiment_degree = fuzzified_inputs["sentiment"][rule["sentiment"]]
        stress_degree = fuzzified_inputs["stress"][rule["stress"]]
        habit_degree = fuzzified_inputs["habit"][rule["habit"]]

        firing_strength = min(
            sentiment_degree,
            stress_degree,
            habit_degree,
        )

        rule_name = (
            f"{rule['sentiment']} AND "
            f"{rule['stress']} AND "
            f"{rule['habit']} -> "
            f"{rule['output']}"
        )

        rule_firing_strengths[rule_name] = float(firing_strength)

    return rule_firing_strengths


def _aggregate_outputs(
    rule_firing_strengths: dict[str, float],
    universe: np.ndarray,
) -> np.ndarray:
    """Clip output membership functions and aggregate using maximum."""

    aggregated = np.zeros_like(universe, dtype=float)

    for rule in RULES:
        rule_name = (
            f"{rule['sentiment']} AND "
            f"{rule['stress']} AND "
            f"{rule['habit']} -> "
            f"{rule['output']}"
        )

        firing_strength = rule_firing_strengths[rule_name]

        output_membership = _output_membership_function(
            rule["output"],
            universe,
        )

        clipped_output = np.fmin(
            firing_strength,
            output_membership,
        )

        aggregated = np.fmax(
            aggregated,
            clipped_output,
        )

    return aggregated


def calculate_wellbeing_index(
    sentiment_score: float,
    stress_indicator: float,
    habit_consistency: float,
) -> dict:
    """
    Calculate the MindMirror Well-Being Index using Mamdani inference.

    Inputs:
        sentiment_score:
            VADER sentiment compound score, -1.0 to 1.0.

        stress_indicator:
            Stress-related linguistic indicator, 0.0 to 1.0.

        habit_consistency:
            Habit consistency, 0.0 to 1.0.

    Returns:
        A dictionary containing the final score, original inputs,
        fuzzified membership degrees, and all rule firing strengths.
    """

    sentiment_score = _validate_input(
        "sentiment_score",
        sentiment_score,
        SENTIMENT_MIN,
        SENTIMENT_MAX,
    )

    stress_indicator = _validate_input(
        "stress_indicator",
        stress_indicator,
        STRESS_MIN,
        STRESS_MAX,
    )

    habit_consistency = _validate_input(
        "habit_consistency",
        habit_consistency,
        HABIT_MIN,
        HABIT_MAX,
    )

    fuzzified_inputs = {
        "sentiment": _fuzzify_sentiment(sentiment_score),
        "stress": _fuzzify_stress(stress_indicator),
        "habit": _fuzzify_habit(habit_consistency),
    }

    rule_firing_strengths = _evaluate_rules(
        fuzzified_inputs
    )

    output_universe = np.linspace(
        WELLBEING_MIN,
        WELLBEING_MAX,
        1000,
    )

    aggregated_output = _aggregate_outputs(
        rule_firing_strengths,
        output_universe,
    )

    if np.max(aggregated_output) == 0:
        raise ValueError(
            "Unable to defuzzify the Well-Being Index: "
            "no rule produced a positive firing strength"
        )

    raw_score = fuzz.defuzz(
        output_universe,
        aggregated_output,
        "centroid",
    )

    score = min(
        WELLBEING_MAX,
        max(WELLBEING_MIN, float(raw_score)),
    )

    return {
        "score": round(score, 2),
        "inputs": {
            "sentiment_score": sentiment_score,
            "stress_indicator": stress_indicator,
            "habit_consistency": habit_consistency,
        },
        "fuzzified_inputs": fuzzified_inputs,
        "rule_firing_strengths": rule_firing_strengths,
    }