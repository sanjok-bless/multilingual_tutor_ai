"""Health check endpoint for monitoring service availability."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint for monitoring and load balancer probes.

    Returns:
        dict: Service health status with timestamp and message.
    """
    return {"status": "healthy", "message": "Multilingual AI Tutor is running"}
