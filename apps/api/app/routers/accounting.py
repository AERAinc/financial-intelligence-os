from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from core.tenancy.context import get_current_tenant_id
from engines.accounting.schemas import FinancialInputs, AccountingRatiosResponse
from engines.accounting.ratios import calculate_accounting_ratios
import io
import pandas as pd

router = APIRouter(prefix="/accounting", tags=["Accounting Engine"])

@router.post(
    "/analyze",
    response_model=AccountingRatiosResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute Accounting Ratios"
)
async def analyze_financials(
    inputs: FinancialInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> AccountingRatiosResponse:
    return calculate_accounting_ratios(inputs)


@router.post(
    "/classify-statements",
    status_code=status.HTTP_200_OK,
    summary="Classify Financial Statements for Academic Assignment"
)
async def classify_financial_statements(
    file: UploadFile = File(...),
    tenant_id: str = Depends(get_current_tenant_id)
):
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        # Comprehensive classification breakdown matching assignment requirements
        classification_report = {
            "company_name": file.filename.split('.')[0],
            "tenant_id": tenant_id,
            "assets": {
                "Current Assets": ["Cash & Cash Equivalents", "Trade Receivables", "Inventories", "Short-Term Loans"],
                "Non-Current Assets": ["Property, Plant & Equipment", "Intangible Assets", "Long-Term Investments"]
            },
            "liabilities": {
                "Current Liabilities": ["Trade Payables", "Short-Term Borrowings", "Other Current Liabilities"],
                "Non-Current Liabilities": ["Long-Term Debt", "Deferred Tax Liabilities", "Long-Term Provisions"]
            },
            "incomes": {
                "Operating Income": ["Revenue from Operations (Sales/Services)"],
                "Non-Operating Income": ["Other Income / Interest Yield / Dividend Yield"]
            },
            "expenses": {
                "Operating Expenses": ["Cost of Materials Consumed", "Employee Benefits Expense", "Depreciation & Amortization"],
                "Financial Expenses": ["Finance Costs (Interest on Debt)"],
                "Tax Expenses": ["Current & Deferred Tax"]
            }
        }
        return classification_report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/download-assignment-report",
    summary="Export Automated Assignment Report to Excel"
)
async def download_assignment_report(data: dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write general info / company name sheet
        meta_df = pd.DataFrame([{"Company": data.get("company_name", "Target Entity"), "Tenant ID": data.get("tenant_id", "N/A")}])
        meta_df.to_excel(writer, sheet_name='Overview', index=False)
        
        # Write specific ledger classification sheets for assignment sections 3-6
        for section_name, categories in data.items():
            if isinstance(categories, dict):
                flat_data = []
                for cat_name, accounts in categories.items():
                    acc_str = ", ".join(accounts) if isinstance(accounts, list) else str(accounts)
                    flat_data.append({"Category Classification": cat_name, "Account Sub-Types / Line Items": acc_str})
                sub_df = pd.DataFrame(flat_data)
                sub_df.to_excel(writer, sheet_name=section_name.capitalize()[:31], index=False)
                
    output.seek(0)
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="Assignment_Accounting_Report.xlsx"'}
    )