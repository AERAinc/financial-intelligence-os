from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.optimization.schemas import CapitalBudgetInputs, CapitalBudgetResponse
from engines.optimization.solver import optimize_capital_budget

router = APIRouter(prefix="/optimization", tags=["Optimization Engine"])

@router.post(
    "/capital-budget",
    response_model=CapitalBudgetResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize Capital Allocation Across Projects"
)
async def solve_capital_budget(
    inputs: CapitalBudgetInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> CapitalBudgetResponse:
    try:
        return optimize_capital_budget(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))