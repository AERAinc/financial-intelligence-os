from pydantic import BaseModel, Field
from typing import Optional

class CVPInputs(BaseModel):
    unit_price: float = Field(..., gt=0, description="Selling price per unit")
    unit_variable_cost: float = Field(..., ge=0, description="Variable cost per unit")
    fixed_costs: float = Field(..., ge=0, description="Total fixed overhead costs")
    actual_units_sold: float = Field(..., ge=0, description="Current or projected sales units")
    interest_expense: float = Field(0.0, ge=0, description="Annual interest expense for leverage calculations")

class CVPResponse(BaseModel):
    unit_contribution_margin: float
    contribution_margin_ratio: float
    break_even_units: float
    break_even_revenue: float
    margin_of_safety_percentage: float
    degree_of_operating_leverage: Optional[float]
    degree_of_financial_leverage: Optional[float]
    degree_of_combined_leverage: Optional[float]