"""Tests for the initial HTTP API surface."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_application_information() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to CodeMind AI",
        "version": "1.0.0",
    }


def test_favicon_is_served() -> None:
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"


def test_health_returns_ok_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "CodeMind AI",
        "version": "1.0.0",
    }
