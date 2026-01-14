# Models & Enums

PyJQuants uses Pydantic models for type safety and validation.

## PriceBar

Represents a single OHLCV price bar.

::: pyjquants.models.price.PriceBar
    options:
      show_source: false

### Example

```python
stock = pjq.Stock("7203")
bar = stock.latest_price

print(f"Date: {bar.date}")
print(f"Open: {bar.open}")
print(f"High: {bar.high}")
print(f"Low: {bar.low}")
print(f"Close: {bar.close}")
print(f"Volume: {bar.volume}")
print(f"Adjustment factor: {bar.adjustment_factor}")
print(f"Adjusted close: {bar.adjusted_close}")
```

## Sector

Represents an industry sector classification.

::: pyjquants.models.company.Sector
    options:
      show_source: false

### Example

```python
stock = pjq.Stock("7203")

# 33-sector classification
sector = stock.sector_33
print(f"Code: {sector.code}")
print(f"Name: {sector.name}")
```

## Enums

### MarketSegment

```python
from pyjquants import MarketSegment

# Available values
MarketSegment.TSE_PRIME     # TSE Prime Market
MarketSegment.TSE_STANDARD  # TSE Standard Market
MarketSegment.TSE_GROWTH    # TSE Growth Market
MarketSegment.OTHER         # Other markets
```

### OrderSide

```python
from pyjquants import OrderSide

OrderSide.BUY   # Buy order
OrderSide.SELL  # Sell order
```

### OrderType

```python
from pyjquants import OrderType

OrderType.MARKET  # Market order (fill at current price)
OrderType.LIMIT   # Limit order (fill at specified price or better)
```

### OrderStatus

```python
from pyjquants import OrderStatus

OrderStatus.PENDING          # Order placed, waiting to fill
OrderStatus.FILLED           # Order fully executed
OrderStatus.PARTIALLY_FILLED # Order partially executed
OrderStatus.CANCELLED        # Order cancelled
OrderStatus.REJECTED         # Order rejected
```

## Type Hints

All models are fully typed. Use them for better IDE support:

```python
from pyjquants import Stock, PriceBar
from pyjquants.models.company import Sector

def analyze_stock(stock: Stock) -> float:
    bar: PriceBar | None = stock.latest_price
    if bar is None:
        return 0.0
    return float(bar.close)

def get_sector(stock: Stock) -> Sector:
    return stock.sector_33
```
