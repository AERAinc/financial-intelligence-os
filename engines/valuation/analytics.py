from engines.valuation.schemas import DCFInputs, DCFResponse

def calculate_dcf(inputs: DCFInputs) -> DCFResponse:
    if inputs.wacc <= inputs.terminal_growth_rate:
        raise ValueError("WACC must be strictly greater than the terminal growth rate.")

    # 1. Calculate Present Value of projected Free Cash Flows
    pv_fcf = sum(
        fcf / ((1 + inputs.wacc) ** (t + 1))
        for t, fcf in enumerate(inputs.projected_fcf)
    )

    # 2. Calculate Terminal Value using Gordon Growth Model
    last_fcf = inputs.projected_fcf[-1]
    terminal_value = (last_fcf * (1 + inputs.terminal_growth_rate)) / (inputs.wacc - inputs.terminal_growth_rate)

    # 3. Discount Terminal Value back to present value
    num_years = len(inputs.projected_fcf)
    pv_terminal_value = terminal_value / ((1 + inputs.wacc) ** num_years)

    # 4. Derive Enterprise Value, Equity Value, and Implied Share Price
    enterprise_value = pv_fcf + pv_terminal_value
    equity_value = enterprise_value - inputs.net_debt
    share_price = equity_value / inputs.shares_outstanding if inputs.shares_outstanding > 0 else 0.0

    return DCFResponse(
        pv_free_cash_flows=round(pv_fcf, 2),
        terminal_value=round(terminal_value, 2),
        pv_terminal_value=round(pv_terminal_value, 2),
        enterprise_value=round(enterprise_value, 2),
        equity_value=round(equity_value, 2),
        implied_share_price=round(share_price, 2)
    )