# PortfolioViz

A desktop app for tracking a personal investment portfolio — add stocks, crypto, or cash, and watch total value, profit/loss, and allocation update live in a dark-themed dashboard.

## Features

- **Add / delete assets** — name, type (Stock / Crypto / Cash), quantity, buy price, current price, with input validation (numeric checks, duplicate names, no negative prices)
- **Live dashboard** — total portfolio value, total profit/loss (color-coded green/red), and overall return %, recalculated on every change
- **Asset allocation pie chart** — Matplotlib chart embedded directly in the window, broken down by asset type with a value-labeled legend
- **CSV-backed persistence** — your portfolio lives in `portfolio.csv`; no database, no account, easy to inspect or back up
- Packaged for distribution via **PyInstaller** (see `PortfolioViz.spec`)

## Getting started

Requires **Python 3.10+**.

```bash
pip install customtkinter pandas matplotlib
python portfolio_viz.py
```

On Windows, `run.bat` does the same thing.

A `portfolio.csv` is created automatically next to the script on first run if one doesn't already exist.

## Building a standalone executable

```bash
pip install pyinstaller
pyinstaller PortfolioViz.spec
```

## Tech stack

- **CustomTkinter** for the UI (dark mode by default)
- **Pandas** for the underlying portfolio data
- **Matplotlib**, embedded via `FigureCanvasTkAgg`, for the allocation chart