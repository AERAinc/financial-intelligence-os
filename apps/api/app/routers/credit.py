from fastapi import APIRouter, HTTPException
from engines.credit.schemas import CreditInputs, CreditResponse
from engines.credit.analytics import calculate_credit_risk

router = APIRouter(prefix="/api/v1/credit", tags=["Credit Intelligence Engine"])

@router.post("/calculate", response_model=CreditResponse)
def run_credit_risk(inputs: CreditInputs):
    try:
        return calculate_credit_risk(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))