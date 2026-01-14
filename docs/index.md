# PyJQuants

[![PyPI](https://img.shields.io/pypi/v/pyjquants.svg)](https://pypi.org/project/pyjquants/)
[![CI](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml/badge.svg)](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/examples/quickstart.ipynb)

yfinance-style Python library for [J-Quants API](https://jpx.gitbook.io/j-quants-en) (Japanese stock market data).

## Features

- **yfinance-style API**: Familiar interface for quantitative analysts
- **Lazy-loaded attributes**: Data fetched on first access, then cached
- **V2 API support**: Simple API key authentication
- **Tier-aware**: Fail-fast validation prevents wasted API calls
- **Type hints**: Full type annotations with Pydantic models
- **DataFrame integration**: Price data returned as pandas DataFrames

## Quick Example

```python
import pyjquants as pjq

# Create a ticker - data is lazy-loaded from API
ticker = pjq.Ticker("7203")  # Toyota

# Access info (fetched on first access, then cached)
ticker.info.name        # "トヨタ自動車"
ticker.info.sector      # "輸送用機器"

# Get price history as DataFrame
df = ticker.history("30d")  # Recent 30 trading days

# Download multiple tickers
df = pjq.download(["7203", "6758"], period="1y")

# Market indices
topix = pjq.Index.topix()
df = topix.history("1y")
```

## Feature Availability by Tier

J-Quants offers different subscription tiers with varying feature access:

| Feature | Free | Light | Standard | Premium |
|---------|:----:|:-----:|:--------:|:-------:|
| Daily prices | ✓* | ✓ | ✓ | ✓ |
| Stock info & search | ✓* | ✓ | ✓ | ✓ |
| Financial statements | ✓* | ✓ | ✓ | ✓ |
| Trading calendar | ✓* | ✓ | ✓ | ✓ |
| Earnings calendar | ✓ | ✓ | ✓ | ✓ |
| Investor trades (market-wide) | - | ✓ | ✓ | ✓ |
| TOPIX index | - | ✓ | ✓ | ✓ |
| Nikkei 225 index | - | - | ✓ | ✓ |
| Index options (Nikkei 225) | - | - | ✓ | ✓ |
| Margin interest | - | - | ✓ | ✓ |
| Short selling ratio | - | - | ✓ | ✓ |
| Short positions report | - | - | ✓ | ✓ |
| Margin alerts | - | - | ✓ | ✓ |
| Sector classifications | - | - | ✓ | ✓ |
| Morning session (AM) prices | - | - | - | ✓ |
| Dividends | - | - | - | ✓ |
| Detailed financials (BS/PL/CF) | - | - | - | ✓ |
| Trade breakdown | - | - | - | ✓ |
| Futures | - | - | - | ✓ |
| Options | - | - | - | ✓ |

*Free tier has 12-week delayed data

## Installation

```bash
pip install pyjquants
```

## Next Steps

- [Getting Started](getting-started.md) - Setup and basic usage
- [Architecture](architecture.md) - How the library is designed
- [API Reference](api/index.md) - Full API documentation
- [Quickstart Notebook](examples/quickstart.ipynb) - Interactive tutorial (Colab-ready)
