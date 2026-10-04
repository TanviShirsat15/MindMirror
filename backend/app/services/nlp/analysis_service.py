"""NLP feature extraction for MindMirror journal entries."""


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.services.nlp.preprocessing import preprocess_journal_text


# Hand-curated terms used only to identify stress-related language.
# This is a simple linguistic heuristic, not a validated stress model.
STRESS_LEXICON = {
    "stressed",
    "stress",
    "overwhelmed",
    "overwhelm",
    "anxious",
    "anxiety",
    "pressure",
    "pressured",
    "deadline",
    "deadlines",
    "worried",
    "worry",
    "worrying",
    "exhausted",
    "exhausting",
    "burned",
    "burnout",
    "panic",
    "panicked",
    "rushed",
    "urgent",
    "urgency",
    "tired",
    "frustrated",
    "frustration",
}


_sentiment_analyzer = SentimentIntensityAnalyzer()


def analyze_journal_text(content: str) -> dict[str, float]:
    """
    Extract lightweight linguistic signals from journal text.

    Returns:
        sentiment_score:
            VADER compound score in the range -1.0 to 1.0.

        positive_emotion_score:
            VADER positive proportion in the range 0.0 to 1.0.

        negative_emotion_score:
            VADER negative proportion in the range 0.0 to 1.0.

        stress_indicator:
            A stress-related linguistic indicator in the range 0.0 to 1.0.
            Formula:
                min(1.0, (stress_word_matches / total_tokens) * 10)
    """
    processed = preprocess_journal_text(content)

    sentiment = _sentiment_analyzer.polarity_scores(
        processed.vader_text
    )

    total_tokens = len(processed.stress_tokens)

    stress_word_matches = sum(
        1
        for token in processed.stress_tokens
        if token in STRESS_LEXICON
    )

    if total_tokens == 0:
        stress_indicator = 0.0
    else:
        stress_indicator = min(
            1.0,
            (stress_word_matches / total_tokens) * 10,
        )

    return {
        "sentiment_score": float(sentiment["compound"]),
        "positive_emotion_score": float(sentiment["pos"]),
        "negative_emotion_score": float(sentiment["neg"]),
        "stress_indicator": float(stress_indicator),
    }