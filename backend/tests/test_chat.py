"""Tests for chat endpoint."""

from fastapi.testclient import TestClient


def test_chat_endpoint(client: TestClient) -> None:
    """Test chat endpoint returns empty dict response."""
    response = client.post("/api/v1/chat")

    assert response.status_code == 200
    data = response.json()
    assert data == {}


def test_languages_endpoint(client: TestClient) -> None:
    """Test languages endpoint returns list of supported languages."""
    response = client.get("/api/v1/languages")

    assert response.status_code == 200
    data = response.json()
    assert data == ["EN", "UK", "PL", "DE"]
    assert isinstance(data, list)
    assert len(data) == 4
