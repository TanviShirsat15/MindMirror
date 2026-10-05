from app.insights.insight_types import (
    InsightCategory,
    InsightDirection,
    RuleResult,
)


def _direction_phrase(direction: InsightDirection) -> str:
    if direction == InsightDirection.HIGHER:
        return "higher"
    if direction == InsightDirection.LOWER:
        return "lower"
    if direction == InsightDirection.VARIED:
        return "varied"
    return "stable"


def render_insight(result: RuleResult) -> tuple[str, str]:
    direction = _direction_phrase(result.direction)
    metrics = result.supporting_metrics

    if result.category == InsightCategory.BASELINE_COMPARISON:
        title = "Recent score compared with your personal baseline"
        explanation = (
            f"Your latest recorded well-being score was "
            f"{metrics['latest_score']:.1f}, which was {direction} "
            f"than your personal baseline of "
            f"{metrics['personal_baseline']:.1f}."
        )
        return title, explanation

    if result.category == InsightCategory.RECENT_CHANGE:
        if result.subject == "wellbeing_recent_pattern":
            title = "Recent well-being pattern"
            pattern = metrics.get("pattern")

            if pattern == "above_baseline":
                explanation = (
                    "Your latest three recorded well-being scores "
                    "were all above your personal baseline."
                )
            else:
                explanation = (
                    "Your latest three recorded well-being scores "
                    "were all below your personal baseline."
                )

            return title, explanation

        title = "Recent well-being change"
        explanation = (
            f"Your recent average score was {direction} than the "
            f"previous 7-day period, based on the available scores "
            f"in your history."
        )
        return title, explanation

    if result.category == InsightCategory.TREND:
        title = "Well-being trend"
        explanation = (
            f"Your well-being scores have tended to be {direction} "
            f"in the more recent half of the 28-day window compared "
            f"with the earlier half."
        )
        return title, explanation

    if result.category == InsightCategory.HABIT_ASSOCIATION:
        title = "Habit completion pattern"
        explanation = (
            f"Higher overall habit completion has been associated "
            f"with {direction} well-being scores in your historical data."
        )
        return title, explanation

    if result.category == InsightCategory.NLP_SIGNAL_TREND:
        signal = result.subject.replace("_", " ")
        title = f"{signal.title()} trend"
        explanation = (
            f"Your {signal} signal has tended to be {direction} "
            f"in the more recent half of the 28-day window."
        )
        return title, explanation

    if result.category == InsightCategory.CONSISTENCY:
        title = "Habit consistency pattern"

        if result.direction == InsightDirection.VARIED:
            explanation = (
                "Your habit completion has been relatively varied "
                "across the available days in the recent 28-day window."
            )
        else:
            explanation = (
                "Your habit completion has been relatively consistent "
                "across the available days in the recent 28-day window."
            )

        return title, explanation

    raise ValueError(f"Unsupported insight category: {result.category}")