"""Tests for Pydantic schemas and data models."""

import uuid

import pytest
from pydantic import ValidationError

from backend.chat.schemas import (
    ChatRequest,
    ChatResponse,
    Correction,
    ErrorType,
    Language,
    Level,
)


class TestLanguageEnum:
    """Test Language enum validation."""

    def test_valid_language_codes(self) -> None:
        """Test valid language codes are accepted."""
        assert Language.EN == "EN"
        assert Language.DE == "DE"
        assert Language.PL == "PL"
        assert Language.UK == "UK"

    def test_invalid_language_code_raises_error(self) -> None:
        """Test invalid language code raises ValidationError."""
        with pytest.raises(ValueError):
            Language("FR")


class TestLevelEnum:
    """Test Level enum validation."""

    def test_valid_level_codes(self) -> None:
        """Test valid CEFR level codes are accepted."""
        assert Level.A1 == "A1"
        assert Level.A2 == "A2"
        assert Level.B1 == "B1"
        assert Level.B2 == "B2"
        assert Level.C1 == "C1"
        assert Level.C2 == "C2"

    def test_invalid_level_code_raises_error(self) -> None:
        """Test invalid level code raises ValidationError."""
        with pytest.raises(ValueError):
            Level("D1")


class TestErrorTypeEnum:
    """Test ErrorType enum validation."""

    def test_valid_error_types(self) -> None:
        """Test valid error types are accepted."""
        assert ErrorType.GRAMMAR == "GRAMMAR"
        assert ErrorType.VOCABULARY == "VOCABULARY"
        assert ErrorType.SPELLING == "SPELLING"
        assert ErrorType.PUNCTUATION == "PUNCTUATION"


class TestCorrectionModel:
    """Test Correction Pydantic model with structured explanation format."""

    def test_valid_correction_creation(self) -> None:
        """Test valid correction model creation with structured explanation."""
        correction = Correction(
            original="I have meeting tomorrow",
            corrected="I have a meeting tomorrow",
            explanation=["Missing Article", "'a' before noun (required for countable nouns)"],
            error_type=ErrorType.GRAMMAR,
        )

        assert correction.original == "I have meeting tomorrow"
        assert correction.corrected == "I have a meeting tomorrow"
        assert correction.explanation == ["Missing Article", "'a' before noun (required for countable nouns)"]
        assert correction.error_type == ErrorType.GRAMMAR

    def test_correction_with_vowel_sound_example(self) -> None:
        """Test correction with vowel sound explanation from demo."""
        correction = Correction(
            original="important meeting",
            corrected="an important meeting",
            explanation=["Missing Article", "\"an\" important meeting (use 'an' before vowel sounds)"],
            error_type=ErrorType.GRAMMAR,
        )

        assert correction.explanation[0] == "Missing Article"
        assert correction.explanation[1] == "\"an\" important meeting (use 'an' before vowel sounds)"

    def test_correction_with_infinitive_example(self) -> None:
        """Test correction with infinitive explanation from demo."""
        correction = Correction(
            original="need practice",
            corrected="need to practice",
            explanation=["Infinitive Marker", "\"need to practice\" (infinitive required after 'need')"],
            error_type=ErrorType.GRAMMAR,
        )

        assert correction.explanation[0] == "Infinitive Marker"
        assert correction.explanation[1] == "\"need to practice\" (infinitive required after 'need')"

    def test_correction_requires_all_fields(self) -> None:
        """Test correction model requires all fields."""
        with pytest.raises(ValidationError):
            Correction(
                original="test",
                corrected="test",
                # Missing explanation and error_type
            )

    def test_correction_validates_non_empty_strings(self) -> None:
        """Test correction model validates non-empty strings."""
        with pytest.raises(ValidationError):
            Correction(
                original="",  # Empty string should fail
                corrected="test",
                explanation=["Grammar", "test explanation"],
                error_type=ErrorType.GRAMMAR,
            )

    def test_correction_validates_explanation_length(self) -> None:
        """Test correction validates explanation has exactly 2 elements."""
        with pytest.raises(ValidationError):
            Correction(
                original="test",
                corrected="test fixed",
                explanation=["Grammar"],  # Missing second element
                error_type=ErrorType.GRAMMAR,
            )

        with pytest.raises(ValidationError):
            Correction(
                original="test",
                corrected="test fixed",
                explanation=["Grammar", "explanation", "extra"],  # Too many elements
                error_type=ErrorType.GRAMMAR,
            )

    def test_spelling_error_type(self) -> None:
        """Test spelling error correction."""
        correction = Correction(
            original="recieve",
            corrected="receive",
            explanation=["Spelling", '"receive" (i before e except after c)'],
            error_type=ErrorType.SPELLING,
        )

        assert correction.error_type == ErrorType.SPELLING
        assert correction.explanation[1] == '"receive" (i before e except after c)'

    def test_punctuation_error_type(self) -> None:
        """Test punctuation error correction."""
        correction = Correction(
            original="Hello how are you",
            corrected="Hello, how are you?",
            explanation=["Punctuation", "comma after greeting, question mark for question"],
            error_type=ErrorType.PUNCTUATION,
        )

        assert correction.error_type == ErrorType.PUNCTUATION
        assert correction.explanation[1] == "comma after greeting, question mark for question"

    def test_vocabulary_error_type(self) -> None:
        """Test vocabulary error correction."""
        correction = Correction(
            original="I'm very happy",
            corrected="I'm delighted",
            explanation=["Vocabulary", "\"delighted\" (more formal than 'very happy')"],
            error_type=ErrorType.VOCABULARY,
        )

        assert correction.error_type == ErrorType.VOCABULARY
        assert correction.explanation[1] == "\"delighted\" (more formal than 'very happy')"


