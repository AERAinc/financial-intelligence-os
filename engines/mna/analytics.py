from engines.mna.schemas import MNAInputs, MNAResponse

def calculate_mna(inputs: MNAInputs) -> MNAResponse:
    if inputs.acquirer_shares <= 0 or inputs.acquirer_share_price <= 0:
        raise ValueError("Acquirer shares and share price must be greater than zero.")

    # 1. Standalone EPS
    acquirer_eps = inputs.acquirer_net_income / inputs.acquirer_shares

    # 2. After-tax Synergies
    after_tax_synergies = inputs.synergies * (1.0 - inputs.tax_rate)

    # 3. Pro-Forma Net Income = Acquirer NI + Target NI + After-tax Synergies
    pro_forma_net_income = inputs.acquirer_net_income + inputs.target_net_income + after_tax_synergies

    # 4. New Shares Issued for Purchase (assuming 100% stock consideration for simplicity)
    shares_issued = inputs.purchase_price / inputs.acquirer_share_price
    pro_forma_shares = inputs.acquirer_shares + shares_issued

    # 5. Pro-Forma EPS and Accretion/Dilution
    pro_forma_eps = pro_forma_net_income / pro_forma_shares if pro_forma_shares > 0 else 0.0
    eps_change_pct = ((pro_forma_eps - acquirer_eps) / acquirer_eps) * 100.0 if acquirer_eps > 0 else 0.0

    target_eps_contribution = inputs.target_net_income / pro_forma_shares if pro_forma_shares > 0 else 0.0

    return MNAResponse(
        acquirer_eps=round(acquirer_eps, 2),
        target_eps_contribution=round(target_eps_contribution, 2),
        pro_forma_net_income=round(pro_forma_net_income, 2),
        pro_forma_shares=round(pro_forma_shares, 2),
        pro_forma_eps=round(pro_forma_eps, 2),
        eps_change_pct=round(eps_change_pct, 2)
    )