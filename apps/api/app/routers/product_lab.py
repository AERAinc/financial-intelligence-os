from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.product_lab.schemas import ProductSimulationRequest, ProductSimulationResponse
from engines.product_lab.simulator import product_simulator

router = APIRouter(prefix="/product-lab", tags=["Financial Product Research Laboratory"])

@router.post(
    "/simulate",
    response_model=ProductSimulationResponse,
    status_code=status.HTTP_200_OK,
    summary="Simulate and Price a Structured Financial Product"
)
async def simulate_product(
    payload: ProductSimulationRequest,
    tenant_id: str = Depends(get_current_tenant_id)
) -> ProductSimulationResponse:
    try:
        return product_simulator.simulate_structured_product(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))