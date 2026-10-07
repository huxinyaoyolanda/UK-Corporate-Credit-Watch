# Methodology & Interview Guide

## 1. Business problem

The project is designed as an analyst decision tool rather than an academic paper. The practical question is:

> Across a portfolio of UK-listed non-financial corporates, which names show weaker debt-service headroom, leverage, cash generation or deterioration, and which should be reviewed first?

The workflow is:

`Disclosure data -> standardised metrics -> stress -> trigger -> ranked watchlist -> monitoring action`

The final output is therefore a decision: **Routine Monitor / Enhanced Review / Escalate**.

## 2. Universe

15 UK-listed corporates across five sectors:

- Utilities: National Grid, SSE, United Utilities
- Consumer & Retail: Tesco, Unilever, Diageo
- Healthcare: AstraZeneca, GSK, Smith & Nephew
- Industrials & Services: Rolls-Royce, Rentokil Initial, Compass Group, RELX
- Telecom: Vodafone, BT Group

Banks and insurers are intentionally excluded because their balance sheets and regulatory capital structures require different credit metrics.

## 3. Current scale

- 15 companies
- 5 sectors
- 4 fiscal years per company
- 60 company-years
- 10+ derived leverage, coverage, cash-flow and trend indicators
- 3 stress scenarios
- 45 scenario-company stress tests

## 4. Core metrics

| Metric | Formula | Interpretation |
|---|---|---|
| EBIT margin | EBIT / Revenue | Operating profitability buffer |
| Interest coverage | EBIT / abs(interest expense) | Debt-service headroom; lower is weaker |
| Debt / Revenue | Total debt / Revenue | Debt intensity relative to business scale |
| Debt / EBIT | Total debt / EBIT | Leverage proxy; higher is weaker |
| FCF | Revenue × FCF margin | Cash-generation proxy |
| FCF / Debt | FCF / Total debt | Cash generation relative to debt burden |
| Revenue growth | Revenue_t / Revenue_t-1 - 1 | Top-line trend |
| EBIT growth | EBIT_t / EBIT_t-1 - 1 | Earnings trend |
| Debt growth | Debt_t / Debt_t-1 - 1 | Funding / leverage deterioration signal |
| EBIT margin change | Margin_t - Margin_t-1 | Profitability deterioration or recovery |
| Severe interest coverage | Stress EBIT / stress interest | Downside debt-service headroom |

## 5. Stress framework

| Scenario | Revenue | EBIT | Interest cost | Debt | FCF margin |
|---|---:|---:|---:|---:|---:|
| Base | 0% | 0% | 0% | 0% | 0ppt |
| Downside | -5% | -10% | +10% | +5% | -3ppt |
| Severe | -10% | -20% | +25% | +10% | -6ppt |

The assumptions are deliberately transparent screening shocks, not forecasts.

## 6. Relative risk score

Seven signals are converted to 0-1 relative risk percentiles within the 15-company universe and combined with these weights:

- Debt / EBIT: 25%
- Interest coverage: 20%
- Debt / Revenue: 15%
- FCF margin: 15%
- Debt growth: 10%
- Severe-stress interest coverage: 10%
- EBIT margin change: 5%

The weighted result is scaled to 0-100. It is a **relative monitoring score**, not a rating-agency score or probability of default.

## 7. Early-warning triggers

| Metric | Amber | Red |
|---|---:|---:|
| Interest coverage | <2.5x | <1.5x |
| Debt / EBIT | >4.0x | >6.0x |
| Debt growth | >10% YoY | >20% YoY |
| FCF margin | <0% | <-10% |
| Severe-stress coverage | <1.75x | <1.25x |
| EBIT margin change | <-3ppt | <-5ppt |

Status logic:

- **RED** if a critical coverage threshold is breached, two or more red triggers fire, or relative risk score is at least 80.
- **AMBER** if any amber/red trigger fires or score is at least 60.
- **GREEN** otherwise.

These are custom early-warning rules, not external ratings.

## 8. Current quantitative output

The current model produces:

- **3 RED / 6 AMBER / 6 GREEN** monitoring priorities.
- United Utilities: relative score **84.6/100**, Debt / EBIT **10.46x**, severe interest coverage **1.69x**.
- Vodafone: current interest coverage **1.42x**, falling to **0.91x** under severe stress.
- Rentokil Initial: debt increased **18.7% YoY** in the latest period.
- Rolls-Royce: strongest relative screen at **13.6/100**, Debt / EBIT **1.16x**, current interest coverage **9.33x**.

Interpretation matters: capital-intensive utilities naturally carry more debt, so a high screening score means **review with sector context**, not “this company will default”.

## 9. What Python does

1. Reads the frozen source-traceable dataset.
2. Calculates leverage, coverage, cash-flow, profitability and trend metrics.
3. Runs Base / Downside / Severe scenarios.
4. Converts signals into relative risk percentiles.
5. Applies explicit trigger thresholds.
6. Assigns RAG status and monitoring action.
7. Exports CSV outputs and charts.

## 10. Data-source architecture

- Structured extraction layer: public StockAnalysis financial pages.
- Those pages state that their financial data is provided by S&P Global Market Intelligence.
- Primary-source validation layer: official Investor Relations / Annual Report URL for every company in `data/sources/source_registry.csv`.
- The project uses a frozen snapshot for reproducibility and does **not** claim live web ingestion.

## 11. Why this is different from research

Academic research usually ends with a finding. This project ends with a monitoring action.

**Research:** question -> methodology -> findings -> paper  
**This project:** disclosures -> metrics -> stress -> trigger -> watchlist -> action

That distinction is deliberate because the portfolio already contains published research; this artifact is intended to demonstrate applied analyst judgement and a reusable workflow.

## 12. Interview explanation

### 30 seconds

> I built an independent corporate credit early-warning tool covering 15 UK-listed companies across five sectors and four years of data. Python calculates leverage, coverage, cash-flow and trend signals, runs three stress scenarios and applies transparent triggers. The output is a ranked RAG watchlist that tells me which names should be routinely monitored, reviewed more deeply or escalated. I deliberately designed it as a decision tool rather than another research paper.

### Example quantitative finding

> Vodafone stood out on debt-service resilience: current interest coverage was about 1.42x and fell to about 0.91x under my severe scenario, so the system escalated it for deeper review.

## 13. Limitations

- Cross-sector capital structures differ, so the overall score requires sector interpretation.
- Standardised public data do not perfectly reconcile every company-specific adjusted metric.
- Debt is total debt rather than a fully adjusted net-debt / lease / pension / derivative construct.
- Interest-expense definitions can differ across companies.
- Stress shocks are transparent screening assumptions, not macroeconomic forecasts.
- No default calibration, rating-agency methodology or investment recommendation is claimed.
- The current version uses a frozen data snapshot rather than live XBRL/ESEF ingestion.

## 14. Future enhancements

- Automated ESEF/XBRL data refresh.
- Debt-maturity and liquidity fields.
- Covenant headroom.
- Sector-specific thresholds.
- Reconciliation between reported and adjusted company metrics.
