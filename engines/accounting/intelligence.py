"""
Accounting Intelligence Engine
Computes core financial ratios, liquidity metrics, working capital cycles,
and profitability indicators with explicit formula versioning and audit traceability.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# Formula Version constant for traceability
ACCOUNTING_ENGINE_VERSION = "1.0.0"

class FinancialInputData(BaseModel):
    current_assets: float = Field(..., description="Total Current Assets")
    current_liabilities: float = Field(..., description="Total Current Liabilities")
    inventory: float = Field(..., description="Total Inventory")
    revenue: float = Field(..., description="Total Net Revenue")
    gross_profit: float = Field(..., description="Gross Profit")
    ebitda: float = Field(..., description="Earnings Before Interest, Taxes, Depreciation, and Amortization")
    ebit: float = Field(..., description="Earnings Before Interest and Taxes")
    net_income: float = Field(..., description="Net Income")
    average_equity: float = Field(..., description="Average Shareholders Equity")
    capital_employed: float = Field(..., description="Total Capital Employed")
    average_accounts_receivable: float = Field(..., description="Average Accounts Receivable")
    credit_sales: float = Field(..., description="Total Credit Sales / Revenue")
    average_inventory: float = Field(..., description="Average Inventory balance")
    cogs: float = Field(..., description="Cost of Goods Sold")
    average_accounts_payable: float = Field(..., description="Average Accounts Payable")
    credit_purchases: float = Field(..., description="Total Credit Purchases / COGS")
    total_debt: float = Field(..., description="Total Debt Obligations")
    interest_expense: float = Field(..., description="Total Interest Expense")
    debt_service: float = Field(..., description="Total Principal Repayments + Interest Expense")

class AccountingIntelligenceEngine:
    @staticmethod
    def compute_liquidity(data: FinancialInputData) -> Dict[str, Any]:
        """Calculates Current Ratio and Quick Ratio."""
        if data.current_liabilities == 0:
            raise ValueError("Current Liabilities cannot be zero (Division by zero risk).")
        
        current_ratio = data.current_assets / data.current_liabilities
        quick_ratio = (data.current_assets - data.inventory) / data.current_liabilities
        
        return {
            "formula_version": ACCOUNTING_ENGINE_VERSION,
            "metrics": {
                "current_ratio": round(current_ratio, 4),
                "quick_ratio": round(quick_ratio, 4)
            },
            "inputs_used": {
                "current_assets": data.current_assets,
                "current_liabilities": data.current_liabilities,
                "inventory": data.inventory
            }
        }

    @staticmethod
    def compute_profitability(data: FinancialInputData) -> Dict[str, Any]:
        """Calculates Gross Margin, EBITDA Margin, ROE, and ROCE."""
        if data.revenue == 0:
            raise ValueError("Revenue cannot be zero.")
        if data.average_equity == 0:
            raise ValueError("Average Equity cannot be zero.")
        if data.capital_employed == 0:
            raise ValueError("Capital Employed cannot be zero.")

        gross_margin = data.gross_profit / data.revenue
        ebitda_margin = data.ebitda / data.revenue
        roe = data.net_income / data.average_equity
        roce = data.ebit / data.capital_employed

        return {
            "formula_version": ACCOUNTING_ENGINE_VERSION,
            "metrics": {
                "gross_margin": round(gross_margin, 4),
                "ebitda_margin": round(ebitda_margin, 4),
                "roe": round(roe, 4),
                "roce": round(roce, 4)
            }
        }

    @staticmethod
    def compute_working_capital(data: FinancialInputData) -> Dict[str, Any]:
        """Calculates DSO, DIO, DPO, and Cash Conversion Cycle (CCC)."""
        dso = (data.average_accounts_receivable / data.credit_sales) * 365 if data.credit_sales > 0 else 0.0
        dio = (data.average_inventory / data.cogs) * 365 if data.cogs > 0 else 0.0
        dpo = (data.average_accounts_payable / data.credit_purchases) * 365 if data.credit_purchases > 0 else 0.0
        ccc = dso + dio - dpo

        return {
            "formula_version": ACCOUNTING_ENGINE_VERSION,
            "metrics": {
                "dso_days": round(dso, 2),
                "dio_days": round(dio, 2),
                "dpo_days": round(dpo, 2),
                "cash_conversion_cycle_days": round(ccc, 2)
            }
        }

    @staticmethod
    def compute_leverage(data: FinancialInputData) -> Dict[str, Any]:
        """Calculates Debt-to-Equity, Interest Coverage Ratio, and DSCR."""
        if data.average_equity == 0:
            raise ValueError("Average Equity cannot be zero.")
        if data.interest_expense == 0:
            raise ValueError("Interest Expense cannot be zero.")
        if data.debt_service == 0:
            raise ValueError("Debt Service cannot be zero.")

        debt_to_equity = data.total_debt / data.average_equity
        debt_to_ebitda = data.total_debt / data.ebitda if data.ebitda > 0 else 0.0
        interest_coverage = data.ebit / data.interest_expense
        dscr = data.ebitda / data.debt_service # Simplified proxy estimation

        return {
            "formula_version": ACCOUNTING_ENGINE_VERSION,
            "metrics": {
                "debt_to_equity": round(debt_to_equity, 4),
                "debt_to_ebitda": round(debt_to_ebitda, 4),
                "interest_coverage_ratio": round(interest_coverage, 4),
                "dscr": round(dscr, 4)
            }
        }

    @classmethod
    def execute_full_audit(cls, data: FinancialInputData) -> Dict[str, Any]:
        """Executes complete accounting intelligence analysis suite."""
        return {
            "engine": "AccountingIntelligenceEngine",
            "version": ACCOUNTING_ENGINE_VERSION,
            "liquidity": cls.compute_liquidity(data),
            "profitability": cls.compute_profitability(data),
            "working_capital": cls.compute_working_capital(data),
            "leverage": cls.compute_leverage(data)
        }

# Example Execution block for testing / verification
if __name__ == "__main__":
    sample_financials = FinancialInputData(
        current_assets=500000.0,
        current_liabilities=300000.0,
        inventory=120000.0,
        revenue=1200000.0,
        gross_profit=480000.0,
        ebitda=250000.0,
        ebit=180000.0,
        net_income=120000.0,
        average_equity=600000.0,
        capital_employed=900000.0,
        average_accounts_receivable=100000.0,
        credit_sales=1200000.0,
        average_inventory=120000.0,
        cogs=720000.0,
        average_accounts_payable=80000.0,
        credit_purchases=720000.0,
        total_debt=350000.0,
        interest_expense=30000.0,
        debt_service=70000.0
    )
    
    results = AccountingIntelligenceEngine.execute_full_audit(sample_financials)
    import json
    print(json.dumps(results, indent=2))