"""Schemas for LLM requests and responses."""

from pydantic import BaseModel, Field


class LLMTestRequest(BaseModel):
    """Request sent to the LLM test endpoint."""

    message: str = Field(..., min_length=1, max_length=10_000)


class LLMTestResponse(BaseModel):
    """Response returned by the LLM test endpoint."""

    success: bool
    response: str
