from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProductLeg(BaseModel):
    leg_id: str
    leg_type: str = Field(..., description="e.g., 'fixed_coupon', 'floating_rate', 'equity_barrier'")
    notional: float = Field(..., gt=0)
    rate_or_spread: float = Field(..., description="Annual rate or spread percentage")
    payment_frequency_months: int = Field(default=6)

class StructuredProductDefinition(BaseModel):
    product_id: str
    product_name: str
    underlying_asset: str = Field(..., description="e.g., 'S&P 500', 'SOFR', 'UST 10Y'")
    tenor_years: float = Field(..., gt=0)
    legs: List[ProductLeg]
    barriers: Optional[Dict[str, float]] = Field(default=None, description="Knock-in or knock-out barrier levels")

class ProductSimulationRequest(BaseModel):
    product_definition: StructuredProductDefinition
    initial_asset_price: float = Field(..., gt=0)
    volatility: float = Field(..., gt=0, description="Annualized volatility assumption")
    risk_free_rate: float = Field(..., description="Risk-free rate for discounting")
    monte_carlo_paths: int = Field(default=1000, description="Number of simulation paths")

class ProductSimulationResponse(BaseModel):
    product_id: str
    status: str
    expected_present_value: float
    value_at_risk_95: float
    probability_of_knock_in: Optional[float] = None
    message: str