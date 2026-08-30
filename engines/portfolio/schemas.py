from pydantic import BaseModel, Field
from typing import List

class PortfolioOptimizationInputs(BaseModel):
    expected_returns: List[float] = Field(..., description="Expected return for each asset")
    covariance_matrix: List[List[float]] = Field(..., description="Covariance matrix of asset returns")
    risk_free_rate: float = Field(0.02, description="Risk-free rate for Sharpe ratio calculation")

class PortfolioOptimizationResponse(BaseModel):
    optimal_weights: List[float] = Field(..., description="Optimal asset allocation weights summing to 1.0")
    portfolio_return: float = Field(..., description="Expected annual portfolio return")
    portfolio_volatility: float = Field(..., description="Portfolio standard deviation (risk)")
    sharpe_ratio: float = Field(..., description="Sharpe ratio of the optimized portfolio")