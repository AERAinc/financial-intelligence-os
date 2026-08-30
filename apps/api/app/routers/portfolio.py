from fastapi import APIRouter, HTTPException
from engines.portfolio.schemas import PortfolioOptimizationInputs, PortfolioOptimizationResponse
from engines.portfolio.analytics import calculate_portfolio_optimization

router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio Optimization Engine"])

@router.post("/optimize", response_model=PortfolioOptimizationResponse)
def run_portfolio_optimization(inputs: PortfolioOptimizationInputs):
    try:
        return calculate_portfolio_optimization(inputs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))