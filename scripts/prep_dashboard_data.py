"""
prep_dashboard_data.py
-----------------------
Converts the processed master dataset into a single compact JSON blob
that gets embedded directly into the HTML dashboard (dashboard.html),
so the artifact is a fully self-contained, single-file deliverable.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

PROC_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
df = pd.read_csv(PROC_DIR / "master_stock_data.csv", parse_dates=["Date"])

tickers = sorted(df["Ticker"].unique().tolist())
data = {"tickers": tickers, "series": {}, "meta": {}}

for t in tickers:
    sub = df[df["Ticker"] == t].sort_values("Date")
    data["series"][t] = {
        "dates": sub["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "close": [None if pd.isna(x) else round(x, 2) for x in sub["Close"]],
        "ma50": [None if pd.isna(x) else round(x, 2) for x in sub["MA50"]],
        "ma200": [None if pd.isna(x) else round(x, 2) for x in sub["MA200"]],
        "volume": [None if pd.isna(x) else int(x) for x in sub["Volume"]],
        "daily_pct_change": [None if pd.isna(x) else round(x, 3) for x in sub["DailyPctChange"]],
        "cumulative_return": [None if pd.isna(x) else round(x, 2) for x in sub["CumulativeReturn"]],
        "drawdown": [None if pd.isna(x) else round(x, 2) for x in sub["Drawdown"]],
        "rolling_vol_30d": [None if pd.isna(x) else round(x, 2) for x in sub["RollingVol30d"]],
        "signal": sub["Signal"].tolist(),
    }
    # crossover marker dates for annotations
    golden = sub.loc[sub["Signal"] == 1, "Date"].dt.strftime("%Y-%m-%d").tolist()
    death = sub.loc[sub["Signal"] == -1, "Date"].dt.strftime("%Y-%m-%d").tolist()
    data["meta"][t] = {"golden_cross_dates": golden, "death_cross_dates": death}

summary = pd.read_csv(PROC_DIR / "summary_stats.csv")
data["summary"] = summary.to_dict(orient="records")

corr = pd.read_csv(PROC_DIR / "correlation_matrix.csv", index_col=0)
data["correlation"] = {"tickers": corr.columns.tolist(), "matrix": corr.values.round(3).tolist()}

with open(PROC_DIR / "dashboard_data.json", "w") as f:
    json.dump(data, f)

size_kb = (PROC_DIR / "dashboard_data.json").stat().st_size / 1024
print(f"dashboard_data.json written: {size_kb:.1f} KB")
