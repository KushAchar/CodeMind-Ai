"""LLM test endpoint."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.llm import LLMTestRequest, LLMTestResponse
from app.services.ai.llm import LLMServiceError, get_llm_service

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post(
    "/test",
    response_model=LLMTestResponse,
    summary="Generate a test LLM response",
)
def test_llm(request: LLMTestRequest) -> LLMTestResponse | JSONResponse:
    """Generate a response using the configured LLM provider."""
    try:
        response = get_llm_service().generate(request.message)
    except LLMServiceError as exc:
        return JSONResponse(
            status_code=503,
            content={"success": False, "response": str(exc)},
        )
    return LLMTestResponse(success=True, response=response)
