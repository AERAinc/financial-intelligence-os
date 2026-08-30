from pydantic import BaseModel, Field
from typing import List, Optional

class DCFInputs(BaseModel):
    ebit: float = Field(..., description="Base year EBIT")
    tax_rate: float = Field(0.25, ge=0, le=1, description="Effective corporate tax rate")
    depreciation_amortization: float = Field(0.0, ge=0, description="D&A expense")
    capex: float = Field(0.0, ge=0, description="Capital expenditures")
    change_in_nwc: float = Field(0.0, description="Change in net working capital")
    
    growth_rate: float = Field(..., description="Annual revenue/EBIT growth rate during forecast period")
    forecast_years: int = Field(5, ge=1, le=10, description="Projection horizon in years")
    
    wacc: float = Field(..., gt=0, lt=1, description="Discount rate (WACC)")
    terminal_growth_rate: float = Field(..., ge=0, lt=1, description="Perpetual growth rate")
    
    total_debt: float = Field(0.0, ge=0, description="Total debt for Equity Value calculation")
    cash_and_equivalents: float = Field(0.0, ge=0, description="Cash & equivalents")

class DCFResponse(BaseModel):
    projected_fcff: List[float]
    pv_of_forecast_fcff: float
    terminal_value: float
    pv_of_terminal_value: float
    enterprise_value: float
    equity_value: float