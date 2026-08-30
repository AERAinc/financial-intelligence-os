from pydantic import BaseModel
from typing import List, Optional

class LBOInputs(BaseModel):
    entry_ev: float              # Entry Enterprise Value
    entry_ebitda: float          # Entry EBITDA
    sponsor_equity_pct: float    # Fraction funded by sponsor equity (e.g., 0.40 for 40%)
    debt_interest_rate: float    # Annual interest rate on debt (e.g., 0.07 for 7%)
    holding_period_years: int    # Investment horizon in years (e.g., 5)
    projected_ebitda: List[float]# Projected EBITDA for each year of holding period
    exit_multiple: float         # Exit EV/EBITDA multiple

class LBOResponse(BaseModel):
    entry_multiple: float
    initial_debt: float
    initial_sponsor_equity: float
    exit_ev: float
    ending_debt: float
    sponsor_exit_proceeds: float
    moic: float                  # Multiple on Invested Capital
    irr: float                   # Internal Rate of Return (as a decimal)