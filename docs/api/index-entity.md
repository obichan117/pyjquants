# Index

The `Index` class represents a market index like TOPIX.

## Basic Usage

```python
import pyjquants as pjq

topix = pjq.Index.topix()
print(topix.name)    # "TOPIX"
print(topix.prices)  # Recent price data
```

## API Reference

::: pyjquants.entities.index.Index
    options:
      show_source: false

## Examples

### Get TOPIX

```python
topix = pjq.Index.topix()

print(topix.code)   # Index code
print(topix.name)   # "TOPIX"
print(topix.prices) # DataFrame of prices
```

### All Available Indices

```python
# Get list of all indices
indices = pjq.Index.all()

for idx in indices:
    print(f"{idx.code}: {idx.name}")
```

### Price Data

```python
from datetime import date

topix = pjq.Index.topix()

# Recent prices
prices = topix.prices

# Custom date range
prices = topix.prices_between(date(2024, 1, 1), date(2024, 6, 30))
```