class TestChatRequestModel:
    """Test ChatRequest Pydantic model."""

    def test_valid_chat_request_creation(self) -> None:
        """Test valid chat request model creation with UUID session_id."""
        session_id = str(uuid.uuid4())
        request = ChatRequest(
            message="Hello, how are you?",
            language=Language.EN,
            level=Level.B1,
            session_id=session_id,
        )

        assert request.message == "Hello, how are you?"
        assert request.language == Language.EN
        assert request.level == Level.B1
        assert request.session_id == session_id

    def test_chat_request_requires_all_fields(self) -> None:
        """Test chat request requires all fields."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Hello",
                language=Language.EN,
                # Missing level and session_id
            )

    def test_chat_request_validates_message_not_empty(self) -> None:
        """Test chat request validates message is not empty."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="",  # Empty message should fail
                language=Language.EN,
                level=Level.B1,
                session_id=str(uuid.uuid4()),
            )

    def test_chat_request_validates_uuid_session_id_format(self) -> None:
        """Test chat request validates UUID session ID format."""
        # Valid UUID format should pass
        valid_uuid = str(uuid.uuid4())
        request = ChatRequest(
            message="Hello",
            language=Language.EN,
            level=Level.B1,
            session_id=valid_uuid,
        )
        assert request.session_id == valid_uuid

        # Invalid UUID format should fail
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Hello",
                language=Language.EN,
                level=Level.B1,
                session_id="not-a-uuid",
            )


