# Getting Started

This guide will help you set up PyJQuants and make your first API calls.

## Prerequisites

- Python 3.10 or higher
- A J-Quants account ([sign up here](https://application.jpx-jquants.com/))

## Installation

=== "pip"

    ```bash
    pip install pyjquants
    ```

=== "uv"

    ```bash
    uv add pyjquants
    ```

For development (includes testing and documentation tools):

```bash
pip install pyjquants[dev]
```

## Configuration

### Environment Variables

Set your J-Quants API key (get it from the [J-Quants dashboard](https://application.jpx-jquants.com/)):

```bash
export JQUANTS_API_KEY="your_api_key_here"
```

### TOML Configuration (Optional)

Create `~/.jquants/config.toml`:

```toml
[auth]
api_key = "your_api_key_here"

[cache]
enabled = true
ttl_seconds = 3600

[rate_limit]
requests_per_minute = 60  # V2 tiers: Free=5, Light=60, Standard=120, Premium=500
```

## Basic Usage

### Working with Tickers

```python
import pyjquants as pjq

# Create a ticker by code
ticker = pjq.Ticker("7203")  # Toyota

# Basic info (lazy-loaded from API)
print(ticker.info.name)           # "トヨタ自動車"
print(ticker.info.name_english)   # "Toyota Motor Corporation"
print(ticker.info.sector)         # "輸送用機器"
print(ticker.info.market)         # "Prime"

# Price history (yfinance-style)
df = ticker.history("30d")        # Recent 30 days
df = ticker.history("1y")         # Last year
df = ticker.history(start="2024-01-01", end="2024-06-30")  # Custom range

print(df[['date', 'open', 'high', 'low', 'close', 'volume']])
```

### Multi-Ticker Download

```python
import pyjquants as pjq

# Download multiple tickers at once
df = pjq.download(["7203", "6758", "9984"], period="30d")
print(df.head())
```

### Search for Tickers

```python
import pyjquants as pjq

# Search by name or code
tickers = pjq.search("トヨタ")
for t in tickers:
    print(f"{t.code}: {t.info.name}")
```

### Market Indices

```python
import pyjquants as pjq

# Get TOPIX index
topix = pjq.Index.topix()
df = topix.history("1y")

# Get Nikkei 225
nikkei = pjq.Index.nikkei225()
df = nikkei.history("30d")
```

### Market Information

```python
import pyjquants as pjq
from datetime import date

market = pjq.Market()

# Check trading days
market.is_trading_day(date(2024, 12, 25))  # False (holiday)
market.next_trading_day(date(2024, 1, 1))  # Next open day

# Sector information
sectors = market.sectors_33  # 33-sector classification
```

### Financial Data

```python
import pyjquants as pjq

ticker = pjq.Ticker("7203")

# Financial statements
financials = ticker.financials

# Dividend history
dividends = ticker.dividends
```

## Next Steps

- Explore the [Architecture](architecture.md) to understand the library design
- Check the [API Reference](api/index.md) for detailed documentation
- Try the [Quickstart Notebook](examples/quickstart.ipynb) for an interactive tutorial
