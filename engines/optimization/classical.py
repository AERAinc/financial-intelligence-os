from typing import List, Dict, Any
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

class ClassicalOptimizationEngine:
    """Engine for solving mixed-integer linear programming and capital allocation problems."""

    @staticmethod
    def optimize_capital_budget(
        project_returns: List[float], 
        cost_matrix: List[List[float]], 
        resource_limits: List[float]
    ) -> Dict[str, Any]:
        """
        Optimizes project selection subject to resource/budget constraints.
        
        Args:
            project_returns: Objective coefficients (e.g., NPV for each project).
            cost_matrix: 2D list where each row represents a resource constraint and columns represent projects.
            resource_limits: Upper bounds for each resource constraint.
        """
        c = -np.array(project_returns, dtype=np.float64)  # Minimize negative NPV (i.e., maximize NPV)
        A = np.array(cost_matrix, dtype=np.float64)
        b_upper = np.array(resource_limits, dtype=np.float64)
        
        # Constraints: A * x <= b_upper
        constraints = LinearConstraint(A, -np.inf, b_upper)
        
        # Decision variables must be binary (0 or 1 for project selection)
        bounds = Bounds(0, 1)
        integrality = np.ones_like(project_returns, dtype=int)
        
        res = milp(c=c, integrality=integrality, constraints=constraints, bounds=bounds)
        
        if not res.success:
            raise ValueError(f"Optimization failed to converge: {res.message}")
            
        selected_projects = [int(round(val)) for val in res.x]
        max_objective_value = float(-res.fun)
        
        return {
            "status": "success",
            "selected_projects": selected_projects,
            "optimal_value": max_objective_value,
            "message": "Capital allocation optimization solved successfully."
        }

optimization_engine = ClassicalOptimizationEngine()