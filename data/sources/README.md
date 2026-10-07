# Data sourcing

The analytical pipeline uses a frozen public-data snapshot so that every result is reproducible.

**Structured extraction layer:** public StockAnalysis company financial pages. These pages state that financial data is provided by S&P Global Market Intelligence.

**Primary-source validation layer:** each company has an official Investor Relations / Annual Report URL in `source_registry.csv`.

The tool deliberately separates *data sourcing* from *decision logic*. It does not claim live web ingestion. A future refresh module could use ESEF/XBRL, but the current portfolio artifact is designed to be fully auditable and explainable in an interview.
