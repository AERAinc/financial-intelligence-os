import numpy as np
from scipy.optimize import minimize
from engines.portfolio.schemas import PortfolioOptimizationInputs, PortfolioOptimizationResponse

def calculate_portfolio_optimization(inputs: PortfolioOptimizationInputs) -> PortfolioOptimizationResponse:
    returns = np.array(inputs.expected_returns)
    cov_matrix = np.array(inputs.covariance_matrix)
    num_assets = len(returns)

    if num_assets == 0 or cov_matrix.shape != (num_assets, num_assets):
        raise ValueError("Invalid dimensions for expected returns or covariance matrix.")

    # Objective function: Negative Sharpe Ratio (since scipy optimizes by minimizing)
    def negative_sharpe(weights):
        p_return = np.dot(weights, returns)
        p_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        if p_volatility == 0:
            return 0.0
        sharpe = (p_return - inputs.risk_free_rate) / p_volatility
        return -sharpe

    # Constraints: sum of weights equals 1.0
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    
    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    
    # Initial guess: equal weighting
    init_guess = num_assets * [1.0 / num_assets]

    result = minimize(negative_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    if not result.success:
        raise ValueError(f"Portfolio optimization failed to converge: {result.message}")

    optimal_weights = result.x.tolist()
    p_return = float(np.dot(result.x, returns))
    p_volatility = float(np.sqrt(np.dot(result.x.T, np.dot(cov_matrix, result.x))))
    sharpe_ratio = float((p_return - inputs.risk_free_rate) / p_volatility) if p_volatility > 0 else 0.0

    return PortfolioOptimizationResponse(
        optimal_weights=[round(w, 4) for w in optimal_weights],
        portfolio_return=round(p_return, 4),
        portfolio_volatility=round(p_volatility, 4),
        sharpe_ratio=round(sharpe_ratio, 4)
    )