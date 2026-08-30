import math
from engines.credit.schemas import CreditInputs, CreditResponse

def calculate_credit_risk(inputs: CreditInputs) -> CreditResponse:
    if len(inputs.features) != len(inputs.coefficients):
        raise ValueError("The number of features must match the number of coefficients.")

    # 1. Linear combination: X * beta + intercept (Logit Z)
    z = sum(f * c for f, c in zip(inputs.features, inputs.coefficients)) + inputs.intercept

    # 2. Probability of Default (PD) via Logistic Function: PD = 1 / (1 + e^(-z))
    # Using clipping to prevent overflow for extreme z values
    z_clamped = max(-50.0, min(50.0, z))
    pd = 1.0 / (1.0 + math.exp(-z_clamped))

    # 3. Expected Loss: EL = PD * LGD * EAD
    expected_loss = pd * inputs.loss_given_default * inputs.exposure_at_default

    return CreditResponse(
        linear_combination=round(z, 4),
        probability_of_default=round(pd, 4),
        exposure_at_default=round(inputs.exposure_at_default, 2),
        loss_given_default=round(inputs.loss_given_default, 4),
        expected_loss=round(expected_loss, 2)
    )