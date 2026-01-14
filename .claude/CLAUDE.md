# PyJQuants

yfinance-style Python library for J-Quants API (Japanese stock market data).

## Quick Start

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Type checking
uv run mypy pyjquants/

# Linting
uv run ruff check pyjquants/

# Build docs
uv run mkdocs build --strict

# Serve docs locally
uv run mkdocs serve
```

## Architecture

Clean Domain-Driven Design with yfinance-style public API:

```
pyjquants/
├── __init__.py       # Public API exports
├── py.typed          # PEP 561 marker
├── domain/           # Business logic
│   ├── ticker.py         # Ticker class + download() + search()
│   ├── index.py          # Index class with .history()
│   ├── market.py         # Market utilities (calendar, sectors)
│   ├── info.py           # TickerInfo dataclass
│   ├── utils.py          # Shared utilities (parse_period, parse_date)
│   └── models/           # Pydantic models (split by domain)
│       ├── __init__.py       # Re-exports all models
│       ├── base.py           # BaseModel, MarketSegment enum
│       ├── price.py          # PriceBar, IndexPrice
│       ├── company.py        # StockInfo, Sector
│       ├── financial.py      # FinancialStatement, Dividend, EarningsAnnouncement
│       └── market.py         # TradingCalendarDay, MarginInterest, ShortSelling
├── infra/            # Infrastructure layer
│   ├── session.py        # HTTP session with auth
│   ├── client.py         # Generic fetch/parse client
│   ├── config.py         # Configuration
│   ├── cache.py          # Caching utilities
│   └── exceptions.py     # Exception hierarchy
└── adapters/         # API layer
    └── endpoints.py      # Declarative endpoint definitions
```

## Public API (yfinance-style)

```python
import pyjquants as pjq

# Single ticker
ticker = pjq.Ticker('7203')
ticker.info.name          # "トヨタ自動車"
df = ticker.history('30d')

# Multi-ticker download
df = pjq.download(['7203', '6758'], period='1y')

# Search
tickers = pjq.search('トヨタ')

# Market indices
topix = pjq.Index.topix()
df = topix.history('1y')

# Market utilities
market = pjq.Market()
market.is_trading_day(date(2024, 12, 25))
```

## Key Files

| File | Purpose |
|------|---------|
| `pyjquants/__init__.py` | Public API exports |
| `pyjquants/domain/ticker.py` | Main Ticker class with .history() |
| `pyjquants/domain/index.py` | Index class with .history() |
| `pyjquants/domain/models/` | Pydantic models split by domain |
| `pyjquants/infra/session.py` | Auth and HTTP handling |
| `pyjquants/infra/client.py` | Generic fetch/parse |
| `pyjquants/adapters/endpoints.py` | Declarative API endpoints |
| `pyproject.toml` | Dependencies and tools config |

## Environment Variables

```bash
JQUANTS_API_KEY=your_api_key  # Get from J-Quants dashboard
# Optional:
JQUANTS_CACHE_ENABLED=true
JQUANTS_CACHE_TTL=3600
JQUANTS_RATE_LIMIT=60  # V2 tiers: Free=5, Light=60, Standard=120, Premium=500
```

## Testing

Tests use mocking - no real API calls:
```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=pyjquants --cov-report=term-missing
```

## Publishing

```bash
uv build
uv run twine upload dist/* -u __token__ -p $PYPI_TOKEN
```

## Examples

- **English quickstart:** `docs/examples/quickstart.ipynb` (Colab-ready with credential helper)
- **Japanese notebooks:** `examples/` (01, 02, 05, 06 - getting started, price data, backtesting, screening)

## What Was Removed

- Paper trading module (`trading/`)
- Old architecture: `entities/`, `repositories/`, `collections/`, `core/`, `models/`, `utils/`
- Outdated notebooks: `03_ペーパートレード.ipynb`, `04_ポートフォリオ分析.ipynb`
