"""Tests for the GitHub repository integration."""

import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest

from app.api.routes import repositories
from app.schemas.github import GitHubRepositoryResponse
from app.services.github import (
    GitHubRepositoryNotFoundError,
    GitHubService,
    InvalidGitHubRepositoryUrlError,
)


class FakeResponse:
    """Minimal response double for the GitHub service."""

    def __init__(self, status_code: int, payload: dict[str, object]) -> None:
        self.status_code = status_code
        self._payload = payload

    @property
    def is_error(self) -> bool:
        return self.status_code >= 400

    def json(self) -> dict[str, object]:
        return self._payload


class FakeAsyncClient:
    """Async client double that returns a configured GitHub response."""

    def __init__(self, response: FakeResponse, **_: object) -> None:
        self.response = response

    async def __aenter__(self) -> "FakeAsyncClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        return None

    async def get(self, _: str) -> FakeResponse:
        return self.response


def test_service_maps_github_repository_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {
        "name": "CodeMind-Ai",
        "description": "Developer assistant",
        "language": "Python",
        "default_branch": "main",
        "stargazers_count": 12,
        "forks_count": 3,
        "html_url": "https://github.com/KushAchar/CodeMind-Ai",
    }
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(FakeResponse(200, payload), **kwargs),
    )

    result = asyncio.run(
        GitHubService(
            api_url="https://api.github.com",
            timeout_seconds=5,
        ).get_repository("https://github.com/KushAchar/CodeMind-Ai")
    )

    assert result == GitHubRepositoryResponse(
        name="CodeMind-Ai",
        description="Developer assistant",
        primary_language="Python",
        default_branch="main",
        stars=12,
        forks=3,
        repository_url="https://github.com/KushAchar/CodeMind-Ai",
    )


def test_service_rejects_non_repository_github_url() -> None:
    with pytest.raises(InvalidGitHubRepositoryUrlError):
        GitHubService(
            api_url="https://api.github.com",
            timeout_seconds=5,
        )._extract_repository_path(
            "https://github.com/KushAchar/CodeMind-Ai/issues"
        )


def test_service_reports_missing_repository(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(FakeResponse(404, {}), **kwargs),
    )

    with pytest.raises(GitHubRepositoryNotFoundError):
        asyncio.run(
            GitHubService(
                api_url="https://api.github.com",
                timeout_seconds=5,
            ).get_repository("https://github.com/example/missing")
        )


def test_connect_endpoint_returns_structured_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AsyncMock()
    service.get_repository.return_value = GitHubRepositoryResponse(
        name="CodeMind-Ai",
        description=None,
        primary_language="Python",
        default_branch="main",
        stars=1,
        forks=0,
        repository_url="https://github.com/KushAchar/CodeMind-Ai",
    )
    monkeypatch.setattr(repositories, "get_github_service", lambda: service)

    response = asyncio.run(
        repositories.connect_repository(
            repositories.GitHubRepositoryConnectRequest(
                repository_url="https://github.com/KushAchar/CodeMind-Ai"
            )
        )
    )

    assert response == service.get_repository.return_value
