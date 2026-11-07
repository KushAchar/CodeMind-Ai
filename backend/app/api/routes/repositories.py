"""Repository registration and management endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.github import (
    GitHubRepositoryConnectRequest,
    GitHubRepositoryResponse,
)
from app.services.github import (
    GitHubAPIError,
    GitHubRepositoryNotFoundError,
    InvalidGitHubRepositoryUrlError,
    get_github_service,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.post(
    "/connect",
    response_model=GitHubRepositoryResponse,
    summary="Connect a public GitHub repository",
)
async def connect_repository(
    request: GitHubRepositoryConnectRequest,
) -> GitHubRepositoryResponse | JSONResponse:
    """Fetch metadata for a public GitHub repository."""
    try:
        return await get_github_service().get_repository(str(request.repository_url))
    except InvalidGitHubRepositoryUrlError as exc:
        return JSONResponse(status_code=422, content={"detail": str(exc)})
    except GitHubRepositoryNotFoundError as exc:
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    except GitHubAPIError as exc:
        return JSONResponse(status_code=503, content={"detail": str(exc)})
