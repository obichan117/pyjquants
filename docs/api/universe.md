# Universe

The `Universe` class represents a filterable collection of stocks.

## Basic Usage

```python
import pyjquants as pjq

# Get all stocks
universe = pjq.Universe.all()

# Filter by market segment
prime_stocks = universe.filter_by_market(pjq.MarketSegment.TSE_PRIME)

# Get first 50
top_50 = prime_stocks.head(50)
```

## API Reference

::: pyjquants.collections.universe.Universe
    options:
      show_source: false

## Examples

### Filtering

```python
import pyjquants as pjq

universe = pjq.Universe.all()

# Filter by market segment
prime = universe.filter_by_market(pjq.MarketSegment.TSE_PRIME)
standard = universe.filter_by_market(pjq.MarketSegment.TSE_STANDARD)
growth = universe.filter_by_market(pjq.MarketSegment.TSE_GROWTH)

print(f"Prime: {len(prime)} stocks")
print(f"Standard: {len(standard)} stocks")
print(f"Growth: {len(growth)} stocks")
```

### Getting Price Data

```python
# Get subset of stocks
subset = universe.filter_by_market(pjq.MarketSegment.TSE_PRIME).head(10)

# Get prices for all stocks in subset
prices = subset.prices  # Multi-stock DataFrame
```

### Iteration

```python
universe = pjq.Universe.all()

for stock in universe.head(5):
    print(f"{stock.code}: {stock.name}")
```
