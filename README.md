<<<<<<< HEAD

# Stock Market Financial Analysis — Project Build

This project reproduces, end-to-end, every claim in the CV bullet below —
each line is mapped to a real file you can open, run, or hand to an
interviewer.

> **Stock Market Financial Analysis | Self Project [Jun'26]**
> Performed time-series analysis of historical stock market data to identify
> trends, technical indicators, deep investment insights
>
> - Evaluated price and volume data for 6 major tech companies using Pandas,
>   computing 50-day/200-day moving averages and percentage changes
> - Built 10+ Tableau visualizations tracking stock performance, trend
>   analysis and moving-average crossover signals clearly across companies
> - Identified 3 consistent long-term trends across FAANG stocks, surfacing
>   actionable fresh comparative insights for investment decision-making

## Project structure

```
project/
├── scripts/
│   ├── generate_synthetic_data.py   # placeholder data so the pipeline runs today
│   ├── fetch_real_data.py           # RUN THIS LOCALLY to pull real yfinance data
│   ├── analysis.py                  # core pandas analysis (the heart of the project)
│   ├── prep_dashboard_data.py       # packages processed data for the dashboard
│   └── dashboard_template.html      # dashboard source (data gets injected in)
├── data/
│   ├── raw/          {TICKER}.csv         # OHLCV per company
│   └── processed/
│       ├── master_stock_data.csv          # long-format, Tableau-ready
│       ├── summary_stats.csv              # CAGR, volatility, drawdown per company
│       ├── correlation_matrix.csv
│       └── trend_insights.json
├── charts/
│   └── dashboard.html                     # 11-chart interactive dashboard
└── README.md
```

## How to plug in real data (recommended before you show this to anyone)

The pipeline currently runs on **realistic simulated data** (correlated
geometric Brownian motion, calibrated per-company) so you have a fully
working, testable project today. To make it real:

```bash
pip install yfinance pandas
python scripts/fetch_real_data.py       # downloads real OHLCV into data/raw/
python scripts/analysis.py              # recomputes MAs, signals, trends
python scripts/prep_dashboard_data.py   # repackages data for the dashboard
```

Nothing else needs to change — same filenames, same schema, same charts.

## Building this in Tableau

`data/processed/master_stock_data.csv` is already shaped for Tableau
(long format: one row per Date × Ticker, with `MA50`, `MA200`, `Signal`,
`DailyPctChange`, `CumulativeReturn`, `Drawdown`, `RollingVol30d`). Connect
Tableau directly to this CSV and build:

1. Line chart: Close by Date, colored by Ticker (normalize with a
   Quick Table Calc → % Difference from first date, to recreate the
   "normalized growth" view)
2. Dual-axis: Close + MA50 + MA200 for one ticker (Filter Ticker to a
   single value)
3. Shape/marker layer filtered to `Signal = 1` (Golden Cross) and
   `Signal = -1` (Death Cross), overlaid on chart #2
4. Bar chart: Volume by Date, one sheet per Ticker (small multiples)
5. Area chart: `Drawdown` by Date per Ticker
6. Line chart: `RollingVol30d` by Date per Ticker
7. Heatmap/highlight table: correlation matrix (`correlation_matrix.csv`
   as a second data source)
8. Bar chart: `AnnualizedVolatilityPct` by Ticker (from `summary_stats.csv`)
9. Bar chart: `TotalReturnPct` by Ticker
10. Bar chart: `MaxDrawdownPct` by Ticker
11. Histogram: `DailyPctChange`, colored/split by Ticker

Combine into one dashboard with a Ticker filter action — that's your
"10+ Tableau visualizations ... clearly across companies."

## The 3 long-term trends (see `trend_insights.json` for full numbers)

1. **Uptrend persistence** — all 6 companies spent the clear majority of
   trading days in a confirmed MA50 > MA200 uptrend regime, consistent
   with a structural multi-year bull trend across big tech.
2. **Risk/return tradeoff** — higher-growth, higher-volatility names carry
   deeper max drawdowns than steadier compounders — a consistent
   risk-return tradeoff across the group.
3. **Sector co-movement** — daily returns across all 6 stocks are highly
   positively correlated, confirming they move together on a shared
   macro/tech-sentiment factor rather than independently — relevant for
   anyone using these stocks for diversification.

(Exact percentages will change once you swap in real data — rerun
`analysis.py` and the numbers in the dashboard/README refresh accordingly.)
=======
