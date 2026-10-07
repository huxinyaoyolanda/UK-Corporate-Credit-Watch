# Project Log

## 2026-10-06 — First publishable version

### Scope locked
- UK Corporate Credit Watch — Automated Early-Warning & Portfolio Monitoring Tool
- 15 UK-listed corporates
- 5 sectors
- 60 company-years
- Python + Excel
- Base / Downside / Severe stress
- Relative 0–100 risk score
- Rule-based early-warning triggers
- RAG watchlist and analyst action

### Current RAG distribution
- RED: 3
- AMBER: 6
- GREEN: 6

### Current top relative-risk screens
- 1. United Utilities (UU) — score 84.6; RED; Debt / EBIT > 6.0x
- 2. National Grid (NG) — score 80.0; RED; Debt / EBIT > 6.0x
- 3. Vodafone (VOD) — score 79.6; RED; interest coverage < 1.5x
- 4. BT Group (BT.A) — score 73.2; AMBER
- 5. Rentokil Initial (RTO) — score 68.9; AMBER; debt growth 18.7% YoY

### CV-safe claims
- 15 companies / 5 sectors / 60 company-years.
- 10+ derived credit and trend indicators.
- 45 scenario-company stress tests across three scenarios.
- Python automated calculation / scoring / trigger pipeline.
- Ranked RAG watchlist with Monitor / Enhanced Review / Escalate actions.

### Do not claim
- Employer-sponsored work.
- A credit rating model.
- A probability-of-default model.
- Live real-time data ingestion.
- Full accounting comparability across sectors.
- Investment recommendations.

### Next optional iteration
- Add automated XBRL/ESEF ingestion as a separate refresh module.
- Add debt-maturity / liquidity fields where definitions can be standardised reliably.
- Add sector-specific thresholds and covenant headroom.
