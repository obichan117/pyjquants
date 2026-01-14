# Market

The `Market` class provides market utilities like trading calendar and sector information.

## Basic Usage

```python
import pyjquants as pjq
from datetime import date

market = pjq.Market()

# Check if a day is a trading day
market.is_trading_day(date(2024, 12, 25))  # False

# Get sector information
sectors = market.sectors_33
```

## API Reference

::: pyjquants.domain.market.Market
    options:
      show_source: false
      members:
        - __init__
        - trading_calendar
        - is_trading_day
        - trading_days
        - next_trading_day
        - prev_trading_day
        - sectors
        - sectors_33
        - sectors_17
        - investor_trades
        - breakdown
        - short_positions
        - margin_alerts
        - earnings_calendar
        - short_ratio
        - margin_interest

## Examples

### Trading Calendar

```python
from datetime import date

market = pjq.Market()

# Check trading day
is_open = market.is_trading_day(date(2024, 12, 25))
print(is_open)  # False (Christmas)

# Get trading days in range
trading_days = market.trading_days(date(2024, 1, 1), date(2024, 1, 31))

# Next trading day
next_day = market.next_trading_day(date(2024, 1, 1))
```

### Sector Information

```python
market = pjq.Market()

# 17-sector classification
sectors_17 = market.sectors_17
for s in sectors_17:
    print(f"{s.code}: {s.name}")

# 33-sector classification
sectors_33 = market.sectors_33
for s in sectors_33:
    print(f"{s.code}: {s.name}")
```

### Investor Trades

```python
from datetime import date

market = pjq.Market()

# Get market-wide trading by investor type
df = market.investor_trades(start=date(2024, 1, 1), end=date(2024, 12, 31))
# Returns DataFrame with: date, proprietary, individual, foreign, etc.
```

### Trade Breakdown

```python
market = pjq.Market()

# Get trade breakdown by type for a specific stock (Premium tier only)
df = market.breakdown("7203")
# Returns DataFrame with trade counts by investor category
```

### Short Positions

```python
market = pjq.Market()

# Get outstanding short positions (Standard+ tier)
df = market.short_positions()
# Returns DataFrame with short sale reports across the market
```

### Margin Alerts

```python
market = pjq.Market()

# Get margin trading alerts (Standard+ tier)
df = market.margin_alerts()
# Returns DataFrame with stocks flagged for margin trading limits
```

### Earnings Calendar

```python
from datetime import date

market = pjq.Market()

# Get scheduled earnings announcements
df = market.earnings_calendar(start=date(2024, 1, 1), end=date(2024, 3, 31))
# Returns DataFrame with: code, company_name, announcement_date, fiscal_year, fiscal_quarter
```

### Short Ratio

```python
market = pjq.Market()

# Get short selling ratio by sector (Standard+ tier)
df = market.short_ratio()
# Returns DataFrame with: date, sector_33_code, selling_value
```

### Margin Interest

```python
market = pjq.Market()

# Get margin trading balances (Standard+ tier)
df = market.margin_interest(code="7203")
# Returns DataFrame with: code, date, margin_buying_balance, margin_selling_balance
```
