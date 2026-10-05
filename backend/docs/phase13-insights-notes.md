# Phase 13 — Explainable Self-Reflection Insights

## Purpose

Phase 13 adds explainable self-reflection insights to MindMirror.

The insight system identifies meaningful patterns in the user's own historical wellbeing, habit, and NLP-derived data. It does not diagnose medical or mental-health conditions and does not provide clinical advice.

Insights are based on personal historical data rather than comparison with other users.

## Data Sources

The insight engine uses:

- Historical Well-Being Index scores.
- Habit completion history.
- Existing NLP-derived daily signals.
- User-specific historical baseline information from the existing analytics/baseline system.

The system does not use journal text directly for generated insight explanations.

Missing dates remain missing and are not automatically converted into zero values.

The insight lookback window is limited to 60 days.

## Insight Categories

Phase 13 supports the following insight categories:

### Baseline

Compares recent valid wellbeing values with the user's established personal baseline.

### Recent Change

Compares the recent 7-day wellbeing period with the immediately preceding 7-day period when enough valid observations exist.

### Trend

Examines movement across two 14-day periods.

### Habit

Identifies meaningful associations between habit completion and wellbeing.

### Consistency

Describes whether wellbeing values are relatively stable or varied over a 28-day period.

### Emotional

Examines changes in existing NLP-derived signals over time.

No new NLP signal is invented by the insight layer.

## Thresholds and Windows

The insight engine uses bounded historical windows:

- Lookback window: 60 days.
- Recent window: 7 days.
- Recency window: 14 days.
- Trend window: 28 days divided into two 14-day halves.
- New-insight window: 48 hours.

A material change threshold is used to avoid reporting insignificant fluctuations.

For datasets with at least 8 values, the threshold is based on 0.5 standard deviation.

For smaller applicable datasets, the threshold is based on 0.05 of the relevant scale range.

Minimum sample requirements are enforced before an insight is considered sufficient.

## Well-Being Rules

### Baseline comparison

Recent valid wellbeing values are compared against the user's personal baseline.

The insight language describes the observed difference without implying that the difference is medically meaningful.

### Recent change

The recent 7-day period is compared with the previous 7-day period.

At least 3 valid observations are required in each period.

### Trend

The 28-day trend window is divided into two 14-day halves.

At least 5 valid observations are required in each half.

The result describes the direction of the user's historical wellbeing pattern.

## Habit Association

Habit association uses paired days containing both habit and wellbeing information.

Requirements include:

- At least 14 paired days.
- At least 5 observations in each median-split group.
- A minimum wellbeing completion gap of 0.15.
- Spearman correlation of at least 0.30 where applicable.
- Materiality checks before displaying an association.

The association describes a historical relationship.

It must not be worded as proof that completing a habit causes a wellbeing change.

## Habit Consistency

Consistency is evaluated over a 28-day window.

At least 14 applicable days are required.

A wellbeing standard deviation of 0.20 or below may be described as relatively consistent.

A standard deviation of 0.35 or above may be described as more varied.

The wording must remain descriptive rather than clinical.

## NLP Trend Analysis

Existing NLP-derived signals are evaluated independently.

For each existing signal:

- Earlier period: 14 days.
- Recent period: 14 days.
- At least 4 analyzed days are required in each period.
- Material change is required before reporting the signal.

Only the single most changed qualifying NLP signal is selected.

The insight engine does not invent new emotional or psychological categories.

## Language Safety

Insight wording must remain cautious and observational.

The system must not use:

- Medical diagnoses.
- Clinical claims.
- Causal claims.
- Alarmist language.
- Commands or treatment directives.

Preferred language describes patterns such as:

- "Your recent scores were..."
- "This pattern appears..."
- "Compared with your previous period..."
- "Your data suggests..."
- "You may want to reflect on..."

The system must not claim that a habit caused a wellbeing change.

## Ranking and Deduplication

Each insight receives a deterministic key:

category:subject:direction:window

Duplicate insight keys are removed.

A maximum display limit is enforced.

Only one insight is retained per category after ranking.

Meaningful insights are prioritized over purely informational near-baseline observations.

When Trend and Recent Change describe the same direction:

- Keep Trend by default.
- Remove Recent Change unless its recent difference is at least twice the material threshold.

Ranking must remain deterministic so the same input data produces the same ordering.

## Persistence

Generated insights are persisted using the `insight_snapshots` table.

The persistence layer stores the generated insight metadata and key rather than journal text.

Each snapshot is associated with a specific user.

The user/key combination is unique.

Existing snapshots are updated rather than duplicated.

An insight is considered new when it was first generated within the previous 48 hours.

Concurrent generation must not create duplicate rows.

## API

The authenticated generated-insights endpoint is exposed through the insights API.

The endpoint:

- Requires authentication.
- Uses the authenticated user identity.
- Does not trust a client-provided user ID.
- Generates explainable insights from the user's own data.
- Returns generated insight records and metadata.
- Returns an appropriate empty state when there is insufficient data or no meaningful pattern.
- Does not expose journal text.

Persistence failures are logged rather than silently treated as successful persistence.

## Reason Codes and Data Sufficiency

Insight generation distinguishes between meaningful insights and insufficient historical evidence.

Insufficient data must not be presented as a negative wellbeing result.

Empty states may occur when:

- There is no relevant history.
- There are too few observations.
- There is no meaningful pattern.
- Existing data does not meet the configured materiality threshold.
- No new insight is available.

## User Isolation

Insight generation is always scoped to the authenticated user.

A client cannot request or retrieve another user's insights by supplying a different user ID.

Database queries and persisted snapshots must maintain user-level isolation.

Cross-user data must never influence an insight.

## Frontend Presentation

Insights are presented as explainable self-reflection information.

The interface should clearly communicate:

- Insight category.
- Insight title.
- Explanation.
- Supporting metrics where appropriate.
- Comparison period.
- Data sufficiency.
- Whether the insight is new.

The interface must provide appropriate loading, empty, insufficient-history, no-meaningful-pattern, no-new-insight, and error states.

Insights must not use alarming medical-style presentation.

## Limitations

MindMirror insights are descriptive summaries of patterns in a user's own historical data.

They are not predictions, diagnoses, medical measurements, or clinical assessments.

Historical association does not establish causation.

Limited data can produce insufficient or unstable patterns.

NLP-derived signals represent computational features and should not be interpreted as clinical assessments.

The Well-Being Index is a project-specific self-reflection metric and should not be treated as a medical score.

## Disclaimer

Insights describe patterns in your own historical data and are not medical or clinical measurements or advice.