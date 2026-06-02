# Rayne Asset Management

This repository contains a Python-based quantitative pairs trading project with a focus on S&P 500 analysis and historical spread backtesting.

## Project Contents

- `pairs_trading/pairs_backtest.py`: Main backtest script using Yahoo Finance data, train/test split, cointegration, regression diagnostics, and strategy performance.
- `Rayne Hedge Fund.html`: Original HTML dashboard asset.

## Running locally

```bash
cd '/Users/rayneperekekeme/Documents/Claude/Projects/Trading stratetgies Portfolio/Rayne Asset Management'
python3 -m venv venv
source venv/bin/activate
pip install -r pairs_trading_repo/requirements.txt
python pairs_trading/pairs_backtest.py
```

## Notes

- This project no longer uses Streamlit.
- The primary deliverable is the Python backtest and notebook workflow.
- Use the notebook files in `pairs_trading_repo/` for exploratory analysis and reporting.
