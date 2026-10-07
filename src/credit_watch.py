from pathlib import Path
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from config import STRESS_SCENARIOS, RISK_WEIGHTS, TRIGGERS, STATUS_ACTION

RAW = ROOT / "data" / "raw" / "uk_corporate_financials.csv"
OUT = ROOT / "output"
CHARTS = OUT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)


def risk_percentile(series, higher_is_worse=True):
    """0 = strongest relative position; 1 = weakest relative position."""
    ranks = series.rank(method="average", ascending=higher_is_worse)
    n = series.notna().sum()
    if n <= 1:
        return series * 0
    return (ranks - 1) / (n - 1)


def calculate_metrics(df):
    df = df.sort_values(["Company", "FY"]).copy()
    df["EBIT_Margin"] = df["EBIT"] / df["Revenue"]
    df["Interest_Coverage"] = df["EBIT"] / df["Interest_Expense"].abs()
    df["Debt_Revenue"] = df["Total_Debt"] / df["Revenue"]
    df["Debt_EBIT"] = np.where(df["EBIT"] > 0, df["Total_Debt"] / df["EBIT"], np.nan)
    df["FCF"] = df["Revenue"] * df["FCF_Margin"]
    df["FCF_Debt"] = df["FCF"] / df["Total_Debt"]
    df["Revenue_Growth"] = df.groupby("Company")["Revenue"].pct_change()
    df["EBIT_Growth"] = df.groupby("Company")["EBIT"].pct_change()
    df["Debt_Growth"] = df.groupby("Company")["Total_Debt"].pct_change()
    df["EBIT_Margin_Change"] = df.groupby("Company")["EBIT_Margin"].diff()
    return df


def run_stress(latest):
    all_rows = []
    for scenario, s in STRESS_SCENARIOS.items():
        x = latest.copy()
        x["Scenario"] = scenario
        x["Stress_Revenue"] = x["Revenue"] * (1 + s["revenue_shock"])
        x["Stress_EBIT"] = x["EBIT"] * (1 + s["ebit_shock"])
        x["Stress_Interest"] = x["Interest_Expense"] * (1 + s["interest_shock"])
        x["Stress_Debt"] = x["Total_Debt"] * (1 + s["debt_shock"])
        x["Stress_FCF_Margin"] = x["FCF_Margin"] + s["fcf_margin_ppt"]
        x["Stress_Interest_Coverage"] = x["Stress_EBIT"] / x["Stress_Interest"].abs()
        x["Stress_Debt_EBIT"] = np.where(x["Stress_EBIT"] > 0, x["Stress_Debt"] / x["Stress_EBIT"], np.nan)
        x["Stress_Debt_Revenue"] = x["Stress_Debt"] / x["Stress_Revenue"]
        all_rows.append(x)
    return pd.concat(all_rows, ignore_index=True)


def get_trigger_list(row):
    out = []
    t = TRIGGERS

    if row["Interest_Coverage"] < t["interest_coverage"]["red"]:
        out.append(("Interest coverage < 1.5x", "RED"))
    elif row["Interest_Coverage"] < t["interest_coverage"]["amber"]:
        out.append(("Interest coverage < 2.5x", "AMBER"))

    if pd.notna(row["Debt_EBIT"]):
        if row["Debt_EBIT"] > t["debt_ebit"]["red"]:
            out.append(("Debt / EBIT > 6.0x", "RED"))
        elif row["Debt_EBIT"] > t["debt_ebit"]["amber"]:
            out.append(("Debt / EBIT > 4.0x", "AMBER"))

    if row["Debt_Growth"] > t["debt_growth"]["red"]:
        out.append(("Debt growth > 20% YoY", "RED"))
    elif row["Debt_Growth"] > t["debt_growth"]["amber"]:
        out.append(("Debt growth > 10% YoY", "AMBER"))

    if row["FCF_Margin"] < t["fcf_margin"]["red"]:
        out.append(("FCF margin < -10%", "RED"))
    elif row["FCF_Margin"] < t["fcf_margin"]["amber"]:
        out.append(("FCF margin < 0%", "AMBER"))

    if row["Severe_Interest_Coverage"] < t["severe_coverage"]["red"]:
        out.append(("Severe stress coverage < 1.25x", "RED"))
    elif row["Severe_Interest_Coverage"] < t["severe_coverage"]["amber"]:
        out.append(("Severe stress coverage < 1.75x", "AMBER"))

    if row["EBIT_Margin_Change"] < t["ebit_margin_change"]["red"]:
        out.append(("EBIT margin down > 5ppt", "RED"))
    elif row["EBIT_Margin_Change"] < t["ebit_margin_change"]["amber"]:
        out.append(("EBIT margin down > 3ppt", "AMBER"))
    return out


