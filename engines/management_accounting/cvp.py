import math
from typing import Optional
from engines.management_accounting.schemas import CVPInputs, CVPResponse

def safe_divide(numerator: float, denominator: float) -> Optional[float]:
    if denominator is None or denominator == 0 or math.isnan(denominator):
        return None
    return numerator / denominator

def calculate_cvp(inputs: CVPInputs) -> CVPResponse:
    unit_cm = inputs.unit_price - inputs.unit_variable_cost
    cm_ratio = safe_divide(unit_cm, inputs.unit_price) or 0.0
    
    break_even_units = safe_divide(inputs.fixed_costs, unit_cm) or 0.0
    break_even_revenue = break_even_units * inputs.unit_price
    
    total_revenue = inputs.actual_units_sold * inputs.unit_price
    total_cm = inputs.actual_units_sold * unit_cm
    ebit = total_cm - inputs.fixed_costs
    
    margin_of_safety = safe_divide(total_revenue - break_even_revenue, total_revenue) if total_revenue > 0 else 0.0
    
    dol = safe_divide(total_cm, ebit)
    dfl = safe_divide(ebit, ebit - inputs.interest_expense)
    dcl = (dol * dfl) if (dol is not None and dfl is not None) else None

    return CVPResponse(
        unit_contribution_margin=round(unit_cm, 4),
        contribution_margin_ratio=round(cm_ratio, 4),
        break_even_units=round(break_even_units, 2),
        break_even_revenue=round(break_even_revenue, 2),
        margin_of_safety_percentage=round(margin_of_safety, 4),
        degree_of_operating_leverage=round(dol, 4) if dol is not None else None,
        degree_of_financial_leverage=round(dfl, 4) if dfl is not None else None,
        degree_of_combined_leverage=round(dcl, 4) if dcl is not None else None,
    )