"""Schemas for GitHub repository integration."""

from pydantic import BaseModel, HttpUrl


class GitHubRepositoryConnectRequest(BaseModel):
    """Request body used to connect a public GitHub repository."""

    repository_url: HttpUrl


class GitHubRepositoryResponse(BaseModel):
    """Public repository metadata returned by GitHub."""

    name: str
    description: str | None
    primary_language: str | None
    default_branch: str
    stars: int
    forks: int
    repository_url: HttpUrl
