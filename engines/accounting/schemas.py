from pydantic import BaseModel, Field
from typing import Optional

class FinancialInputs(BaseModel):
    current_assets: float = Field(..., description="Total Current Assets")
    current_liabilities: float = Field(..., description="Total Current Liabilities")
    inventory: float = Field(0.0, description="Total Inventory")
    total_debt: float = Field(0.0, description="Total Short & Long Term Debt")
    total_equity: float = Field(..., description="Total Shareholders Equity")
    cash_and_equivalents: float = Field(0.0, description="Cash & Equivalents")
    
    revenue: float = Field(..., description="Total Revenue")
    credit_sales: Optional[float] = Field(None, description="Credit Sales (defaults to Revenue)")
    cogs: float = Field(..., description="Cost of Goods Sold")
    credit_purchases: Optional[float] = Field(None, description="Credit Purchases (defaults to COGS)")
    gross_profit: float = Field(..., description="Gross Profit")
    ebitda: float = Field(..., description="EBITDA")
    ebit: float = Field(..., description="EBIT / Operating Income")
    net_income: float = Field(..., description="Net Income")
    interest_expense: float = Field(0.0, description="Annual Interest Expense")
    
    avg_accounts_receivable: float = Field(0.0, description="Average Accounts Receivable")
    avg_inventory: float = Field(0.0, description="Average Inventory")
    avg_accounts_payable: float = Field(0.0, description="Average Accounts Payable")

class AccountingRatiosResponse(BaseModel):
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    gross_margin: Optional[float]
    ebitda_margin: Optional[float]
    roe: Optional[float]
    roce: Optional[float]
    dso: Optional[float]
    dio: Optional[float]
    dpo: Optional[float]
    ccc: Optional[float]
    debt_to_equity: Optional[float]
    net_debt_to_ebitda: Optional[float]
    interest_coverage: Optional[float]