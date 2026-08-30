from pydantic import BaseModel, Field
from typing import Optional

class FinancialInputSchema(BaseModel):
    revenue: float = Field(..., description="Total revenue or net sales")
    gross_profit: float = Field(..., description="Gross profit")
    ebitda: float = Field(..., description="EBITDA")
    ebit: float = Field(..., description="EBIT (Operating Income)")
    net_income: float = Field(..., description="Net income after taxes")
    current_assets: float = Field(..., description="Total current assets")
    current_liabilities: float = Field(..., description="Total current liabilities")
    inventory: float = Field(..., description="Total inventory")
    accounts_receivable: float = Field(..., description="Average accounts receivable")
    accounts_payable: float = Field(..., description="Average accounts payable")
    cost_of_goods_sold: float = Field(..., description="COGS")
    credit_sales: Optional[float] = Field(None, description="Credit sales (defaults to revenue if None)")
    credit_purchases: Optional[float] = Field(None, description="Credit purchases (defaults to COGS if None)")
    total_debt: float = Field(..., description="Total debt")
    total_equity: float = Field(..., description="Total shareholders' equity")
    capital_employed: float = Field(..., description="Total capital employed")
    interest_expense: float = Field(..., description="Total interest expense")
    annual_debt_service: float = Field(..., description="Principal repayments + interest")