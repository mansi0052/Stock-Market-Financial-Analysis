"""
generate_synthetic_data.py
---------------------------
Creates realistic stand-in OHLCV data for 6 tech tickers so the whole
pipeline (moving averages, crossover signals, trend detection, charts)
can be built and tested end-to-end RIGHT NOW.

This is a placeholder. Once you run fetch_real_data.py locally (with
yfinance) and get real CSVs, drop them into data/raw/ with the exact
same filenames/columns and rerun analysis.py + build_dashboard.py —
nothing else changes.

Model: correlated Geometric Brownian Motion.
  - One shared "market factor" drives all 6 tickers partially (like the
    real market/tech-sector co-movement you'd see in FAANG+MSFT).
  - Each ticker also has its own drift/volatility/idiosyncratic noise
    calibrated loosely to that company's real-world character
    (e.g. NFLX more volatile, MSFT steadier).
"""
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

RAW_DIR = Path("/home/claude/project/data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 5.5 years of trading days ~ matches a typical "multi-year" analysis window
start_date = "2021-01-04"
end_date = "2026-06-30"
dates = pd.bdate_range(start=start_date, end=end_date)
n = len(dates)

# ticker: (start_price, annual_drift, annual_vol, beta_to_market)
TICKERS = {
    "AAPL":  (132.0, 0.16, 0.28, 1.00),
    "MSFT":  (222.0, 0.18, 0.26, 0.95),
    "GOOGL": (87.0,  0.15, 0.30, 1.05),
    "AMZN":  (159.0, 0.14, 0.34, 1.10),
    "META":  (268.0, 0.12, 0.42, 1.20),
    "NFLX":  (540.0, 0.10, 0.45, 1.15),
}

dt = 1 / 252
market_vol = 0.20
market_factor = np.random.normal(0, market_vol * np.sqrt(dt), n)

for ticker, (p0, mu, sigma, beta) in TICKERS.items():
    idio_vol = np.sqrt(max(sigma**2 - (beta * market_vol) ** 2, 0.01))
    idio_noise = np.random.normal(0, idio_vol * np.sqrt(dt), n)
    daily_return = (mu - 0.5 * sigma**2) * dt + beta * market_factor + idio_noise

    close = p0 * np.exp(np.cumsum(daily_return))
    close = np.round(close, 2)

    # Derive open/high/low from close with small intraday noise
    intraday = np.random.uniform(0.003, 0.018, n)
    open_ = close * (1 + np.random.normal(0, 0.004, n))
    high = np.maximum(open_, close) * (1 + intraday)
    low = np.minimum(open_, close) * (1 - intraday)

    # Volume: baseline + spikes correlated with |daily_return|
    base_vol = np.random.uniform(15_000_000, 45_000_000, n)
    vol_spike = 1 + 6 * np.abs(daily_return)
    volume = (base_vol * vol_spike).astype(int)

    df = pd.DataFrame({
        "Date": dates,
        "Open": np.round(open_, 2),
        "High": np.round(high, 2),
        "Low": np.round(low, 2),
        "Close": close,
        "Adj Close": close,
        "Volume": volume,
    })
    df.to_csv(RAW_DIR / f"{ticker}.csv", index=False)
    print(f"{ticker}: {len(df)} rows -> {RAW_DIR / f'{ticker}.csv'}")

print("\nSynthetic data generated. Replace these files with real data anytime (same schema).")
