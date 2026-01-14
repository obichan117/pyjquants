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
