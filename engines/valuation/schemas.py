from pydantic import BaseModel
from typing import List

class DCFInputs(BaseModel):
    projected_fcf: List[float]  # Projected Free Cash Flows for N years
    wacc: float                 # Weighted Average Cost of Capital (e.g., 0.10 for 10%)
    terminal_growth_rate: float # Perpetual growth rate (e.g., 0.025 for 2.5%)
    net_debt: float             # Total Debt minus Cash
    shares_outstanding: float   # Total shares to compute per-share value

class DCFResponse(BaseModel):
    pv_free_cash_flows: float
    terminal_value: float
    pv_terminal_value: float
    enterprise_value: float
    equity_value: float
    implied_share_price: float