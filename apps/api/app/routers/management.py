from fastapi import APIRouter, Depends, status, HTTPException
from core.tenancy.context import get_current_tenant_id
from engines.management_accounting.schemas import CVPInputs, CVPResponse
from engines.management_accounting.cvp import calculate_cvp
import io
import pandas as pd
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/management", tags=["Management Accounting Engine"])

@router.post(
    "/cvp-analysis",
    response_model=CVPResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute Break-Even & Operational Leverage"
)
async def analyze_cvp(
    inputs: CVPInputs,
    tenant_id: str = Depends(get_current_tenant_id)
) -> CVPResponse:
    try:
        return calculate_cvp(inputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/download-cvp-report",
    summary="Export CVP & Management Accounting Report to Excel"
)
async def download_cvp_report(data: dict, tenant_id: str = Depends(get_current_tenant_id)):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        flat_data = [{"Metric Parameter": k, "Evaluated Value": v} for k, v in data.items()]
        df = pd.DataFrame(flat_data)
        df.to_excel(writer, sheet_name='CVP Summary', index=False)
        
    output.seek(0)
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="Management_CVP_Report.xlsx"'}
    )