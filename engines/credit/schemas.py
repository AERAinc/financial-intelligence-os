from pydantic import BaseModel
from typing import List

class CreditInputs(BaseModel):
    features: List[float]        # Financial ratios or feature values (e.g., [Debt/Equity, Current Ratio, ROE])
    coefficients: List[float]    # Logistic regression beta coefficients corresponding to features
    intercept: float             # Logistic model intercept (beta_0)
    exposure_at_default: float   # EAD: Total value exposed at default
    loss_given_default: float    # LGD: Fraction of exposure lost if default occurs (e.g., 0.45 for 45%)

class CreditResponse(BaseModel):
    linear_combination: float    # X * beta + intercept
    probability_of_default: float # PD calculated via logistic function
    exposure_at_default: float
    loss_given_default: float
    expected_loss: float         # EL = PD * LGD * EAD