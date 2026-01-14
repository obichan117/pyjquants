# API Reference

This section documents all public classes and functions in PyJQuants.

## Quick Links

| Category | Classes |
|----------|---------|
| [Entities](stock.md) | `Stock`, `Index` |
| [Collections](market.md) | `Market`, `Universe` |
| [Trading](trading.md) | `Trader`, `Order`, `Portfolio`, `Position`, `Execution` |
| [Models](models.md) | `PriceBar`, `Sector`, enums |

## Import Patterns

### Standard Usage

```python
import pyjquants as pjq

stock = pjq.Stock("7203")
trader = pjq.Trader(initial_cash=10_000_000)
```

### Explicit Imports

```python
from pyjquants import Stock, Trader, Market
from pyjquants import MarketSegment, OrderSide, OrderType
```

## All Exports

The following are available from `pyjquants`:

### Entities
- `Stock` - Japanese stock with lazy-loaded data
- `Index` - Market index (TOPIX, etc.)

### Collections
- `Market` - Market utilities (calendar, sectors)
- `Universe` - Filterable collection of stocks

### Trading
- `Trader` - Paper trading interface
- `Order` - Buy/sell order
- `Execution` - Filled order record
- `Portfolio` - Holdings and cash
- `Position` - Single stock holding

### Models & Enums
- `PriceBar` - OHLCV price data
- `Sector` - Industry sector
- `MarketSegment` - TSE_PRIME, TSE_STANDARD, TSE_GROWTH, OTHER
- `OrderSide` - BUY, SELL
- `OrderType` - MARKET, LIMIT
- `OrderStatus` - PENDING, FILLED, PARTIALLY_FILLED, CANCELLED, REJECTED
- `OptionType` - Option type enum

### Session & Exceptions
- `Session` - HTTP session with authentication
- `set_global_session` - Set global session
- `PyJQuantsError` - Base exception
- `AuthenticationError` - Auth failures
- `TokenExpiredError` - Token expiration
- `APIError` - API errors
- `RateLimitError` - Rate limit exceeded
- `NotFoundError` - Resource not found
- `ValidationError` - Validation errors
- `ConfigurationError` - Configuration errors
