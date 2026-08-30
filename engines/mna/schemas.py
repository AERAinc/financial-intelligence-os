from pydantic import BaseModel

class MNAInputs(BaseModel):
    acquirer_net_income: float
    target_net_income: float
    acquirer_shares: float
    acquirer_share_price: float
    purchase_price: float         # Total purchase price offered for the target
    synergies: float              # Pre-tax cost synergies
    tax_rate: float               # Corporate tax rate (e.g., 0.25 for 25%)

class MNAResponse(BaseModel):
    acquirer_eps: float
    target_eps_contribution: float
    pro_forma_net_income: float
    pro_forma_shares: float
    pro_forma_eps: float
    eps_change_pct: float         # Positive means accretive, negative means dilutive