"""FastAPI application entry point."""

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.api.router import api_router
from app.api.routes import root
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()
favicon_path = Path(__file__).resolve().parents[2] / "frontend" / "public" / "favicon.svg"

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(api_router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """Serve the shared application favicon."""
    return FileResponse(favicon_path, media_type="image/svg+xml")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return a stable error shape for invalid request data."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation failed",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Log unexpected failures and avoid exposing internal details."""
    logger.exception("Unhandled exception while processing %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)