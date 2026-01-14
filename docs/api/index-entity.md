# Index

The `Index` class provides access to market indices like TOPIX and Nikkei 225 with a yfinance-style API.

## Basic Usage

```python
import pyjquants as pjq

topix = pjq.Index.topix()
print(topix.name)               # "TOPIX"
df = topix.history("1y")        # Last year of data
```

## API Reference

::: pyjquants.domain.index.Index
    options:
      show_source: false
      members:
        - __init__
        - name
        - history
        - topix
        - nikkei225
        - all

## Examples

### Get TOPIX

```python
topix = pjq.Index.topix()

print(topix.code)   # "0000"
print(topix.name)   # "TOPIX"

# Get price history
df = topix.history("30d")
print(df[['date', 'close']])
```

### Get Nikkei 225

```python
nikkei = pjq.Index.nikkei225()

print(nikkei.code)  # "0001"
print(nikkei.name)  # "Nikkei 225"

df = nikkei.history("1y")
```

### All Available Indices

```python
# Get list of all known indices
indices = pjq.Index.all()

for idx in indices:
    print(f"{idx.code}: {idx.name}")
```

### Price History

```python
from datetime import date

topix = pjq.Index.topix()

# Recent prices (default 30 days)
df = topix.history()

# Specific period
df = topix.history("1y")     # 1 year
df = topix.history("6mo")    # 6 months

# Custom date range
df = topix.history(start="2024-01-01", end="2024-06-30")

# With date objects
df = topix.history(start=date(2024, 1, 1), end=date(2024, 6, 30))
```
