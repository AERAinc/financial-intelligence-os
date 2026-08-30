from fastapi import APIRouter, HTTPException
from engines.lbo.schemas import LBOInputs, LBOResponse
from engines.lbo.analytics import calculate_lbo

router = APIRouter(prefix="/api/v1/lbo", tags=["LBO Engine"])

@router.post("/calculate", response_model=LBOResponse)
def run_lbo(inputs: LBOInputs):
    try:
        return calculate_lbo(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))