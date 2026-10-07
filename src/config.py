STRESS_SCENARIOS = {
    "Base": {"revenue_shock": 0.00, "ebit_shock": 0.00, "interest_shock": 0.00, "debt_shock": 0.00, "fcf_margin_ppt": 0.00},
    "Downside": {"revenue_shock": -0.05, "ebit_shock": -0.10, "interest_shock": 0.10, "debt_shock": 0.05, "fcf_margin_ppt": -0.03},
    "Severe": {"revenue_shock": -0.10, "ebit_shock": -0.20, "interest_shock": 0.25, "debt_shock": 0.10, "fcf_margin_ppt": -0.06},
}

RISK_WEIGHTS = {
    "Debt_EBIT": 0.25,
    "Interest_Coverage": 0.20,
    "Debt_Revenue": 0.15,
    "FCF_Margin": 0.15,
    "Debt_Growth": 0.10,
    "Severe_Interest_Coverage": 0.10,
    "EBIT_Margin_Change": 0.05,
}

TRIGGERS = {
    "interest_coverage": {"amber": 2.5, "red": 1.5},
    "debt_ebit": {"amber": 4.0, "red": 6.0},
    "debt_growth": {"amber": 0.10, "red": 0.20},
    "fcf_margin": {"amber": 0.00, "red": -0.10},
    "severe_coverage": {"amber": 1.75, "red": 1.25},
    "ebit_margin_change": {"amber": -0.03, "red": -0.05},
}

STATUS_ACTION = {
    "RED": "Escalate",
    "AMBER": "Enhanced Review",
    "GREEN": "Routine Monitor",
}
