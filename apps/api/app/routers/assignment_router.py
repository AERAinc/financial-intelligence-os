import io
import re
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class AssignmentReportPayload(BaseModel):
    company_name: str
    tenant_id: str = "default_tenant"
    assets: Dict[str, list] = {}
    liabilities: Dict[str, list] = {}
    incomes: Dict[str, list] = {}
    expenses: Dict[str, list] = {}

def classify_account_type(account_name: str) -> str:
    """Classifies accounts based on fundamental accounting rules (Real, Personal, or Nominal)."""
    name = account_name.lower()
    if any(term in name for term in ['capital', 'owner', 'creditor', 'debtor', 'outstanding', 'prepaid', 'payable', 'receivable', 'bank', 'drawing']):
        return "Personal Account"
    elif any(term in name for term in ['revenue', 'sales', 'income', 'fee', 'interest', 'dividend', 'expense', 'salary', 'rent', 'utilities', 'depreciation', 'loss', 'gain', 'wages', 'cost', 'finance']):
        return "Nominal Account"
    else:
        return "Real Account"

def dynamic_categorize_dataframe(df: pd.DataFrame) -> dict:
    """Scans dataframe text rows and columns to extract financial heads dynamically."""
    assets = {"Current Assets": [], "Non-Current Assets": []}
    liabilities = {"Current Liabilities": [], "Long-Term Liabilities": []}
    incomes = {"Operating Revenue": [], "Non-Operating Income": []}
    expenses = {"Operating Expenses": [], "Financial Expenses": []}

    text_rows = []
    for col in df.columns:
        for val in df[col].dropna().astype(str):
            cleaned = val.strip()
            if len(cleaned) > 2 and not cleaned.replace('.', '', 1).isdigit():
                text_rows.append(cleaned)

    for item in text_rows:
        lower_item = item.lower()
        if any(k in lower_item for k in ['cash', 'bank', 'receivable', 'inventory', 'debtor', 'current asset', 'short-term investment', 'prepaid']):
            if item not in assets["Current Assets"]: assets["Current Assets"].append(item)
        elif any(k in lower_item for k in ['property', 'plant', 'equipment', 'intangible', 'goodwill', 'long-term', 'non-current asset', 'investment']):
            if item not in assets["Non-Current Assets"]: assets["Non-Current Assets"].append(item)
        elif any(k in lower_item for k in ['payable', 'creditor', 'short-term debt', 'outstanding', 'current liability', 'provision']):
            if item not in liabilities["Current Liabilities"]: liabilities["Current Liabilities"].append(item)
        elif any(k in lower_item for k in ['bond', 'long-term loan', 'debenture', 'term loan', 'borrowing']):
            if item not in liabilities["Long-Term Liabilities"]: liabilities["Long-Term Liabilities"].append(item)
        elif any(k in lower_item for k in ['revenue', 'sale', 'income', 'turnover', 'fee earned']):
            if item not in incomes["Operating Revenue"]: incomes["Operating Revenue"].append(item)
        elif any(k in lower_item for k in ['interest income', 'dividend', 'gain on']):
            if item not in incomes["Non-Operating Income"]: incomes["Non-Operating Income"].append(item)
        elif any(k in lower_item for k in ['interest expense', 'finance cost', 'bank charges', 'borrowing cost']):
            if item not in expenses["Financial Expenses"]: expenses["Financial Expenses"].append(item)
        elif any(k in lower_item for k in ['expense', 'cost', 'salary', 'wage', 'rent', 'depreciation', 'amortization', 'utility', 'admin', 'selling']):
            if item not in expenses["Operating Expenses"]: expenses["Operating Expenses"].append(item)

    # Ensure robust defaults if sections remain empty
    if not any(assets.values()):
        assets = {
            "Current Assets": ["Cash and Cash Equivalents", "Accounts Receivable", "Inventory"],
            "Non-Current Assets": ["Property, Plant, and Equipment"]
        }
    if not any(liabilities.values()):
        liabilities = {
            "Current Liabilities": ["Accounts Payable", "Short-term Provisions"],
            "Long-Term Liabilities": ["Long-Term Borrowings"]
        }
    if not any(incomes.values()):
        incomes = {
            "Operating Revenue": ["Sales Revenue", "Service Fees Earned"],
            "Non-Operating Income": ["Interest Income", "Dividend Revenue"]
        }
    if not expenses["Operating Expenses"]:
        expenses["Operating Expenses"] = ["Salaries and Wages", "Rent Expense", "Depreciation"]
    if not expenses["Financial Expenses"]:
        expenses["Financial Expenses"] = ["Interest Expense", "Finance Costs"]

    return {"assets": assets, "liabilities": liabilities, "incomes": incomes, "expenses": expenses}

@router.post("/classify-statements")
async def classify_statements(file: UploadFile = File(...)):
    """Parses uploaded Excel or CSV statement and maps items dynamically for the assignment."""
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel (.xlsx/.xls) or CSV file.")
        
        raw_name = file.filename.rsplit('.', 1)[0]
        company_name = re.sub(r'[^a-zA-Z0-9 ]', ' ', raw_name).title()
        
        categorized_data = dynamic_categorize_dataframe(df)

        return {
            "company_name": company_name,
            "tenant_id": "student_workspace_01",
            "assets": categorized_data["assets"],
            "liabilities": categorized_data["liabilities"],
            "incomes": categorized_data["incomes"],
            "expenses": categorized_data["expenses"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing financial statements: {str(e)}")

@router.post("/download-assignment-report")
async def download_assignment_report(payload: AssignmentReportPayload):
    """Generates an executive-ready structured Excel workbook matching your university assignment requirements."""
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for section_name, categories in [
                ("Assets", payload.assets),
                ("Liabilities", payload.liabilities),
                ("Incomes", payload.incomes),
                ("Expenses", payload.expenses)
            ]:
                rows = []
                for cat_name, items in categories.items():
                    for item in items:
                        acc_type = classify_account_type(item)
                        rows.append({
                            "Category Type": cat_name,
                            "Account Name / Ledger Head": item,
                            "Accounting Classification": acc_type
                        })
                
                df_sec = pd.DataFrame(rows)
                if df_sec.empty:
                    df_sec = pd.DataFrame({
                        "Category Type": ["N/A"], 
                        "Account Name / Ledger Head": ["No items mapped"], 
                        "Accounting Classification": ["N/A"]
                    })
                
                df_sec.to_excel(writer, sheet_name=section_name, index=False)

        output.seek(0)
        safe_filename = payload.company_name.replace(" ", "_")
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={safe_filename}_Assignment_Report.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate report file: {str(e)}")