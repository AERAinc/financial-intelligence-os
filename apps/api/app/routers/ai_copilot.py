from fastapi import APIRouter, HTTPException
from engines.ai.copilot import copilot_engine, CopilotQueryRequest, CopilotResponse

router = APIRouter(prefix="/api/v1/ai", tags=["AI Financial Copilot"])

@router.post("/copilot", response_model=CopilotResponse)
def invoke_financial_copilot(payload: CopilotQueryRequest):
    """
    Overhauled Copilot Endpoint: Accepts natural language queries combined with arbitrary 
    engine context (accounting, valuation, credit, etc.) to produce audited responses.
    """
    try:
        response = copilot_engine.resolve_query(payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Copilot execution failed: {str(e)}")