"""
Pytest configuration and shared fixtures for backend tests.

Provides common test fixtures including FastAPI test client setup
and application instance configuration for consistent testing across
all test modules.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
