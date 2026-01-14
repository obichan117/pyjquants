# Stock

The `Stock` class represents a Japanese stock with lazy-loaded data.

## Basic Usage

```python
import pyjquants as pjq

stock = pjq.Stock("7203")  # Toyota

# Properties are lazy-loaded
stock.name           # API call on first access
stock.prices         # DataFrame of recent prices
```

## API Reference

::: pyjquants.entities.stock.Stock
    options:
      show_source: false
      members:
        - __init__
        - name
        - name_english
        - sector_17
        - sector_33
        - market_segment
        - listing_date
        - prices
        - adjusted_prices
        - latest_price
        - prices_between
        - adjusted_prices_between
        - price_bars
        - financials
        - dividends
        - next_earnings
        - dividends_between
        - margin_data
        - short_selling
        - margin_data_between
        - short_selling_between
        - all
        - search

## Examples

### Basic Info

```python
stock = pjq.Stock("7203")

print(stock.code)           # "7203"
print(stock.name)           # "トヨタ自動車"
print(stock.name_english)   # "Toyota Motor Corporation"
print(stock.sector_33.name) # "輸送用機器"
print(stock.market_segment) # MarketSegment.TSE_PRIME
```

### Price Data

```python
from datetime import date

# Recent 30 days
prices = stock.prices
print(prices[['date', 'close', 'volume']])

# Custom date range
prices = stock.prices_between(date(2024, 1, 1), date(2024, 6, 30))

# Adjusted for splits
adjusted = stock.adjusted_prices_between(date(2024, 1, 1), date(2024, 6, 30))

# As typed objects
bars = stock.price_bars(date(2024, 1, 1), date(2024, 1, 31))
for bar in bars:
    print(f"{bar.date}: {bar.close}")
```

### Financial Data

```python
# Latest financial statements
financials = stock.financials

# Dividend history
dividends = stock.dividends

# Next earnings date
next_earnings = stock.next_earnings
```

### Discovery

```python
# Get all listed stocks
all_stocks = pjq.Stock.all()

# Search by name or code
results = pjq.Stock.search("toyota")
```
