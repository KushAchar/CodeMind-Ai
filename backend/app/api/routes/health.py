"""Health and readiness endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.qdrant import QdrantConnectionError, check_qdrant_connection
from app.db.session import DatabaseConnectionError, check_database_connection
from app.core.config import get_settings
from app.schemas.common import DependencyHealthResponse, HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Check API health")
async def health_check() -> HealthResponse:
    """Return the current availability of the HTTP service."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get(
    "/health/ready",
    response_model=DependencyHealthResponse,
    summary="Check PostgreSQL and Qdrant connectivity",
)
async def readiness_check() -> DependencyHealthResponse | JSONResponse:
    """Report whether the application dependencies are reachable."""
    postgres_status = "ok"
    qdrant_status = "ok"

    try:
        check_database_connection()
    except DatabaseConnectionError:
        postgres_status = "unavailable"

    try:
        check_qdrant_connection()
    except QdrantConnectionError:
        qdrant_status = "unavailable"

    status = "ok" if postgres_status == qdrant_status == "ok" else "degraded"
    response = DependencyHealthResponse(
        status=status,
        postgres=postgres_status,
        qdrant=qdrant_status,
    )
    if status != "ok":
        return JSONResponse(status_code=503, content=response.model_dump())
    return response
