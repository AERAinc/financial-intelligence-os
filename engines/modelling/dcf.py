import math
from typing import Optional
from engines.modelling.schemas import DCFInputs, DCFResponse

def calculate_dcf(inputs: DCFInputs) -> DCFResponse:
    if inputs.wacc <= inputs.terminal_growth_rate:
        raise ValueError("WACC must be strictly greater than terminal growth rate.")

    base_fcff = (
        inputs.ebit * (1 - inputs.tax_rate)
        + inputs.depreciation_amortization
        - inputs.capex
        - inputs.change_in_nwc
    )

    projected_fcff = []
    pv_forecast_fcff = 0.0

    # Forecast Period Cash Flows
    for year in range(1, inputs.forecast_years + 1):
        fcff_t = base_fcff * ((1 + inputs.growth_rate) ** year)
        projected_fcff.append(round(fcff_t, 2))
        
        discount_factor = (1 + inputs.wacc) ** year
        pv_forecast_fcff += fcff_t / discount_factor

    # Terminal Value Calculation
    final_year_fcff = projected_fcff[-1]
    terminal_value = (final_year_fcff * (1 + inputs.terminal_growth_rate)) / (inputs.wacc - inputs.terminal_growth_rate)
    pv_terminal_value = terminal_value / ((1 + inputs.wacc) ** inputs.forecast_years)

    # Enterprise & Equity Value
    enterprise_value = pv_forecast_fcff + pv_terminal_value
    equity_value = enterprise_value - inputs.total_debt + inputs.cash_and_equivalents

    return DCFResponse(
        projected_fcff=projected_fcff,
        pv_of_forecast_fcff=round(pv_forecast_fcff, 2),
        terminal_value=round(terminal_value, 2),
        pv_of_terminal_value=round(pv_terminal_value, 2),
        enterprise_value=round(enterprise_value, 2),
        equity_value=round(equity_value, 2)
    )