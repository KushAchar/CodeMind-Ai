"""Shared API response schemas."""

from pydantic import BaseModel


class RootResponse(BaseModel):
    """Response returned by the API root endpoint."""

    message: str
    version: str


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    status: str
    service: str
    version: str


class DependencyHealthResponse(BaseModel):
    """Response returned by the dependency readiness endpoint."""

    status: str
    postgres: str
    qdrant: str