def build_watchlist(metrics, stress):
    latest = metrics.groupby("Company", as_index=False).tail(1).copy()
    severe = stress[stress["Scenario"].eq("Severe")][["Company", "Stress_Interest_Coverage", "Stress_Debt_EBIT"]].copy()
    severe = severe.rename(columns={"Stress_Interest_Coverage": "Severe_Interest_Coverage", "Stress_Debt_EBIT": "Severe_Debt_EBIT"})
    latest = latest.merge(severe, on="Company", how="left")

    risk_specs = {
        "Debt_EBIT": True,
        "Interest_Coverage": False,
        "Debt_Revenue": True,
        "FCF_Margin": False,
        "Debt_Growth": True,
        "Severe_Interest_Coverage": False,
        "EBIT_Margin_Change": False,
    }
    for metric, higher_worse in risk_specs.items():
        latest[f"Risk_{metric}"] = risk_percentile(latest[metric], higher_worse)

    latest["Risk_Score"] = 100 * sum(
        latest[f"Risk_{metric}"] * weight for metric, weight in RISK_WEIGHTS.items()
    )

    latest["Sector_Risk_Percentile"] = latest.groupby("Sector")["Risk_Score"].rank(method="average", pct=True)

    latest["Trigger_List"] = latest.apply(get_trigger_list, axis=1)
    latest["Red_Triggers"] = latest["Trigger_List"].apply(lambda xs: sum(1 for _, level in xs if level == "RED"))
    latest["Amber_Triggers"] = latest["Trigger_List"].apply(lambda xs: sum(1 for _, level in xs if level == "AMBER"))
    latest["Main_Trigger"] = latest["Trigger_List"].apply(lambda xs: xs[0][0] if xs else "None")
    latest["Trigger_Summary"] = latest["Trigger_List"].apply(
        lambda xs: "; ".join([f"{level}: {label}" for label, level in xs]) if xs else "No hard threshold triggered"
    )
    critical_red = (latest["Interest_Coverage"] < TRIGGERS["interest_coverage"]["red"]) | (
        latest["Severe_Interest_Coverage"] < TRIGGERS["severe_coverage"]["red"]
    )
    latest["Status"] = np.where(
        critical_red | (latest["Red_Triggers"] >= 2) | (latest["Risk_Score"] >= 80),
        "RED",
        np.where((latest["Red_Triggers"] + latest["Amber_Triggers"] > 0) | (latest["Risk_Score"] >= 60), "AMBER", "GREEN"),
    )
    latest["Action"] = latest["Status"].map(STATUS_ACTION)
    latest["Rank"] = latest["Risk_Score"].rank(method="min", ascending=False).astype(int)
    return latest.sort_values(["Rank", "Company"]).reset_index(drop=True)


def charts(watch):
    plot = watch.sort_values("Risk_Score", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(plot["Company"], plot["Risk_Score"])
    ax.set_xlabel("Relative risk score (0-100; higher = weaker)")
    ax.set_title("UK Corporate Credit Watch — Relative Risk Screen")
    fig.tight_layout()
    fig.savefig(CHARTS / "risk_score.png", dpi=180)
    plt.close(fig)

    plot = watch.sort_values("Interest_Coverage", ascending=False)
    x = np.arange(len(plot))
    width = 0.38
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width / 2, plot["Interest_Coverage"], width, label="Current")
    ax.bar(x + width / 2, plot["Severe_Interest_Coverage"], width, label="Severe stress")
    ax.set_xticks(x)
    ax.set_xticklabels(plot["Ticker"], rotation=45, ha="right")
    ax.set_ylabel("Interest coverage (x)")
    ax.set_title("Debt-service resilience: current vs severe stress")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "interest_coverage_stress.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    status_counts = watch["Status"].value_counts().reindex(["GREEN", "AMBER", "RED"]).fillna(0)
    ax.bar(status_counts.index, status_counts.values)
    ax.set_ylabel("Companies")
    ax.set_title("Current RAG watchlist distribution")
    fig.tight_layout()
    fig.savefig(CHARTS / "rag_distribution.png", dpi=180)
    plt.close(fig)


def main():
    raw = pd.read_csv(RAW)
    metrics = calculate_metrics(raw)
    stress = run_stress(metrics.groupby("Company", as_index=False).tail(1).copy())
    watch = build_watchlist(metrics, stress)

    metrics.to_csv(OUT / "metrics.csv", index=False)
    stress.to_csv(OUT / "stress_results.csv", index=False)
    watch.to_csv(OUT / "watchlist.csv", index=False)

    latest_cols = [
        "Rank", "Company", "Ticker", "Sector", "FY", "Risk_Score", "Sector_Risk_Percentile", "Status", "Action",
        "Main_Trigger", "Red_Triggers", "Amber_Triggers", "Debt_EBIT", "Interest_Coverage", "Debt_Revenue",
        "FCF_Margin", "Debt_Growth", "EBIT_Margin_Change", "Severe_Interest_Coverage", "Trigger_Summary",
    ]
    watch[latest_cols].to_csv(OUT / "latest_snapshot.csv", index=False)
    charts(watch)

    red = int((watch["Status"] == "RED").sum())
    amber = int((watch["Status"] == "AMBER").sum())
    green = int((watch["Status"] == "GREEN").sum())
    top = watch.iloc[0]

    review = f"""# Portfolio Review — Current Snapshot

Universe: {watch['Company'].nunique()} UK-listed corporates across {watch['Sector'].nunique()} sectors.
History: {metrics.shape[0]} company-years.
RAG distribution: {green} Green / {amber} Amber / {red} Red.

Highest relative-risk name: {top['Company']} ({top['Ticker']})
- Relative risk score: {top['Risk_Score']:.1f}/100
- Current interest coverage: {top['Interest_Coverage']:.2f}x
- Severe-stress interest coverage: {top['Severe_Interest_Coverage']:.2f}x
- Debt / EBIT: {top['Debt_EBIT']:.2f}x
- Main trigger: {top['Main_Trigger']}
- Suggested monitoring action: {top['Action']}

Important: this is a relative early-warning screen, not a credit rating, probability-of-default model, or investment recommendation.
"""
    (OUT / "portfolio_review.md").write_text(review, encoding="utf-8")
    print(watch[latest_cols].to_string(index=False))
    print("\n" + review)


if __name__ == "__main__":
    main()
