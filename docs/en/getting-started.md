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

# Financial statements (Free/Light)
financials = ticker.financials

# Dividend history (Standard+ only)
dividends = ticker.dividends

# Detailed financials BS/PL/CF (Standard+ only)
details = ticker.financial_details
```

### Derivatives (Standard+ only)

```python
import pyjquants as pjq

# Futures
futures = pjq.Futures("NK225M")  # Nikkei 225 mini
df = futures.history("30d")

# Options
options = pjq.Options("NK225C25000")
df = options.history("30d")

# Nikkei 225 Index Options
idx_opts = pjq.IndexOptions.nikkei225()
df = idx_opts.history("30d")
```

### Market Data (Standard+ only)

```python
import pyjquants as pjq

market = pjq.Market()

# Trade breakdown by type
df = market.breakdown("7203")

# Outstanding short positions
df = market.short_positions()

# Margin trading alerts
df = market.margin_alerts()

# Sector classifications
sectors = market.sectors_33
```

## API Endpoint Mapping

PyJQuants provides a Pythonic interface to all J-Quants V2 API endpoints.

**Tier legend:** *(L)* = Light+, *(S)* = Standard+, *(P)* = Premium only

### Equities

| J-Quants API | PyJQuants | Description |
|--------------|-----------|-------------|
| `/equities/bars/daily` | `Ticker("7203").history("30d")` | Daily OHLCV prices |
| `/equities/bars/daily/am` | `Ticker("7203").history_am("30d")` | Morning session prices *(P)* |
| `/equities/master` | `Ticker("7203").info` / `search("トヨタ")` | Company info |
| `/equities/earnings-calendar` | `Market().earnings_calendar()` | Earnings announcements |
| `/equities/investor-types` | `Market().investor_trades()` | Market-wide trading by investor type *(L)* |

### Financials

| J-Quants API | PyJQuants | Description |
|--------------|-----------|-------------|
| `/fins/summary` | `Ticker("7203").financials` | Financial statements |
| `/fins/dividend` | `Ticker("7203").dividends` | Dividend history *(P)* |
| `/fins/details` | `Ticker("7203").financial_details` | Detailed BS/PL/CF *(P)* |

### Markets

| J-Quants API | PyJQuants | Description |
|--------------|-----------|-------------|
| `/markets/calendar` | `Market().is_trading_day(date)` | Trading calendar |
| `/markets/margin-interest` | `Market().margin_interest()` | Margin interest *(S)* |
| `/markets/sectors/topix17` | `Market().sectors_17` | 17-sector classification *(S)* |
| `/markets/sectors/topix33` | `Market().sectors_33` | 33-sector classification *(S)* |
| `/markets/short-ratio` | `Market().short_ratio()` | Short selling ratio *(S)* |
| `/markets/breakdown` | `Market().breakdown("7203")` | Trade breakdown by type *(P)* |
| `/markets/short-sale-report` | `Market().short_positions()` | Short positions *(S)* |
| `/markets/margin-alert` | `Market().margin_alerts()` | Margin alerts *(S)* |

### Indices

| J-Quants API | PyJQuants | Description |
|--------------|-----------|-------------|
| `/indices/bars/daily/topix` | `Index.topix().history("30d")` | TOPIX prices *(L)* |
| `/indices/bars/daily` | `Index.nikkei225().history("30d")` | Index prices (incl. Nikkei 225) *(S)* |

### Derivatives

| J-Quants API | PyJQuants | Description |
|--------------|-----------|-------------|
| `/derivatives/bars/daily/futures` | `Futures("NK225M").history("30d")` | Futures prices *(P)* |
| `/derivatives/bars/daily/options` | `Options("NK225C25000").history("30d")` | Options prices *(P)* |
| `/derivatives/bars/daily/options/225` | `IndexOptions.nikkei225().history("30d")` | Nikkei 225 index options *(S)* |

## Rate Limits by Tier

J-Quants V2 API has different rate limits based on subscription tier:

| Tier | Requests/min | Monthly Fee | Best For |
|------|-------------|-------------|----------|
| **Free** | 5 | ¥0 | Testing, learning |
| **Light** | 60 | ~¥1,650 | Personal projects |
| **Standard** | 120 | ~¥3,300 | Active trading |
| **Premium** | 500 | ~¥16,500 | Production systems |

Configure your rate limit to match your tier:

=== "Environment Variable"

    ```bash
    export JQUANTS_RATE_LIMIT=60
    ```

=== "TOML Config"

    ```toml
    [rate_limit]
    requests_per_minute = 60
    ```

!!! tip "Rate Limit Tips"
    - PyJQuants automatically throttles requests to stay within your limit
    - Caching (enabled by default) reduces API calls for repeated queries
    - Use `download()` for batch operations instead of looping through tickers

## Next Steps

- Explore the [Architecture](architecture.md) to understand the library design
- Check the [API Reference](api/index.md) for detailed documentation
- Try the [Quickstart Notebook](examples/quickstart.ipynb) for an interactive tutorial
