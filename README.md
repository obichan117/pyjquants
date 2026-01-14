# PyJQuants

[![PyPI](https://img.shields.io/pypi/v/pyjquants.svg)](https://pypi.org/project/pyjquants/)
[![CI](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml/badge.svg)](https://github.com/obichan117/pyjquants/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/en/examples/quickstart.ipynb)

> **日本語ドキュメント / Japanese Documentation**
>
> 日本語のドキュメントとチュートリアルは [こちら](https://obichan117.github.io/pyjquants/) をご覧ください。
> Colabで試す: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/examples/quickstart_ja.ipynb)

yfinance-style Python library for [J-Quants API](https://jpx.gitbook.io/j-quants-en) (Japanese stock market data).

**[Documentation (EN)](https://obichan117.github.io/pyjquants/en/)** | **[API Spec](https://obichan117.github.io/pyjquants/en/openapi/)** | **[Quickstart Notebook](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/en/examples/quickstart.ipynb)**

## Features

- **yfinance-style API**: Familiar interface for quantitative analysts
- **Lazy-loaded attributes**: Data fetched on first access, then cached
- **V2 API support**: Simple API key authentication
- **Type hints**: Full type annotations with Pydantic models
- **DataFrame integration**: Price data returned as pandas DataFrames

## Feature Availability by Tier

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

For development:
```bash
pip install pyjquants[dev]
```

## Quick Start

### Setup

Get your API key from the [J-Quants dashboard](https://application.jpx-jquants.com/) and set it:

```bash
export JQUANTS_API_KEY="your_api_key_here"
```

### Basic Usage

```python
import pyjquants as pjq

# Create a ticker - data is lazy-loaded from API
ticker = pjq.Ticker("7203")  # Toyota

# Access info (fetched on first access, then cached)
ticker.info.name            # "トヨタ自動車"
ticker.info.name_english    # "Toyota Motor Corporation"
ticker.info.sector          # "輸送用機器"
ticker.info.market          # "Prime"

# Get price history (yfinance-style)
df = ticker.history("30d")        # Recent 30 days
df = ticker.history("1y")         # Last year
df = ticker.history(start="2024-01-01", end="2024-06-30")  # Custom range

# Financial data
ticker.financials           # Financial statements
ticker.dividends            # Dividend history
```

### Multi-Ticker Download

```python
import pyjquants as pjq

# Download multiple tickers at once
df = pjq.download(["7203", "6758", "9984"], period="30d")
```

### Search

```python
import pyjquants as pjq

# Search by name or code
tickers = pjq.search("トヨタ")
for t in tickers:
    print(f"{t.code}: {t.info.name}")
```

### Market Indices

```python
import pyjquants as pjq

# Get TOPIX index
topix = pjq.Index.topix()
df = topix.history("1y")

# Get Nikkei 225
nikkei = pjq.Index.nikkei225()
df = nikkei.history("30d")
```

### Market Information

```python
import pyjquants as pjq
from datetime import date

market = pjq.Market()

# Check trading days
market.is_trading_day(date(2024, 12, 25))  # False (holiday)
market.next_trading_day(date(2024, 1, 1))  # Next open day

# Sector information
market.sectors_17  # 17-sector classification
market.sectors_33  # 33-sector classification
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `JQUANTS_API_KEY` | Your J-Quants API key (required) |
| `JQUANTS_CACHE_ENABLED` | Enable caching (default: `true`) |
| `JQUANTS_CACHE_TTL` | Cache TTL in seconds (default: `3600`) |
| `JQUANTS_RATE_LIMIT` | Requests per minute (default: `60`) |

**Rate limit tiers:** Free=5, Light=60, Standard=120, Premium=500

### TOML Configuration

Create `~/.jquants/config.toml`:

```toml
[auth]
api_key = "your_api_key_here"

[cache]
enabled = true
ttl_seconds = 3600

[rate_limit]
requests_per_minute = 60
```

## Data Models

### PriceBar

```python
from pyjquants import PriceBar

bar = ticker.history("1d").iloc[0]
bar.date            # datetime.date
bar.open            # Decimal
bar.high            # Decimal
bar.low             # Decimal
bar.close           # Decimal
bar.volume          # int
```

## API Reference

### Main API

| Class/Function | Description |
|----------------|-------------|
| `Ticker(code)` | Stock ticker with `.history()`, `.info`, `.financials` |
| `download(codes, period)` | Download price data for multiple tickers |
| `search(query)` | Search tickers by name or code |
| `Index` | Market index (TOPIX, Nikkei 225) |
| `Market` | Market utilities (calendar, sectors) |

### Models & Enums

| Class | Description |
|-------|-------------|
| `PriceBar` | OHLCV price data |
| `StockInfo` | Stock information |
| `Sector` | Industry sector |
| `MarketSegment` | `TSE_PRIME`, `TSE_STANDARD`, `TSE_GROWTH`, `OTHER` |

## API Endpoint Mapping

PyJQuants provides a Pythonic interface to all J-Quants V2 API endpoints.

**Tier legend:** *(L)* = Light+, *(S)* = Standard+, *(P)* = Premium only

### Equities

| J-Quants API | PyJQuants |
|--------------|-----------|
| `/equities/bars/daily` | `Ticker("7203").history("30d")` |
| `/equities/bars/daily/am` | `Ticker("7203").history_am("30d")` *(P)* |
| `/equities/master` | `Ticker("7203").info` / `search("トヨタ")` |
| `/equities/earnings-calendar` | `Market().earnings_calendar()` |
| `/equities/investor-types` | `Market().investor_trades()` *(L)* |

### Financials

| J-Quants API | PyJQuants |
|--------------|-----------|
| `/fins/summary` | `Ticker("7203").financials` |
| `/fins/dividend` | `Ticker("7203").dividends` *(P)* |
| `/fins/details` | `Ticker("7203").financial_details` *(P)* |

### Markets

| J-Quants API | PyJQuants |
|--------------|-----------|
| `/markets/calendar` | `Market().is_trading_day(date)` / `trading_days(start, end)` |
| `/markets/margin-interest` | `Market().margin_interest()` *(S)* |
| `/markets/sectors/topix17` | `Market().sectors_17` *(S)* |
| `/markets/sectors/topix33` | `Market().sectors_33` *(S)* |
| `/markets/short-ratio` | `Market().short_ratio()` *(S)* |
| `/markets/breakdown` | `Market().breakdown("7203")` *(P)* |
| `/markets/short-sale-report` | `Market().short_positions()` *(S)* |
| `/markets/margin-alert` | `Market().margin_alerts()` *(S)* |

### Indices

| J-Quants API | PyJQuants |
|--------------|-----------|
| `/indices/bars/daily/topix` | `Index.topix().history("30d")` *(L)* |
| `/indices/bars/daily` | `Index.nikkei225().history("30d")` *(S)* |

### Derivatives

| J-Quants API | PyJQuants |
|--------------|-----------|
| `/derivatives/bars/daily/futures` | `Futures("NK225M").history("30d")` *(P)* |
| `/derivatives/bars/daily/options` | `Options("NK225C25000").history("30d")` *(P)* |
| `/derivatives/bars/daily/options/225` | `IndexOptions.nikkei225().history("30d")` *(S)* |

## Rate Limits by Tier

J-Quants V2 API has different rate limits based on subscription tier:

| Tier | Requests/min | Monthly Fee | Best For |
|------|-------------|-------------|----------|
| **Free** | 5 | ¥0 | Testing, learning |
| **Light** | 60 | ~¥1,650 | Personal projects |
| **Standard** | 120 | ~¥3,300 | Active trading |
| **Premium** | 500 | ~¥16,500 | Production systems |

Configure your rate limit in environment:
```bash
export JQUANTS_RATE_LIMIT=60  # Match your tier
```

## Architecture

PyJQuants follows a Clean Domain-Driven Design:

```
pyjquants/
├── domain/       # Business logic (Ticker, Index, Market, Futures, Options, models)
├── infra/        # Infrastructure (Session, Cache, Config)
└── adapters/     # API layer (endpoint definitions)
```

See the [Architecture documentation](https://obichan117.github.io/pyjquants/en/architecture/) for details.

## Development

```bash
# Clone repository
git clone https://github.com/obichan117/pyjquants.git
cd pyjquants

# Install with uv
uv sync --all-extras

# Run tests
uv run pytest tests/ -v

# Type checking
uv run mypy pyjquants/

# Linting
uv run ruff check pyjquants/

# Build documentation
uv run mkdocs build --strict

# Serve documentation locally
uv run mkdocs serve
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Documentation (日本語)](https://obichan117.github.io/pyjquants/) - Japanese documentation (default)
- [Documentation (English)](https://obichan117.github.io/pyjquants/en/) - English documentation
- [J-Quants API Spec (OpenAPI)](https://obichan117.github.io/pyjquants/en/openapi/) - Unofficial OpenAPI 3.0 spec for J-Quants V2
- [Quickstart Notebook (日本語)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/examples/quickstart_ja.ipynb)
- [Quickstart Notebook (English)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/en/examples/quickstart.ipynb)
- [J-Quants Official](https://jpx-jquants.com/) - Official J-Quants site
- [GitHub Repository](https://github.com/obichan117/pyjquants)
