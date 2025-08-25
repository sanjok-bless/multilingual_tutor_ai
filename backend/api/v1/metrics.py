"""Metrics endpoint for application monitoring and observability."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
async def metrics_endpoint() -> dict:
    """
    Metrics endpoint for application monitoring.

    Returns basic application metrics in a simple format for MVP.
    Future implementation will provide Prometheus-compatible metrics
    including request counts, response times, and system health indicators.

    Returns:
        dict: Empty dict placeholder for MVP setup.
    """
    return {}
