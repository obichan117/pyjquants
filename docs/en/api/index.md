# API Reference

This section documents all public classes and functions in PyJQuants.

## Quick Links

| Category | Classes & Functions |
|----------|---------------------|
| [Ticker](stock.md) | `Ticker`, `download()`, `search()` |
| [Index](index-entity.md) | `Index` |
| [Market](market.md) | `Market` |
| [Models](models.md) | `PriceBar`, `Sector`, `MarketSegment` |

## Import Patterns

### Standard Usage

```python
import pyjquants as pjq

# Single ticker
ticker = pjq.Ticker("7203")
df = ticker.history("30d")

# Multiple tickers
df = pjq.download(["7203", "6758"], period="1y")

# Search
tickers = pjq.search("トヨタ")
```

### Explicit Imports

```python
from pyjquants import Ticker, Index, Market, download, search
from pyjquants import PriceBar, Sector, MarketSegment
```

## All Exports

The following are available from `pyjquants`:

### Main API (yfinance-style)
- `Ticker` - Stock ticker with `.history()` method
- `download()` - Download price data for multiple tickers
- `search()` - Search tickers by name or code

### Entities
- `Index` - Market index (TOPIX, Nikkei 225)
- `Market` - Market utilities (calendar, sectors)

### Models & Enums
- `PriceBar` - OHLCV price data
- `StockInfo` - Stock information
- `Sector` - Industry sector
- `MarketSegment` - TSE_PRIME, TSE_STANDARD, TSE_GROWTH, OTHER

### Session & Exceptions
- `Session` - HTTP session with authentication
- `PyJQuantsError` - Base exception
- `AuthenticationError` - Auth failures
- `APIError` - API errors
- `RateLimitError` - Rate limit exceeded
- `NotFoundError` - Resource not found
- `ValidationError` - Validation errors
- `ConfigurationError` - Configuration errors

