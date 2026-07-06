"""
fetch_real_data.py
-------------------
RUN THIS ON YOUR OWN MACHINE (needs internet access).

Installs:  pip install yfinance pandas

What it does:
  Downloads ~5.5 years of daily OHLCV data for the 6 tickers used in
  this project (AAPL, MSFT, GOOGL, AMZN, META, NFLX) and saves one CSV
  per ticker into data/raw/, using EXACTLY the same schema as the
  synthetic placeholder data:

      Date, Open, High, Low, Close, Adj Close, Volume

  Once these files exist, just rerun analysis.py and build_dashboard.py
  from this project folder — everything downstream (moving averages,
  crossover signals, trend detection, charts) will automatically use
  the real data instead of the synthetic placeholder.

Usage:
    python fetch_real_data.py
"""
import yfinance as yf
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NFLX"]
START_DATE = "2021-01-01"
END_DATE = "2026-06-30"   # adjust to "today" if you want the latest data

for ticker in TICKERS:
    print(f"Downloading {ticker} ...")
    df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False, progress=False)

    if df.empty:
        print(f"  WARNING: no data returned for {ticker}, skipping.")
        continue

    # yfinance sometimes returns MultiIndex columns when downloading — flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()  # Date becomes a column
    df = df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

    out_path = RAW_DIR / f"{ticker}.csv"
    df.to_csv(out_path, index=False)
    print(f"  Saved {len(df)} rows -> {out_path}")

print("\nDone. Now rerun: python scripts/analysis.py && python scripts/build_dashboard.py")
