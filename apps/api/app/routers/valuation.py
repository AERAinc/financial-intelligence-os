from fastapi import APIRouter, HTTPException
from engines.valuation.schemas import DCFInputs, DCFResponse
from engines.valuation.analytics import calculate_dcf

router = APIRouter(prefix="/api/v1/valuation", tags=["Valuation Engine"])

@router.post("/dcf", response_model=DCFResponse)
def run_dcf(inputs: DCFInputs):
    try:
        return calculate_dcf(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))