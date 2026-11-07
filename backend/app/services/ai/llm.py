"""Provider-independent LLM service with a Groq implementation."""

import logging
from functools import lru_cache
from typing import Protocol

from groq import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    Groq,
    RateLimitError,
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class LLMServiceError(RuntimeError):
    """Raised when an LLM request cannot be completed."""


class LLMService(Protocol):
    """Interface implemented by supported LLM providers."""

    def generate(self, message: str) -> str:
        """Generate a response for a user message."""


class GroqLLMService:
    """Generate chat completions through the Groq SDK."""

    def __init__(self, client: Groq, model: str) -> None:
        self._client = client
        self._model = model

    def generate(self, message: str) -> str:
        """Generate one response without exposing provider credentials."""
        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": message}],
            )
            response = completion.choices[0].message.content
            if not response:
                raise LLMServiceError("The LLM returned an empty response")
            return response
        except LLMServiceError:
            raise
        except (AttributeError, IndexError, TypeError) as exc:
            logger.error("Groq returned an invalid completion")
            raise LLMServiceError("The LLM provider returned an invalid response") from exc
        except (APIConnectionError, APITimeoutError) as exc:
            logger.warning("Groq request could not connect: %s", exc.__class__.__name__)
            raise LLMServiceError("The LLM provider is unavailable") from exc
        except RateLimitError as exc:
            logger.warning("Groq rate limit reached")
            raise LLMServiceError("The LLM provider rate limit was reached") from exc
        except APIError as exc:
            logger.error("Groq API request failed: %s", exc.__class__.__name__)
            raise LLMServiceError("The LLM provider rejected the request") from exc


@lru_cache
def get_llm_service() -> LLMService:
    """Return the process-wide configured LLM provider."""
    settings = get_settings()
    if not settings.groq_api_key:
        raise LLMServiceError("GROQ_API_KEY is not configured")
    try:
        client = Groq(api_key=settings.groq_api_key)
    except ValueError as exc:
        logger.error("Groq client configuration is invalid")
        raise LLMServiceError("The LLM provider configuration is invalid") from exc
    return GroqLLMService(client=client, model=settings.groq_model)
