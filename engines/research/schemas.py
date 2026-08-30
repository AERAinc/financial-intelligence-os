from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FormulaDefinitionRequest(BaseModel):
    formula_id: str = Field(..., description="Unique identifier for the research formula (e.g., CUSTOM_RATIO_01)")
    name: str = Field(..., description="Human-readable name of the ratio or model")
    expression: str = Field(..., description="Mathematical expression (e.g., 'operating_cash_flow / capital_employed')")
    variables: List[str] = Field(..., description="List of input variables required by the formula")
    sector_applicability: List[str] = Field(default=["General"], description="Target industries or sectors")
    assumptions: List[str] = Field(default=[], description="Underlying economic or financial assumptions")

class BacktestEvaluationRequest(BaseModel):
    formula_id: str
    historical_dataset: List[Dict[str, float]] = Field(..., description="List of historical records containing variable values")

class FormulaResearchResponse(BaseModel):
    formula_id: str
    status: str
    validation_passed: bool
    statistical_metrics: Dict[str, float]
    message: str