import numpy as np
from scipy.optimize import linprog
from engines.optimization.schemas import CapitalBudgetInputs, CapitalBudgetResponse, OptimizedProjectAllocation

def optimize_capital_budget(inputs: CapitalBudgetInputs) -> CapitalBudgetResponse:
    num_projects = len(inputs.projects)
    if num_projects == 0:
        return CapitalBudgetResponse(total_spent=0.0, total_npv=0.0, allocations=[])

    # linprog minimizes c^T * x, so we negate NPV to maximize
    c = [-p.expected_npv for p in inputs.projects]
    
    # Budget constraint: sum(cost_i * x_i) <= total_budget
    A_ub = [[p.cost for p in inputs.projects]]
    b_ub = [inputs.total_budget]
    
    # Bounds for each project fraction: 0 <= x_i <= 1
    bounds = [(0, 1) for _ in range(num_projects)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if not res.success:
        raise ValueError("Optimization failed to find a valid solution.")

    allocations = []
    total_spent = 0.0
    total_npv = 0.0

    for i, p in enumerate(inputs.projects):
        frac = float(res.x[i])
        allocated_cost = frac * p.cost
        project_npv = frac * p.expected_npv
        
        total_spent += allocated_cost
        total_npv += project_npv

        allocations.append(OptimizedProjectAllocation(
            name=p.name,
            allocation_fraction=round(frac, 4),
            allocated_cost=round(allocated_cost, 2),
            expected_npv=round(project_npv, 2)
        ))

    return CapitalBudgetResponse(
        total_spent=round(total_spent, 2),
        total_npv=round(total_npv, 2),
        allocations=allocations
    )