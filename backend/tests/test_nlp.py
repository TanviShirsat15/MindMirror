from app.services.nlp.analysis_service import analyze_journal_text


def assert_valid_analysis(result):
    assert set(result.keys()) == {
        "sentiment_score",
        "positive_emotion_score",
        "negative_emotion_score",
        "stress_indicator",
    }

    assert -1.0 <= result["sentiment_score"] <= 1.0
    assert 0.0 <= result["positive_emotion_score"] <= 1.0
    assert 0.0 <= result["negative_emotion_score"] <= 1.0
    assert 0.0 <= result["stress_indicator"] <= 1.0


def test_positive_text():
    result = analyze_journal_text(
        "I had a wonderful and happy day today!"
    )

    assert_valid_analysis(result)
    assert result["sentiment_score"] > 0
    assert result["positive_emotion_score"] > 0


def test_negative_text():
    result = analyze_journal_text(
        "Today was terrible and disappointing."
    )

    assert_valid_analysis(result)
    assert result["sentiment_score"] < 0
    assert result["negative_emotion_score"] > 0


def test_neutral_text():
    result = analyze_journal_text(
        "I went to college and completed my assignment."
    )

    assert_valid_analysis(result)


def test_stress_related_text():
    result = analyze_journal_text(
        "I am overwhelmed and worried about my deadline."
    )

    assert_valid_analysis(result)
    assert result["stress_indicator"] > 0


def test_short_entry():
    result = analyze_journal_text("Good.")

    assert_valid_analysis(result)


def test_multiline_entry():
    result = analyze_journal_text(
        "Today was productive.\n\n"
        "I completed my assignment.\n"
        "I feel happy about it."
    )

    assert_valid_analysis(result)


def test_long_entry():
    content = "I had a good day. " * 500

    result = analyze_journal_text(content)

    assert_valid_analysis(result)