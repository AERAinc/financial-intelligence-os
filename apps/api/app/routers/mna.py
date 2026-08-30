from fastapi import APIRouter, HTTPException
from engines.mna.schemas import MNAInputs, MNAResponse
from engines.mna.analytics import calculate_mna

router = APIRouter(prefix="/api/v1/mna", tags=["M&A Engine"])

@router.post("/calculate", response_model=MNAResponse)
def run_mna(inputs: MNAInputs):
    try:
        return calculate_mna(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))