# Ticker

The `Ticker` class provides a yfinance-style API for accessing Japanese stock data.

## Basic Usage

```python
import pyjquants as pjq

ticker = pjq.Ticker("7203")  # Toyota

# Stock info (lazy-loaded)
ticker.info.name           # "トヨタ自動車"
ticker.info.sector         # "輸送用機器"

# Price history
df = ticker.history("30d")        # Recent 30 days
df = ticker.history("1y")         # Last year
df = ticker.history(start="2024-01-01", end="2024-12-31")  # Custom range
```

## API Reference

::: pyjquants.domain.ticker.Ticker
    options:
      show_source: false
      members:
        - __init__
        - info
        - history
        - history_am
        - financials
        - financial_details
        - dividends
        - refresh

## Module Functions

### download

Download price data for multiple tickers:

```python
df = pjq.download(["7203", "6758"], period="1y")
```

::: pyjquants.domain.ticker.download
    options:
      show_source: false

### search

Search for tickers by name or code:

```python
tickers = pjq.search("トヨタ")
```

::: pyjquants.domain.ticker.search
    options:
      show_source: false

## Examples

### Stock Info

```python
ticker = pjq.Ticker("7203")

print(ticker.info.code)            # "7203"
print(ticker.info.name)            # "トヨタ自動車"
print(ticker.info.name_english)    # "Toyota Motor Corporation"
print(ticker.info.sector)          # "輸送用機器"
print(ticker.info.market)          # "Prime"
```

### Price History

```python
# Recent 30 days (default)
df = ticker.history()

# Specific period
df = ticker.history("1y")    # 1 year
df = ticker.history("6mo")   # 6 months
df = ticker.history("30d")   # 30 days

# Custom date range
df = ticker.history(start="2024-01-01", end="2024-06-30")

# With date objects
from datetime import date
df = ticker.history(start=date(2024, 1, 1), end=date(2024, 6, 30))
```

### Multi-Ticker Download

```python
# Download close prices for multiple tickers
df = pjq.download(["7203", "6758", "9984"], period="1y")
print(df.head())
#         date     7203     6758     9984
# 0 2024-01-04  2530.0  1245.0  5678.0
# 1 2024-01-05  2545.0  1256.0  5690.0
```

### Financial Data

```python
# Financial statements (summary)
financials = ticker.financials

# Full financial details (BS/PL/CF)
details = ticker.financial_details

# Dividend history
dividends = ticker.dividends
```

### Morning Session Prices

```python
# Get morning session (AM) prices only
df = ticker.history_am("30d")
df = ticker.history_am(start="2024-01-01", end="2024-06-30")
```

### Search

```python
# Search by Japanese name
tickers = pjq.search("トヨタ")
for t in tickers:
    print(f"{t.code}: {t.info.name}")

# Search by English name
tickers = pjq.search("Toyota")

# Search by code prefix
tickers = pjq.search("72")  # All codes starting with 72
```
