"""Common enums used across the application."""

from enum import StrEnum


class Language(StrEnum):
    """Supported languages for tutoring sessions."""

    EN = "EN"
    DE = "DE"
    PL = "PL"
    UK = "UK"


class Level(StrEnum):
    """CEFR language proficiency levels."""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class ErrorType(StrEnum):
    """Types of language errors that can be corrected."""

    GRAMMAR = "GRAMMAR"
    VOCABULARY = "VOCABULARY"
    SPELLING = "SPELLING"
    PUNCTUATION = "PUNCTUATION"
