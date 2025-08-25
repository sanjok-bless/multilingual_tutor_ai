"""Tests for metrics endpoint."""

from fastapi.testclient import TestClient


def test_metrics_endpoint(client: TestClient) -> None:
    """Test metrics endpoint returns empty dict response."""
    response = client.get("/api/v1/metrics")

    assert response.status_code == 200
    data = response.json()
    assert data == {}
