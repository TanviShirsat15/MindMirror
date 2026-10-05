# MindMirror — Phase 9 Fuzzy Inference Engine Notes

## 1. Purpose

Phase 9 implements the Mamdani Fuzzy Inference Engine used to calculate the MindMirror Well-Being Index.

The engine takes three already-prepared crisp inputs:

1. Sentiment score
2. Stress-related linguistic indicator
3. Habit consistency

The processing pipeline is:

Crisp Inputs
→ Fuzzification
→ Rule Evaluation
→ Rule Aggregation
→ Centroid Defuzzification
→ Well-Being Index

The fuzzy engine is implemented as a standalone, deterministic, and unit-testable Python module.

It does not directly access the database, FastAPI routes, journal services, habit services, or NLP services.

---

## 2. Inputs

### 2.1 Sentiment Score

Source: Phase 8 NLP analysis.

Range:

- Minimum: -1.0
- Maximum: 1.0

Interpretation:

- Negative
- Neutral
- Positive

The sentiment score is produced by VADER sentiment analysis.

---

### 2.2 Stress-Related Linguistic Indicator

Source: Phase 8 NLP analysis.

Range:

- Minimum: 0.0
- Maximum: 1.0

Interpretation:

- Low
- Medium
- High

This value represents a linguistic indicator derived from stress-related words in journal text.

It is not a medical stress measurement or clinical assessment.

---

### 2.3 Habit Consistency

Source: Phase 7 habit completion data.

Range:

- Minimum: 0.0
- Maximum: 1.0

Interpretation:

- Low
- Medium
- High

Habit consistency represents the user's observed habit completion consistency.

---

## 3. Membership Functions

The membership functions are engineering and design choices for the MindMirror system. They are not clinically validated thresholds.

### 3.1 Sentiment Membership Functions

Sentiment range: -1.0 to 1.0.

#### Negative

```text
trapmf(-1.0, -1.0, -0.5, 0.0)

---

## 4. Rule Generation

The rule base contains all possible combinations of the three input linguistic variables.

There are:

3 sentiment terms × 3 stress terms × 3 habit terms = 27 rules

Instead of manually assigning 27 unrelated rules, each rule is generated using a direction-sum formula.

### Direction Values

Favorable conditions receive `+1`:

- Positive sentiment = +1
- Low stress = +1
- High habit consistency = +1

Neutral conditions receive `0`:

- Neutral sentiment = 0
- Medium stress = 0
- Medium habit consistency = 0

Unfavorable conditions receive `-1`:

- Negative sentiment = -1
- High stress = -1
- Low habit consistency = -1

For every rule:

```text
direction_sum =
    sentiment_direction
    + stress_direction
    + habit_direction