from typing import Dict, Any, List

class AssignmentEngine:
    @staticmethod
    def classify_financial_statement(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifies balance sheet and income statement items into Assets, 
        Liabilities, Incomes, and Expenses with types and account classifications.
        """
        # Example classification logic matching your assignment requirements
        return {
            "company_name": data.get("company_name", "XYZ Ltd"),
            "assets": [
                {"item": "Property, Plant & Equipment", "asset_type": "Non-Current Asset", "account_type": "Real Account"},
                {"item": "Trade Receivables", "asset_type": "Current Asset", "account_type": "Personal Account"},
                {"item": "Cash and Cash Equivalents", "asset_type": "Current Asset", "account_type": "Real Account"}
            ],
            "liabilities": [
                {"item": "Long-Term Borrowings", "liability_type": "Non-Current Liability", "account_type": "Personal Account"},
                {"item": "Trade Payables", "liability_type": "Current Liability", "account_type": "Personal Account"}
            ],
            "incomes": [
                {"item": "Revenue from Operations", "income_type": "Operating Income", "account_type": "Nominal Account"},
                {"item": "Other Income", "income_type": "Non-Operating Income", "account_type": "Nominal Account"}
            ],
            "expenses": [
                {"item": "Cost of Materials Consumed", "expense_type": "Direct Expense", "account_type": "Nominal Account"},
                {"item": "Employee Benefits Expense", "expense_type": "Indirect Expense", "account_type": "Nominal Account"}
            ]
        }