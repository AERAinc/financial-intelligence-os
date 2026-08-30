from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.modelling.schemas import DCFInputs, DCFResponse
from engines.modelling.dcf import calculate_dcf

router = APIRouter(prefix="/modelling", tags=["Valuation Engine"])

@router.post(
    "/dcf-valuation",
    response_model=DCFResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute Intrinsic DCF Valuation"
)
async def analyze_dcf(
    inputs: DCFInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> DCFResponse:
    try:
        return calculate_dcf(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))