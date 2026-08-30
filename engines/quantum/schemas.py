from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QuantumOptimizationRequest(BaseModel):
    experiment_id: str = Field(..., description="Unique identifier for the quantum experiment")
    expected_returns: List[float] = Field(..., description="Expected return vector for assets")
    covariance_matrix: List[List[float]] = Field(..., description="Asset covariance matrix")
    risk_tolerance_lambda: float = Field(default=0.5, description="Risk aversion parameter")
    budget_constraint: int = Field(default=3, description="Exact number of assets to select (combinatorial constraint)")

class QuantumBenchmarkResponse(BaseModel):
    experiment_id: str
    status: str
    classical_optimal_selection: List[int]
    classical_objective_value: float
    classical_runtime_seconds: float
    quantum_simulated_selection: List[int]
    quantum_objective_value: float
    quantum_runtime_seconds: float
    approximation_ratio: float
    message: str