from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.econometrics.schemas import RegressionInputs, RegressionResponse, VaRInputs, VaRResponse
from engines.econometrics.analytics import run_linear_regression, calculate_var

router = APIRouter(prefix="/econometrics", tags=["Econometrics & Risk Engine"])

@router.post(
    "/regression",
    response_model=RegressionResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute OLS Linear Regression"
)
async def analyze_regression(
    inputs: RegressionInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> RegressionResponse:
    try:
        return run_linear_regression(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/value-at-risk",
    response_model=VaRResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate Parametric Value at Risk (VaR)"
)
async def analyze_var(
    inputs: VaRInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> VaRResponse:
    return calculate_var(inputs)