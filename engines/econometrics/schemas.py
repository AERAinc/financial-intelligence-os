from pydantic import BaseModel, Field
from typing import List, Optional

class RegressionInputs(BaseModel):
    dependent_var: List[float] = Field(..., min_items=3, description="Y values (e.g., Sales)")
    independent_var: List[float] = Field(..., min_items=3, description="X values (e.g., Marketing Spend)")

class RegressionResponse(BaseModel):
    slope: float
    intercept: float
    r_squared: float
    std_err: float

class VaRInputs(BaseModel):
    portfolio_value: float = Field(..., gt=0, description="Total portfolio value")
    mean_return: float = Field(0.0, description="Expected daily return (decimal)")
    std_dev: float = Field(..., gt=0, description="Daily volatility/std dev (decimal)")
    confidence_level: float = Field(0.95, ge=0.80, le=0.999, description="Confidence level (e.g. 0.95 or 0.99)")
    time_horizon_days: int = Field(1, ge=1, description="Holding period in days")

class VaRResponse(BaseModel):
    value_at_risk: float
    confidence_level: float
    horizon_days: int