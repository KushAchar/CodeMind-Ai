"""Reusable Qdrant client and connectivity checks."""

import logging
from functools import lru_cache

import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class QdrantConnectionError(RuntimeError):
    """Raised when Qdrant cannot be reached."""


@lru_cache
def get_qdrant_client() -> QdrantClient:
    """Return the process-wide Qdrant client."""
    return QdrantClient(url=get_settings().qdrant_url)


def check_qdrant_connection() -> None:
    """Verify Qdrant connectivity by requesting the collection list."""
    try:
        get_qdrant_client().get_collections()
    except (
        ResponseHandlingException,
        UnexpectedResponse,
        httpx.HTTPError,
        ValueError,
    ) as exc:
        logger.exception("Qdrant connectivity check failed")
        raise QdrantConnectionError("Qdrant is unavailable") from exc
