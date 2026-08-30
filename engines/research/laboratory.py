import numpy as np
from engines.research.schemas import FormulaDefinitionRequest, BacktestEvaluationRequest, FormulaResearchResponse

class FormulaResearchLaboratory:
    """Experimental lab for defining, testing, and validating custom financial formulas and ratios."""

    @staticmethod
    def evaluate_formula_backtest(
        definition: FormulaDefinitionRequest, 
        backtest_payload: BacktestEvaluationRequest
    ) -> FormulaResearchResponse:
        """
        Evaluates a custom mathematical expression across historical dataset records 
        to check for numerical stability, outliers, and distribution properties.
        """
        results = []
        errors = 0
        
        for record in backtest_payload.historical_dataset:
            try:
                # Safely map variables from the record into local evaluation context
                local_context = {var: record[var] for var in definition.variables if var in record}
                if len(local_context) != len(definition.variables):
                    errors += 1
                    continue
                
                # Evaluate expression securely
                val = eval(definition.expression, {"__builtins__": {}}, local_context)
                if np.isnan(val) or np.isinf(val):
                    errors += 1
                else:
                    results.append(float(val))
            except ZeroDivisionError:
                errors += 1
            except Exception:
                errors += 1

        if not results:
            return FormulaResearchResponse(
                formula_id=definition.formula_id,
                status="failed",
                validation_passed=False,
                statistical_metrics={},
                message="Backtest failed: All records resulted in computation errors or missing variables."
            )

        arr = np.array(results)
        stats = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std_dev": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "error_count": float(errors)
        }

        validation_passed = errors == 0 and stats["std_dev"] > 0.0

        return FormulaResearchResponse(
            formula_id=definition.formula_id,
            status="success" if validation_passed else "warning",
            validation_passed=validation_passed,
            statistical_metrics=stats,
            message="Formula successfully backtested and evaluated against historical data."
        )

research_lab = FormulaResearchLaboratory()