# Trading

PyJQuants includes a paper trading simulation system for backtesting strategies.

## Overview

| Class | Purpose |
|-------|---------|
| `Trader` | Main interface for placing orders and managing portfolio |
| `Order` | Represents a buy/sell order |
| `Execution` | Record of a filled order |
| `Portfolio` | Manages positions and cash |
| `Position` | Holdings of a single stock |

## Trader

::: pyjquants.trading.trader.Trader
    options:
      show_source: false

### Example

```python
import pyjquants as pjq
from datetime import date

# Initialize with starting cash
trader = pjq.Trader(initial_cash=10_000_000)

# Get stock
stock = pjq.Stock("7203")

# Place orders
order = trader.buy(stock, 100)              # Market buy
order = trader.buy(stock, 100, price=2500)  # Limit buy
order = trader.sell(stock, 50)              # Market sell

# Simulate fills using historical prices
executions = trader.simulate_fills(date(2024, 6, 15))

# Check portfolio
print(f"Cash: {trader.cash}")
print(f"Total value: {trader.portfolio.total_value}")
```

## Order

::: pyjquants.trading.order.Order
    options:
      show_source: false

### Order Types

```python
from pyjquants import Order, OrderSide, OrderType
from decimal import Decimal

# Market orders
order = Order.market_buy(stock, 100)
order = Order.market_sell(stock, 100)

# Limit orders
order = Order.limit_buy(stock, 100, Decimal("2600"))
order = Order.limit_sell(stock, 100, Decimal("2600"))
```

### Order Status

| Status | Description |
|--------|-------------|
| `PENDING` | Waiting to be filled |
| `FILLED` | Fully executed |
| `PARTIALLY_FILLED` | Partially executed |
| `CANCELLED` | Cancelled by user |
| `REJECTED` | Rejected by system |

## Execution

::: pyjquants.trading.order.Execution
    options:
      show_source: false

### Example

```python
# After simulate_fills
for execution in executions:
    print(f"Filled: {execution.quantity} @ {execution.price}")
    print(f"Value: {execution.value}")
```

## Portfolio

::: pyjquants.trading.portfolio.Portfolio
    options:
      show_source: false

### Example

```python
portfolio = trader.portfolio

# Overall metrics
print(f"Total value: {portfolio.total_value}")
print(f"Realized P&L: {portfolio.realized_pnl}")
print(f"Unrealized P&L: {portfolio.unrealized_pnl}")

# Position weights
weights = portfolio.weights
for code, weight in weights.items():
    print(f"{code}: {weight:.2%}")
```

## Position

::: pyjquants.trading.portfolio.Position
    options:
      show_source: false

### Example

```python
# Get position for a stock
position = trader.position(stock)

if position:
    print(f"Quantity: {position.quantity}")
    print(f"Avg cost: {position.average_cost}")
    print(f"Unrealized P&L: {position.unrealized_pnl}")
```

## Complete Example

```python
import pyjquants as pjq
from datetime import date, timedelta

# Setup
trader = pjq.Trader(initial_cash=1_000_000)
stock = pjq.Stock("7203")

# Simple strategy: buy and hold
trader.buy(stock, 100)

# Simulate over time
start = date(2024, 1, 1)
for i in range(30):
    current = start + timedelta(days=i)
    trader.simulate_fills(current)

# Results
print(f"Initial: ¥1,000,000")
print(f"Final: ¥{trader.portfolio.total_value:,.0f}")
print(f"Return: {(trader.portfolio.total_value / 1_000_000 - 1) * 100:.2f}%")
```
