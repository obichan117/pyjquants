# PyJQuants

[![PyPI](https://img.shields.io/pypi/v/pyjquants.svg)](https://pypi.org/project/pyjquants/)
[![CI](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml/badge.svg)](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Investor-friendly OOP Python library for [J-Quants API](https://jpx.gitbook.io/j-quants-en).**

## Features

- **Intuitive OOP design**: `Stock("7203")` just works
- **Lazy-loaded attributes**: `stock.name`, `stock.prices`, `stock.financials`
- **Auto-authentication**: Reads credentials from environment variables
- **Paper trading simulation**: `Trader`, `Order`, `Portfolio`, `Position`
- **Type hints**: Full type annotations with Pydantic models
- **DataFrame integration**: Price data returned as pandas DataFrames

## Quick Example

```python
import pyjquants as pjq

# Create a stock - data is lazy-loaded from API
stock = pjq.Stock("7203")  # Toyota

# Access attributes (fetched on first access, then cached)
stock.name              # "トヨタ自動車"
stock.sector_33.name    # "輸送用機器"

# Get price data as DataFrame
stock.prices            # Recent 30 trading days

# Paper trading
trader = pjq.Trader(initial_cash=10_000_000)
trader.buy(stock, 100)
```

## Installation

```bash
pip install pyjquants
```

## Next Steps

- [Getting Started](getting-started.md) - Setup and basic usage
- [Architecture](architecture.md) - How the library is designed
- [API Reference](api/index.md) - Full API documentation
- [Quickstart Notebook](examples/quickstart.ipynb) - Interactive tutorial
