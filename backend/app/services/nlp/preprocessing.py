"""Text preprocessing helpers for MindMirror NLP."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PreprocessedJournalText:
    """Two representations of the same journal text."""

    vader_text: str
    stress_tokens: tuple[str, ...]


_WORD_PATTERN = re.compile(
    r"[^\W_]+(?:['’][^\W_]+)?",
    flags=re.UNICODE,
)


def preprocess_journal_text(content: str) -> PreprocessedJournalText:
    """
    Prepare journal text for the two NLP paths.

    VADER receives trimmed but otherwise unchanged text so that
    capitalization and punctuation are preserved.

    Stress analysis receives a separate lowercase tokenized copy.
    The original journal content is never modified.
    """
    vader_text = content.strip()

    stress_tokens = tuple(
        token.lower()
        for token in _WORD_PATTERN.findall(vader_text)
    )

    return PreprocessedJournalText(
        vader_text=vader_text,
        stress_tokens=stress_tokens,
    )