"""Pydantic schemas and data models for chat functionality."""

import uuid
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


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


class Correction(BaseModel):
    """Model for individual language corrections."""

    original: str = Field(..., min_length=1, description="Original incorrect text")
    corrected: str = Field(..., min_length=1, description="Corrected version of the text")
    explanation: list[str] = Field(..., description="Structured explanation as [category, description]")
    error_type: ErrorType = Field(..., description="Type of error being corrected")

    @field_validator("explanation")
    @classmethod
    def validate_explanation_length(cls, v: list[str]) -> list[str]:
        """Validate explanation has exactly 2 elements."""
        if len(v) != 2:
            msg = "Explanation must have exactly 2 elements: [category, description]"
            raise ValueError(msg)
        return v


class ChatRequest(BaseModel):
    """Model for incoming chat requests."""

    message: str = Field(..., min_length=1, description="User's message to be processed")
    language: Language = Field(..., description="Target language for correction")
    level: Level = Field(..., description="User's proficiency level")
    session_id: str = Field(..., description="UUID session identifier")

    @field_validator("session_id")
    @classmethod
    def validate_session_id_format(cls, v: str) -> str:
        """Validate session_id is a valid UUID format."""
        try:
            uuid.UUID(v)
        except ValueError as e:
            msg = "session_id must be a valid UUID format"
            raise ValueError(msg) from e
        return v


class ChatResponse(BaseModel):
    """Model for AI chat responses."""

    ai_response: str = Field(..., min_length=1, description="AI's natural explanation or positive feedback")
    next_phrase: str = Field(..., min_length=1, description="AI's conversational response/next phrase")
    corrections: list[Correction] = Field(default=[], description="List of corrections made")
    session_id: str = Field(..., description="UUID session identifier from request")
    tokens_used: int = Field(..., gt=0, description="Number of tokens consumed by the request")
