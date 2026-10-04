# Phase 8 â€” NLP Journal Analysis Notes

## 1. Purpose

MindMirror uses lightweight local NLP to extract linguistic signals from journal entries.

The NLP component does not diagnose, predict, or clinically assess a person's mental health.

The extracted signals are later intended to support the project's behavioral analytics and fuzzy-inference components.

---

## 2. NLP Library

MindMirror uses `vaderSentiment`.

VADER is a rule- and lexicon-based sentiment analysis tool.

It was selected because it:

- works locally
- does not require model training
- does not require an external API
- produces deterministic outputs
- is lightweight and explainable

No external LLM or external NLP API is used.

---

## 3. Two Preprocessing Paths

The journal text is never modified or truncated in the database.

Two separate representations are created.

### 3.1 VADER representation

VADER receives the journal text after trimming surrounding whitespace.

Capitalization and punctuation are preserved because they can contribute to VADER's analysis.

Example:

`I am VERY stressed!!!`

is passed to VADER without converting it to lowercase or removing punctuation.

### 3.2 Stress-lexicon representation

A separate tokenized representation is created for the stress-related linguistic indicator.

The tokens are:

- lowercased
- separated from punctuation
- stored only for analysis

Example:

`I am VERY stressed!!!`

becomes:

`i`, `am`, `very`, `stressed`

The original journal content is never changed.

---

## 4. Extracted Signals

MindMirror extracts four numerical signals.

### 4.1 Sentiment Score

Source:

VADER compound score.

Range:

`-1.0 to +1.0`

Interpretation:

- values closer to `+1.0` indicate more positive linguistic sentiment
- values closer to `-1.0` indicate more negative linguistic sentiment
- values around `0.0` indicate relatively neutral linguistic sentiment

The VADER compound score is stored directly without additional normalization.

---

### 4.2 Positive Emotion Score

Source:

VADER positive proportion (`pos`).

Range:

`0.0 to 1.0`

This represents the proportion of VADER's sentiment components associated with positive language.

---

### 4.3 Negative Emotion Score

Source:

VADER negative proportion (`neg`).

Range:

`0.0 to 1.0`

This represents the proportion of VADER's sentiment components associated with negative language.

---

### 4.4 Stress-Related Linguistic Indicator

MindMirror uses a small hand-curated lexicon containing stress-related terms.

Examples include:

- stressed
- stress
- overwhelmed
- anxious
- anxiety
- pressure
- deadline
- worried
- worry
- exhausted
- burnout
- panic
- rushed
- urgent
- tired
- frustrated

The complete lexicon is maintained in:

`app/services/nlp/analysis_service.py`

The indicator is calculated using:

`min(1.0, (stress_word_matches / total_tokens) * 10)`

The multiplication by `10` is a tunable heuristic. It is not a clinically validated stress model.

The system refers to this feature as a:

**stress-related linguistic indicator**

It is not a medical stress score or clinical stress level.

---

## 5. No Confidence Score

MindMirror does not store an NLP confidence score.

VADER does not provide a defensible probability that a journal entry belongs to a particular psychological category.

Therefore, adding an artificial confidence value would create false precision.

---

## 6. Analysis Lifecycle

NLP analysis runs synchronously when a journal is created.

The flow is:

Journal text
â†’ preprocessing
â†’ VADER and stress-lexicon extraction
â†’ four numerical signals
â†’ `journal_analysis` database row

When journal content is updated, the analysis is recalculated.

The existing analysis row for that journal is updated rather than creating a stale second analysis.

Each journal has at most one analysis row because `journal_id` is unique.

When a journal is deleted, its analysis is deleted through the existing database relationship and cascade behavior.

---

## 7. API

The existing read-only endpoint is used:

`GET /api/journals/{journal_id}/analysis`

No public endpoint is provided for manually submitting NLP analysis.

Analysis is generated internally from the journal content.

Ownership is enforced through the parent journal.

Unauthenticated requests return `401`.

Requests from another user return `404`.

---

## 8. Input Handling

MindMirror does not impose a word or character limit on journal entries.

The NLP pipeline supports:

- one-sentence entries
- paragraphs
- multiline entries
- long entries

Journal content is not truncated.

Whitespace-only entries are rejected by the existing journal validation before NLP processing.

---

## 9. Evaluation

The NLP engine was evaluated using representative positive, negative, neutral, stress-related, and mixed examples.

The evaluation checks whether the signals fall within their documented ranges and behave sensibly.

The evaluation is not a clinical accuracy study.

---

## 10. Limitations

The NLP approach is lightweight and intentionally explainable.

It may not correctly interpret:

- sarcasm
- complex negation
- subtle emotional context
- ambiguous wording
- context-dependent language
- language outside the assumptions of the VADER lexicon

The stress-related linguistic indicator is a simple keyword-based heuristic and should not be interpreted as a clinical measurement.

---

## 11. Non-Medical Disclaimer

MindMirror's NLP component extracts linguistic signals from journal text. These signals are not medical diagnoses, clinical assessments, or predictions of mental health conditions.