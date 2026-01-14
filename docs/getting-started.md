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

Set your J-Quants credentials:

```bash
export JQUANTS_MAIL_ADDRESS="your_email@example.com"
export JQUANTS_PASSWORD="your_password"
```

### TOML Configuration (Optional)

Create `~/.jquants/config.toml`:

```toml
[credentials]
mail_address = "your_email@example.com"
password = "your_password"

[cache]
enabled = true
ttl_seconds = 3600

[rate_limit]
requests_per_minute = 60
```

## Basic Usage

### Working with Stocks

```python
import pyjquants as pjq

# Create a stock by code
stock = pjq.Stock("7203")  # Toyota

# Basic info (lazy-loaded from API)
print(stock.name)           # "トヨタ自動車"
print(stock.name_english)   # "Toyota Motor Corporation"
print(stock.sector_33.name) # "輸送用機器"
print(stock.market_segment) # MarketSegment.TSE_PRIME

# Price data as DataFrame
prices = stock.prices  # Recent 30 trading days
print(prices[['date', 'open', 'high', 'low', 'close', 'volume']])

# Custom date range
from datetime import date
prices = stock.prices_between(date(2024, 1, 1), date(2024, 6, 30))
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

### Paper Trading

```python
import pyjquants as pjq
from datetime import date

# Initialize trader
trader = pjq.Trader(initial_cash=10_000_000)

# Get stock
toyota = pjq.Stock("7203")

# Place orders
order = trader.buy(toyota, 100)              # Market buy
order = trader.buy(toyota, 100, price=2500)  # Limit buy

# Simulate fills with historical prices
executions = trader.simulate_fills(date(2024, 6, 15))

# Check portfolio
print(f"Cash: {trader.cash}")
print(f"Total value: {trader.portfolio.total_value}")
print(f"Positions: {trader.portfolio.positions}")
```

## Next Steps

- Explore the [Architecture](architecture.md) to understand the library design
- Check the [API Reference](api/index.md) for detailed documentation
- Try the [Quickstart Notebook](examples/quickstart.ipynb) for an interactive tutorial