class TestChatResponseModel:
    """Test ChatResponse Pydantic model with ai_response and next_phrase fields."""

    def test_valid_chat_response_creation_with_corrections(self) -> None:
        """Test valid chat response model creation with natural error explanations."""
        correction = Correction(
            original="I have meeting",
            corrected="I have a meeting",
            explanation=["Missing Article", '"a" before noun (required for countable nouns)'],
            error_type=ErrorType.GRAMMAR,
        )

        session_id = str(uuid.uuid4())
        response = ChatResponse(
            ai_response="I have **a** meeting tomorrow. Remember to use 'a' before countable nouns!",
            next_phrase="That sounds important! What's the meeting about?",
            corrections=[correction],
            session_id=session_id,
            tokens_used=50,
        )

        assert "Remember to use 'a' before countable nouns" in response.ai_response
        assert response.next_phrase == "That sounds important! What's the meeting about?"
        assert len(response.corrections) == 1
        assert response.corrections[0] == correction
        assert response.session_id == session_id
        assert response.tokens_used == 50

    def test_chat_response_perfect_english_no_corrections(self) -> None:
        """Test chat response when English is perfect - positive feedback in ai_response."""
        response = ChatResponse(
            ai_response="Excellent! Your English is perfect.",
            next_phrase="Let's continue our conversation. What would you like to talk about?",
            corrections=[],
            session_id=str(uuid.uuid4()),
            tokens_used=30,
        )

        assert response.ai_response == "Excellent! Your English is perfect."
        assert response.next_phrase == "Let's continue our conversation. What would you like to talk about?"
        assert len(response.corrections) == 0

    def test_chat_response_requires_positive_tokens(self) -> None:
        """Test chat response requires positive token count."""
        with pytest.raises(ValidationError):
            ChatResponse(
                ai_response="Test ai response",
                next_phrase="Test next phrase",
                corrections=[],
                session_id=str(uuid.uuid4()),
                tokens_used=-1,  # Negative tokens should fail
            )

    def test_chat_response_validates_non_empty_next_phrase(self) -> None:
        """Test chat response validates next_phrase is not empty."""
        with pytest.raises(ValidationError):
            ChatResponse(
                ai_response="Test ai response",
                next_phrase="",  # Empty next phrase should fail
                corrections=[],
                session_id=str(uuid.uuid4()),
                tokens_used=10,
            )

    def test_chat_response_validates_non_empty_ai_response(self) -> None:
        """Test chat response validates ai_response is not empty."""
        with pytest.raises(ValidationError):
            ChatResponse(
                ai_response="",  # Empty ai response should fail
                next_phrase="Test next phrase",
                corrections=[],
                session_id=str(uuid.uuid4()),
                tokens_used=10,
            )

    def test_chat_response_with_multiple_corrections_demo_format(self) -> None:
        """Test chat response with multiple corrections and natural explanations."""
        corrections = [
            Correction(
                original="important meeting",
                corrected="an important meeting",
                explanation=["Missing Article", "\"an\" important meeting (use 'an' before vowel sounds)"],
                error_type=ErrorType.GRAMMAR,
            ),
            Correction(
                original="need practice",
                corrected="need to practice",
                explanation=["Infinitive Marker", "\"need to practice\" (infinitive required after 'need')"],
                error_type=ErrorType.GRAMMAR,
            ),
        ]

        ai_response_text = (
            "I have **an** important meeting tomorrow and I need **to** practice my presentation skills. "
            "Great topic! Remember: use 'an' before vowel sounds like 'important', and always include "
            "'to' after 'need' when followed by a verb. These small details make your English sound natural!"
        )
        next_phrase_text = (
            "Great! I'd be happy to help you practice. Presentations can be nerve-wracking, "
            "but practice makes perfect. What's your presentation about?"
        )

        response = ChatResponse(
            ai_response=ai_response_text,
            next_phrase=next_phrase_text,
            corrections=corrections,
            session_id=str(uuid.uuid4()),
            tokens_used=75,
        )

        assert len(response.corrections) == 2
        assert "use 'an' before vowel sounds" in response.ai_response
        assert "include 'to' after 'need'" in response.ai_response
        assert "These small details make your English sound natural!" in response.ai_response
        assert response.next_phrase == next_phrase_text
        assert response.corrections[0].explanation[0] == "Missing Article"
        assert response.corrections[0].explanation[1] == "\"an\" important meeting (use 'an' before vowel sounds)"
        assert response.corrections[1].explanation[0] == "Infinitive Marker"
        assert response.corrections[1].explanation[1] == "\"need to practice\" (infinitive required after 'need')"
