from dataclasses import dataclass
from enum import Enum
from typing import Any


class InsightCategory(str, Enum):
    BASELINE_COMPARISON = "baseline_comparison"
    RECENT_CHANGE = "recent_change"
    HABIT_ASSOCIATION = "habit_association"
    TREND = "trend"
    NLP_SIGNAL_TREND = "nlp_signal_trend"
    CONSISTENCY = "consistency"


class InsightDirection(str, Enum):
    HIGHER = "higher"
    LOWER = "lower"
    STABLE = "stable"
    VARIED = "varied"
    NOT_APPLICABLE = "not_applicable"


class DataSufficiency(str, Enum):
    SUFFICIENT_MEANINGFUL = "sufficient_meaningful"
    SUFFICIENT_NO_MEANINGFUL_CHANGE = "sufficient_no_meaningful_change"
    INSUFFICIENT_HISTORY = "insufficient_history"
    NO_DATA = "no_data"


class InsightReason(str, Enum):
    NO_JOURNAL_DATA = "no_journal_data"
    NO_WELLBEING_SCORES = "no_wellbeing_scores"
    INSUFFICIENT_SCORES = "insufficient_scores"
    NO_RECENT_SCORES = "no_recent_scores"
    NO_HABIT_DATA = "no_habit_data"
    INSUFFICIENT_HABIT_OBSERVATIONS = "insufficient_habit_observations"
    NO_NLP_DATA = "no_nlp_data"
    INSUFFICIENT_NLP_OBSERVATIONS = "insufficient_nlp_observations"
    NO_MEANINGFUL_TREND = "no_meaningful_trend"
    NO_MEANINGFUL_ASSOCIATION = "no_meaningful_association"
    NO_MEANINGFUL_PATTERN = "no_meaningful_pattern"
    NO_NEW_INSIGHT = "no_new_insight"


@dataclass(frozen=True)
class RuleResult:
    category: InsightCategory
    subject: str
    direction: InsightDirection
    data_sufficiency: DataSufficiency
    sample_size: int
    supporting_metrics: dict[str, Any]
    comparison_period: dict[str, Any] | None = None
    reason: InsightReason | None = None


@dataclass(frozen=True)
class InsightResult:
    insight_key: str
    category: InsightCategory
    subject: str
    title: str
    explanation: str
    direction: InsightDirection
    supporting_metrics: dict[str, Any]
    comparison_period: dict[str, Any] | None
    data_sufficiency: DataSufficiency
    sample_size: int
    is_new: bool
    first_generated_at: Any | None = None
    generated_at: Any | None = None
