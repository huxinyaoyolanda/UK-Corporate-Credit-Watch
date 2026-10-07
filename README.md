# UK Corporate Credit Watch

**Automated Early-Warning & Portfolio Monitoring Tool**  
Independent project | October 2026 – Present

## What this is

This is an original analyst-style decision tool, not a guided course project and not an academic paper.

It converts a frozen, source-traceable public financial snapshot into:

1. standardized corporate credit metrics;
2. Base / Downside / Severe scenario analysis;
3. rule-based early-warning triggers;
4. a 0–100 relative risk screen;
5. sector context;
6. a ranked RAG watchlist with a suggested action: **Routine Monitor / Enhanced Review / Escalate**.

## Current scope

- **15 UK-listed corporates**
- **5 sectors**
- **4 fiscal years per company**
- **60 company-years**
- **10+ derived leverage, coverage, cash-flow and trend signals**
- **3 stress scenarios / 45 scenario-company stress tests**
- Python analytical pipeline + Excel audit/dashboard layer

## Current watchlist snapshot

- RED: **3**
- AMBER: **6**
- GREEN: **6**
- Highest relative-risk screen: **United Utilities (UU) — 84.6/100**
- Vodafone interest coverage: **1.42x current / 0.91x severe stress**
- Rentokil debt growth: **18.7% YoY**

The screen is **not** a credit rating, probability-of-default model, or investment recommendation.

## Why this is different from research

A research project normally ends with *findings*.  
This project ends with a **decision workflow**:

`Disclosure data -> metrics -> stress -> trigger -> watchlist -> action`

That design is deliberate: the objective is to demonstrate that Python, Excel and financial analysis can be combined into a reusable analyst tool.

## Repository structure

```text
UK_Corporate_Credit_Watch/
├── README.md
├── requirements.txt
├── run_project.bat
├── run_project.sh
├── data/
│   ├── raw/
│   │   └── uk_corporate_financials.csv
│   └── sources/
│       └── source_registry.csv
├── src/
│   ├── config.py
│   └── credit_watch.py
├── model/
│   └── UK_Corporate_Credit_Watch.xlsx
├── output/
│   ├── metrics.csv
│   ├── stress_results.csv
│   ├── watchlist.csv
│   ├── latest_snapshot.csv
│   ├── portfolio_review.md
│   └── charts/
└── docs/
    └── Methodology_and_Interview_Guide.docx
```

## How to run

```bash
pip install -r requirements.txt
python src/credit_watch.py
```

On Windows you can also run `run_project.bat`.

The script uses the frozen CSV snapshot in `data/raw/`, so it can be reproduced without live web access.

## Data-source design

- **Structured extraction layer:** public StockAnalysis financial pages. Those pages state that financial data is provided by S&P Global Market Intelligence.
- **Primary-source validation layer:** each company’s official Investor Relations / Annual Report page is registered in `data/sources/source_registry.csv`.
- The project does **not** claim to live-scrape or automatically download the internet. “Automated” refers to the downstream calculation, scoring, stress and watchlist pipeline.
- Cross-company accounting definitions are not perfectly identical; this is documented as a limitation rather than hidden.

## Core metrics

- EBIT margin
- Interest coverage
- Debt / revenue
- Debt / EBIT
- FCF margin
- FCF / debt
- Revenue growth
- EBIT growth
- Debt growth
- EBIT margin change
- Severe-stress interest coverage

## Stress framework

| Scenario | Revenue | EBIT | Interest cost | Debt | FCF margin |
|---|---:|---:|---:|---:|---:|
| Base | 0% | 0% | 0% | 0% | 0ppt |
| Downside | -5% | -10% | +10% | +5% | -3ppt |
| Severe | -10% | -20% | +25% | +10% | -6ppt |

Stress assumptions are intentionally transparent and editable. They are screening assumptions, not forecasts.

## CV-safe wording

> **UK Corporate Credit Watch | Independent Project | Oct 2026 – Present**  
> Built a Python- and Excel-based early-warning tool covering **15 UK-listed companies across 5 sectors and 60 company-years**, generating **10+ credit/trend indicators and 45 scenario-company stress tests** from source-traceable public financial data.  
> Converted the 15-name universe into **3 RED / 6 AMBER / 6 GREEN** monitoring priorities, flagging Vodafone at **1.42x interest coverage (0.91x under severe stress)** and Rentokil after debt rose **18.7% YoY**.

## Disclaimer

For educational and portfolio demonstration purposes only. This is a relative monitoring screen and does not constitute investment advice, a credit rating or a probability-of-default model.
