from pydantic import BaseModel, Field
from typing import List, Optional

class CapitalProject(BaseModel):
    name: str
    cost: float = Field(..., gt=0, description="Initial investment cost")
    expected_npv: float = Field(..., description="Expected Net Present Value")

class CapitalBudgetInputs(BaseModel):
    total_budget: float = Field(..., gt=0, description="Total available capital")
    projects: List[CapitalProject]

class OptimizedProjectAllocation(BaseModel):
    name: str
    allocation_fraction: float
    allocated_cost: float
    expected_npv: float

class CapitalBudgetResponse(BaseModel):
    total_spent: float
    total_npv: float
    allocations: List[OptimizedProjectAllocation]