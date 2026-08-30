from fastapi import APIRouter, Depends, HTTPException, status
from core.tenancy.context import get_current_tenant_id
from engines.quantum.schemas import QuantumOptimizationRequest, QuantumBenchmarkResponse
from engines.quantum.simulator import quantum_lab

router = APIRouter(prefix="/quantum", tags=["Quantum Finance Laboratory"])

@router.post(
    "/benchmark",
    response_model=QuantumBenchmarkResponse,
    status_code=status.HTTP_200_OK,
    summary="Benchmark Quantum Optimization Against Classical Solvers"
)
async def benchmark_quantum_optimization(
    payload: QuantumOptimizationRequest,
    tenant_id: str = Depends(get_current_tenant_id)
) -> QuantumBenchmarkResponse:
    try:
        return quantum_lab.benchmark_portfolio_optimization(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))