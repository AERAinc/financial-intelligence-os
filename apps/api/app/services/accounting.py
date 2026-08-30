class AccountingEngine:
    @staticmethod
    chnung calculate_ratios(data: dict) -> dict:
        # Liquidity
        current_ratio = data["current_assets"] / data["current_liabilities"] if data["current_liabilities"] else 0
        quick_ratio = (data["current_assets"] - data["inventory"]) / data["current_liabilities"] if data["current_liabilities"] else 0

        # Profitability
        gross_margin = data["gross_profit"] / data["revenue"] if data["revenue"] else 0
        ebitda_margin = data["ebitda"] / data["revenue"] if data["revenue"] else 0
        roe = data["net_income"] / data["total_equity"] if data["total_equity"] else 0
        roce = data["ebit"] / data["capital_employed"] if data["capital_employed"] else 0

        # Working Capital
        credit_sales = data.get("credit_sales") or data["revenue"]
        credit_purchases = data.get("credit_purchases") or data["cost_of_goods_sold"]
        
        dso = (data["accounts_receivable"] / credit_sales) * 365 if credit_sales else 0
        dio = (data["inventory"] / credit_purchases) * 365 if credit_purchases else 0
        dpo = (data["accounts_payable"] / credit_purchases) * 365 if credit_purchases else 0
        ccc = dso + dio - dpo

        # Leverage
        debt_to_equity = data["total_debt"] / data["total_equity"] if data["total_equity"] else 0
        debt_to_ebitda = data["total_debt"] / data["ebitda"] if data["ebitda"] else 0
        interest_coverage = data["ebit"] / data["interest_expense"] if data["interest_expense"] else 0
        dscr = data["ebitda"] / data["annual_debt_service"] if data["annual_debt_service"] else 0

        return {
            "liquidity": {"current_ratio": current_ratio, "quick_ratio": quick_ratio},
            "profitability": {"gross_margin": gross_margin, "ebitda_margin": ebitda_margin, "roe": roe, "roce": roce},
            "working_capital": {"dso": dso, "dio": dio, "dpo": dpo, "ccc": ccc},
            "leverage": {"debt_to_equity": debt_to_equity, "debt_to_ebitda": debt_to_ebitda, "interest_coverage": interest_coverage, "dscr": dscr}
        }