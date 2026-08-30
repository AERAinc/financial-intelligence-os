import math
from typing import Optional
from engines.accounting.schemas import FinancialInputs, AccountingRatiosResponse

def safe_divide(numerator: float, denominator: float) -> Optional[float]:
    if denominator is None or denominator == 0 or math.isnan(denominator):
        return None
    return numerator / denominator

def calculate_accounting_ratios(inputs: FinancialInputs) -> AccountingRatiosResponse:
    current_ratio = safe_divide(inputs.current_assets, inputs.current_liabilities)
    quick_ratio = safe_divide(inputs.current_assets - inputs.inventory, inputs.current_liabilities)
    
    gross_margin = safe_divide(inputs.gross_profit, inputs.revenue)
    ebitda_margin = safe_divide(inputs.ebitda, inputs.revenue)
    roe = safe_divide(inputs.net_income, inputs.total_equity)
    roce = safe_divide(inputs.ebit, inputs.total_equity + inputs.total_debt)
    
    eff_sales = inputs.credit_sales if inputs.credit_sales is not None else inputs.revenue
    eff_purchases = inputs.credit_purchases if inputs.credit_purchases is not None else inputs.cogs
    
    dso = safe_divide(inputs.avg_accounts_receivable * 365.0, eff_sales)
    dio = safe_divide(inputs.avg_inventory * 365.0, inputs.cogs)
    dpo = safe_divide(inputs.avg_accounts_payable * 365.0, eff_purchases)
    
    ccc = (dso + dio - dpo) if (dso is not None and dio is not None and dpo is not None) else None
    
    debt_to_equity = safe_divide(inputs.total_debt, inputs.total_equity)
    net_debt_to_ebitda = safe_divide(inputs.total_debt - inputs.cash_and_equivalents, inputs.ebitda)
    interest_coverage = safe_divide(inputs.ebit, inputs.interest_expense)
    
    return AccountingRatiosResponse(
        current_ratio=round(current_ratio, 4) if current_ratio is not None else None,
        quick_ratio=round(quick_ratio, 4) if quick_ratio is not None else None,
        gross_margin=round(gross_margin, 4) if gross_margin is not None else None,
        ebitda_margin=round(ebitda_margin, 4) if ebitda_margin is not None else None,
        roe=round(roe, 4) if roe is not None else None,
        roce=round(roce, 4) if roce is not None else None,
        dso=round(dso, 2) if dso is not None else None,
        dio=round(dio, 2) if dio is not None else None,
        dpo=round(dpo, 2) if dpo is not None else None,
        ccc=round(ccc, 2) if ccc is not None else None,
        debt_to_equity=round(debt_to_equity, 4) if debt_to_equity is not None else None,
        net_debt_to_ebitda=round(net_debt_to_ebitda, 4) if net_debt_to_ebitda is not None else None,
        interest_coverage=round(interest_coverage, 4) if interest_coverage is not None else None,
    )