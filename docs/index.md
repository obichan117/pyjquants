# PyJQuants

[![PyPI](https://img.shields.io/pypi/v/pyjquants.svg)](https://pypi.org/project/pyjquants/)
[![CI](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml/badge.svg)](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Investor-friendly OOP Python library for [J-Quants API](https://jpx.gitbook.io/j-quants-en).**

## Features

- **yfinance-style API**: `Ticker("7203")` with `.history()`, `.info`, `.financials`
- **Lazy-loaded attributes**: Data fetched only when accessed, then cached
- **Auto-authentication**: Reads credentials from environment variables
- **Multi-ticker download**: `pjq.download(["7203", "6758"], period="1y")`
- **Type hints**: Full type annotations with Pydantic models
- **DataFrame integration**: Price data returned as pandas DataFrames

## Quick Example

```python
import pyjquants as pjq

# Create a ticker - data is lazy-loaded from API
ticker = pjq.Ticker("7203")  # Toyota

# Access info (fetched on first access, then cached)
ticker.info.name        # "トヨタ自動車"
ticker.info.sector_33   # "輸送用機器"

# Get price history as DataFrame
df = ticker.history("30d")  # Recent 30 trading days

# Download multiple tickers
df = pjq.download(["7203", "6758"], period="1y")

# Market indices
topix = pjq.Index.topix()
df = topix.history("1y")
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
