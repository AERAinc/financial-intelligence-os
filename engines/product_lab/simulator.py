import numpy as np
from engines.product_lab.schemas import ProductSimulationRequest, ProductSimulationResponse

class FinancialProductSimulator:
    """Simulates cash flows and evaluates pricing for complex structured products via Monte Carlo."""

    @staticmethod
    def simulate_structured_product(request: ProductSimulationRequest) -> ProductSimulationResponse:
        prod = request.product_definition
        S0 = request.initial_asset_price
        T = prod.tenor_years
        r = request.risk_free_rate
        sigma = request.volatility
        paths = request.monte_carlo_paths
        
        # Simple Geometric Brownian Motion simulation for the underlying asset
        dt = T / 252.0  # Daily steps over tenor
        steps = int(252 * T)
        if steps < 1:
            steps = 1
            
        np.random.seed(42)
        # Generate standard normal shocks
        z = np.random.standard_normal((paths, steps))
        
        # Time array
        t = np.linspace(0, T, steps)
        
        # Price paths matrix (paths x steps)
        drift = (r - 0.5 * sigma ** 2) * dt
        diffusion = sigma * np.sqrt(dt) * z
        increment = drift + diffusion
        
        log_paths = np.log(S0) + np.cumsum(increment, axis=1)
        asset_paths = np.exp(log_paths)
        
        # Evaluate barrier breach if barriers exist
        knock_in_occurred = np.zeros(paths, dtype=bool)
        if prod.barriers and "knock_in" in prod.barriers:
            barrier_level = prod.barriers["knock_in"]
            knock_in_occurred = np.any(asset_paths <= barrier_level, axis=1)
            prob_knock_in = float(np.mean(knock_in_occurred))
        else:
            prob_knock_in = 0.0

        # Estimate simple present value based on fixed/floating cash flows discounted
        total_cash_flows = np.zeros(paths)
        for leg in prod.legs:
            annual_cash_flow = leg.notional * (leg.rate_or_spread / 100.0)
            total_cash_flows += annual_cash_flow * T

        discount_factor = np.exp(-r * T)
        pv_paths = total_cash_flows * discount_factor
        
        expected_pv = float(np.mean(pv_paths))
        var_95 = float(np.percentile(pv_paths, 5))

        return ProductSimulationResponse(
            product_id=prod.product_id,
            status="success",
            expected_present_value=expected_pv,
            value_at_risk_95=var_95,
            probability_of_knock_in=prob_knock_in if prod.barriers else None,
            message="Structured financial product simulation completed successfully."
        )

product_simulator = FinancialProductSimulator()