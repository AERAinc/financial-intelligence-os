from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.research.schemas import FormulaDefinitionRequest, BacktestEvaluationRequest, FormulaResearchResponse
from engines.research.laboratory import research_lab

router = APIRouter(prefix="/research", tags=["Formula Research Laboratory"])

@router.post(
    "/backtest",
    response_model=FormulaResearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Backtest a Custom Financial Formula or Ratio"
)
async def backtest_formula(
    definition: FormulaDefinitionRequest,
    backtest_payload: BacktestEvaluationRequest,
    tenant_id: str = Depends(get_current_tenant_id)
) -> FormulaResearchResponse:
    try:
        return research_lab.evaluate_formula_backtest(definition, backtest_payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))