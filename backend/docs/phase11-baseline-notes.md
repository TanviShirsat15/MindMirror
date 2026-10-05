# Phase 11 — Personal Baseline & Historical Data

## Personal Baseline Methodology

The personal baseline is calculated only from the same user's previous valid well-being scores.

A score is eligible when:
- It belongs to the current user.
- Its score date is strictly before the target date.
- The score is numeric and within the valid 1–100 range.
- The current score is excluded.
- Future scores are excluded.

The most recent 7 valid previous scores are considered.

A minimum of 3 previous valid scores is required:
- 0–2 previous scores → `insufficient_history`
- 3–7 previous scores → average all valid scores
- More than 7 → average the most recent 7 valid scores

The baseline is displayed to one decimal place.

Irregular dates and missing dates do not affect the calculation because the method uses valid historical scores rather than requiring consecutive dates.

## Baseline Comparison

The named application-level tolerance is:

`BASELINE_NEAR_TOLERANCE = 5.0`

Comparison is calculated as:

`difference = current score - personal baseline`

Results:
- Difference > +5 → `above`
- Difference < -5 → `below`
- Difference between -5 and +5 inclusive → `near`

This comparison is an application-level historical reference and is not a clinical threshold.

## Baseline Statuses

The system uses:
- `no_score`
- `insufficient_history`
- `baseline_available`

When a baseline is unavailable, the system does not substitute zero, `NaN`, or another artificial value.

## Historical Habit Handling

Habit history is evaluated according to whether the habit was applicable on the historical date.

A habit is applicable when:

`created_date <= historical_date`

and:

`deactivated_at IS NULL OR historical_date < deactivated_at`

When a habit is deactivated, `deactivated_at` is recorded. When it is reactivated, `deactivated_at` is cleared.

This allows historical well-being calculations to preserve the habits that were actually applicable on the date being analyzed.

The Phase 11 migration adds the nullable `deactivated_at` column. Existing active habits receive `NULL`. For existing inactive habits where the original deactivation date is unknown, the migration conservatively leaves the value `NULL`; therefore the historical applicability of those older inactive habits may be treated as active. This limitation is documented rather than inventing a historical date.

## Existing Historical Scores

Existing stored historical well-being scores are not recalculated or overwritten solely because Phase 11 was introduced.

The personal baseline is calculated from historical scores when requested.

`baseline_value` may contain a stored snapshot from a score recalculation, while the baseline calculation used for the API response is derived from the user's valid historical scores.

## API Response

The well-being endpoint returns:

- `date`
- `status`
- `score`
- `baseline`
- `difference`
- `comparison`
- `baseline_sample_size`
- compact historical score information

The endpoint is user-scoped and does not use another user's scores when calculating a baseline.

## Data Isolation

Baseline calculations use only the authenticated user's historical scores.

Cross-user data is never included in the baseline calculation.

## Duplicate Prevention

The database maintains one well-being score per user per date through the unique constraint:

`uq_wellbeing_scores_user_date`

Repeated baseline calculation does not create additional well-being score records.

## Limitations

The personal baseline is an application-level historical reference and not a medical or clinical benchmark.

The baseline describes the user's own historical scoring pattern and should not be interpreted as a diagnosis, medical measurement, or universal well-being standard.
