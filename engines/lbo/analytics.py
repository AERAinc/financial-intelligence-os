import numpy_financial as npf
from engines.lbo.schemas import LBOInputs, LBOResponse

def calculate_lbo(inputs: LBOInputs) -> LBOResponse:
    if len(inputs.projected_ebitda) != inputs.holding_period_years:
        raise ValueError("Length of projected_ebitda must equal holding_period_years.")

    # 1. Entry Valuation & Capital Structure
    entry_multiple = inputs.entry_ev / inputs.entry_ebitda if inputs.entry_ebitda > 0 else 0.0
    initial_sponsor_equity = inputs.entry_ev * inputs.sponsor_equity_pct
    initial_debt = inputs.entry_ev * (1.0 - inputs.sponsor_equity_pct)

    # 2. Simplified Debt Amortization Schedule
    # Assumes 50% of free cash flow (simplified here as EBITDA minus interest) goes toward debt paydown each year
    current_debt = initial_debt
    for ebitda in inputs.projected_ebitda:
        interest = current_debt * inputs.debt_interest_rate
        fcf_available = max(0.0, ebitda - interest)
        debt_repayment = min(current_debt, fcf_available * 0.5)
        current_debt -= debt_repayment

    ending_debt = current_debt

    # 3. Exit Valuation & Returns
    exit_ebitda = inputs.projected_ebitda[-1]
    exit_ev = exit_ebitda * inputs.exit_multiple
    sponsor_exit_proceeds = max(0.0, exit_ev - ending_debt)

    # 4. MOIC and IRR
    moic = sponsor_exit_proceeds / initial_sponsor_equity if initial_sponsor_equity > 0 else 0.0
    
    # Cash flow array: Initial outflow followed by zeros, then final exit inflow
    cash_flows = [-initial_sponsor_equity] + [0.0] * (inputs.holding_period_years - 1) + [sponsor_exit_proceeds]
    irr = float(npf.irr(cash_flows))

    return LBOResponse(
        entry_multiple=round(entry_multiple, 2),
        initial_debt=round(initial_debt, 2),
        initial_sponsor_equity=round(initial_sponsor_equity, 2),
        exit_ev=round(exit_ev, 2),
        ending_debt=round(ending_debt, 2),
        sponsor_exit_proceeds=round(sponsor_exit_proceeds, 2),
        moic=round(moic, 2),
        irr=round(irr, 4)
    )