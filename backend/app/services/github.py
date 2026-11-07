"""GitHub REST API integration for public repository metadata."""

from __future__ import annotations

from functools import lru_cache
from urllib.parse import urlparse

import httpx

from app.core.config import get_settings
from app.schemas.github import GitHubRepositoryResponse


class GitHubServiceError(Exception):
    """Base exception for expected GitHub integration failures."""


class InvalidGitHubRepositoryUrlError(GitHubServiceError):
    """Raised when a URL is not a supported public GitHub repository URL."""


class GitHubRepositoryNotFoundError(GitHubServiceError):
    """Raised when GitHub cannot find the requested repository."""


class GitHubAPIError(GitHubServiceError):
    """Raised when GitHub is unavailable or returns an unexpected response."""


class GitHubService:
    """Fetch metadata for public repositories from the GitHub REST API."""

    def __init__(
        self,
        api_url: str,
        timeout_seconds: float,
        token: str | None = None,
    ) -> None:
        self._api_url = api_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout_seconds)
        self._token = token

    async def get_repository(
        self,
        repository_url: str,
    ) -> GitHubRepositoryResponse:
        """Validate a repository URL and return its public GitHub metadata."""
        owner, name = self._extract_repository_path(repository_url)
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "CodeMind-AI",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            async with httpx.AsyncClient(
                timeout=self._timeout,
                headers=headers,
            ) as client:
                response = await client.get(
                    f"{self._api_url}/repos/{owner}/{name}",
                )
        except httpx.TimeoutException as exc:
            raise GitHubAPIError(
                "GitHub did not respond before the request timed out."
            ) from exc
        except httpx.RequestError as exc:
            raise GitHubAPIError(
                "GitHub could not be reached."
            ) from exc

        if response.status_code == 404:
            raise GitHubRepositoryNotFoundError(
                "The GitHub repository does not exist or is not public."
            )
        if response.is_error:
            raise GitHubAPIError(
                f"GitHub returned an unexpected status ({response.status_code})."
            )

        try:
            payload = response.json()
            return GitHubRepositoryResponse(
                name=payload["name"],
                description=payload.get("description"),
                primary_language=payload.get("language"),
                default_branch=payload["default_branch"],
                stars=payload["stargazers_count"],
                forks=payload["forks_count"],
                repository_url=payload["html_url"],
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise GitHubAPIError(
                "GitHub returned an invalid repository response."
            ) from exc

    @staticmethod
    def _extract_repository_path(repository_url: str) -> tuple[str, str]:
        """Extract owner and repository name from a supported GitHub URL."""
        parsed_url = urlparse(repository_url)
        if (
            parsed_url.scheme != "https"
            or parsed_url.netloc.lower() != "github.com"
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise InvalidGitHubRepositoryUrlError(
                "Use a public GitHub URL such as "
                "https://github.com/owner/repository."
            )

        path_parts = [
            part for part in parsed_url.path.strip("/").split("/") if part
        ]
        if len(path_parts) != 2:
            raise InvalidGitHubRepositoryUrlError(
                "Use a repository URL without issues, pull requests, or file paths."
            )

        owner, name = path_parts
        if name.endswith(".git"):
            name = name[:-4]
        if not owner or not name:
            raise InvalidGitHubRepositoryUrlError(
                "Both the GitHub owner and repository name are required."
            )
        return owner, name


@lru_cache
def get_github_service() -> GitHubService:
    """Return the process-wide configured GitHub service."""
    settings = get_settings()
    return GitHubService(
        api_url=settings.github_api_url,
        timeout_seconds=settings.github_timeout_seconds,
        token=settings.github_token,
    )
