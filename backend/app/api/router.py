"""Composition root for HTTP API routers."""

from fastapi import APIRouter

from app.api.routes import health, llm, repositories

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(llm.router)
api_router.include_router(repositories.router)
