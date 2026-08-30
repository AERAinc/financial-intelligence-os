import math
import numpy as np
from engines.econometrics.schemas import RegressionInputs, RegressionResponse, VaRInputs, VaRResponse

def run_linear_regression(inputs: RegressionInputs) -> RegressionResponse:
    x = np.array(inputs.independent_var, dtype=float)
    y = np.array(inputs.dependent_var, dtype=float)
    
    if len(x) != len(y):
        raise ValueError("X and Y datasets must have the exact same length.")
        
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - (slope * x_mean)
    
    y_pred = intercept + slope * x
    ss_tot = np.sum((y - y_mean) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    std_err = math.sqrt(ss_res / (n - 2)) / math.sqrt(np.sum((x - x_mean) ** 2)) if n > 2 else 0.0

    return RegressionResponse(
        slope=round(float(slope), 4),
        intercept=round(float(intercept), 4),
        r_squared=round(float(r_squared), 4),
        std_err=round(float(std_err), 4)
    )

def calculate_var(inputs: VaRInputs) -> VaRResponse:
    # Standard Normal Distribution Z-score lookup
    z_scores = {0.90: 1.2815, 0.95: 1.64485, 0.99: 2.32635}
    z_score = z_scores.get(round(inputs.confidence_level, 2), 1.64485)
    
    horizon_std_dev = inputs.std_dev * math.sqrt(inputs.time_horizon_days)
    horizon_mean = inputs.mean_return * inputs.time_horizon_days
    
    var_amount = inputs.portfolio_value * (z_score * horizon_std_dev - horizon_mean)
    
    return VaRResponse(
        value_at_risk=round(float(var_amount), 2),
        confidence_level=inputs.confidence_level,
        horizon_days=inputs.time_horizon_days
    )