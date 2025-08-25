"""Tests for health endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Test health endpoint returns successful response."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data
