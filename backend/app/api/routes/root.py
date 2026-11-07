"""Root API endpoint."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import RootResponse

router = APIRouter(tags=["root"])


@router.get("/", response_model=RootResponse, summary="Get API information")
async def root() -> RootResponse:
    """Return basic information about the CodeMind AI API."""
    settings = get_settings()
    return RootResponse(
        message="Welcome to CodeMind AI",
        version=settings.app_version,
    )
