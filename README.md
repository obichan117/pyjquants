# PyJQuants

Investor-friendly OOP Python library for J-Quants API.

## Installation

```bash
pip install pyjquants
```

## Quick Start

```python
import pyjquants as pjq

# Set environment variables:
# JQUANTS_MAIL_ADDRESS=your_email
# JQUANTS_PASSWORD=your_password

# Then use entities directly
stock = pjq.Stock("7203")
print(stock.name)       # Toyota Motor Corporation
print(stock.prices)     # Recent 30 days DataFrame

# Paper trading
trader = pjq.Trader(initial_cash=10_000_000)
trader.buy(stock, 100)
```

## License

MIT
