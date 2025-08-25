"""Chat endpoint for multilingual AI tutoring interactions."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat_endpoint() -> dict:
    """
    Main chat endpoint for AI tutoring sessions.

    Handles multilingual conversational practice with real-time grammar corrections
    and explanations. Future implementation will accept user messages and return
    AI responses with structured corrections.

    Returns:
        dict: Empty response for MVP setup.
    """
    return {}


@router.get("/languages")
async def get_languages() -> list[str]:
    """
    Get supported languages for the tutoring platform.

    Returns:
        list[str]: List of supported language codes.
    """
    # TODO: Load supported languages from environment configuration
    return ["EN"]
