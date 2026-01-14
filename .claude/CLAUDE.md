# PyJQuants

yfinance-style Python library for J-Quants API V2 (Japanese stock market data).

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
├── __init__.py       # Public API exports (version 0.2.0)
├── py.typed          # PEP 561 marker
├── domain/           # Business logic
│   ├── ticker.py         # Ticker class + download() + search()
│   ├── index.py          # Index class with .history()
│   ├── market.py         # Market utilities (calendar, sectors, breakdown, short positions)
│   ├── futures.py        # Futures class with .history()
│   ├── options.py        # Options + IndexOptions classes with .history()
│   ├── info.py           # TickerInfo dataclass
│   ├── utils.py          # Shared utilities (parse_period, parse_date)
│   └── models/           # Pydantic models (split by domain)
│       ├── __init__.py       # Re-exports all models
│       ├── base.py           # BaseModel, MarketSegment enum
│       ├── price.py          # PriceBar, IndexPrice
│       ├── company.py        # StockInfo, Sector
│       ├── financial.py      # FinancialStatement, FinancialDetails, Dividend, EarningsAnnouncement
│       ├── market.py         # TradingCalendarDay, MarginInterest, ShortSelling, InvestorTrades, BreakdownTrade, ShortSaleReport, MarginAlert
│       └── derivatives.py    # FuturesPrice, OptionsPrice
├── infra/            # Infrastructure layer
│   ├── session.py        # HTTP session with API key auth (V2)
│   ├── client.py         # Generic fetch/parse client
│   ├── config.py         # Configuration
│   ├── cache.py          # Caching utilities
│   └── exceptions.py     # Exception hierarchy
└── adapters/         # API layer
    └── endpoints.py      # Declarative endpoint definitions (20 V2 endpoints)
```

## Public API (yfinance-style)

```python
import pyjquants as pjq

# Single ticker
ticker = pjq.Ticker('7203')
ticker.info.name          # "トヨタ自動車"
df = ticker.history('30d')
df = ticker.history_am('30d')  # Morning session prices
df = ticker.financials        # Financial statements
df = ticker.financial_details # Detailed BS/PL/CF
df = ticker.dividends         # Dividend history
df = ticker.investor_trades   # Trading by investor type

# Multi-ticker download
df = pjq.download(['7203', '6758'], period='1y')

# Search
tickers = pjq.search('トヨタ')

# Market indices
topix = pjq.Index.topix()
nikkei = pjq.Index.nikkei225()
df = topix.history('1y')

# Market utilities
market = pjq.Market()
market.is_trading_day(date(2024, 12, 25))
df = market.breakdown('7203')      # Trade breakdown by type
df = market.short_positions()      # Outstanding short positions
df = market.margin_alerts()        # Margin trading alerts

# Derivatives (V2 endpoints)
futures = pjq.Futures('NK225M')    # Nikkei 225 mini futures
df = futures.history('30d')

options = pjq.Options('NK225C25000')
df = options.history('30d')

idx_opts = pjq.IndexOptions.nikkei225()
df = idx_opts.history('30d')
```

## Key Files

| File | Purpose |
|------|---------|
| `pyjquants/__init__.py` | Public API exports |
| `pyjquants/domain/ticker.py` | Ticker class with .history(), .history_am(), financials |
| `pyjquants/domain/index.py` | Index class with .history() |
| `pyjquants/domain/market.py` | Market utilities (calendar, sectors, breakdown, short positions) |
| `pyjquants/domain/futures.py` | Futures class with .history() |
| `pyjquants/domain/options.py` | Options + IndexOptions classes |
| `pyjquants/domain/models/` | Pydantic models split by domain |
| `pyjquants/infra/session.py` | API key auth and HTTP handling (V2) |
| `pyjquants/infra/client.py` | Generic fetch/parse |
| `pyjquants/adapters/endpoints.py` | Declarative API endpoints (20 V2 endpoints) |
| `pyproject.toml` | Dependencies and tools config |

## V2 API Endpoints Coverage

All J-Quants V2 endpoints are supported:

**Equities:**
- `/equities/bars/daily` - Daily OHLCV prices
- `/equities/bars/daily/am` - Morning session prices
- `/equities/master` - Listed company info
- `/equities/earnings-calendar` - Earnings announcements
- `/equities/investor-types` - Trading by investor type

**Financials:**
- `/fins/summary` - Financial statements
- `/fins/dividend` - Dividends
- `/fins/details` - Detailed BS/PL/CF

**Markets:**
- `/markets/calendar` - Trading calendar
- `/markets/sectors/topix17` - 17-sector classification
- `/markets/sectors/topix33` - 33-sector classification
- `/markets/short-ratio` - Short selling ratio
- `/markets/margin-interest` - Margin trading interest
- `/markets/breakdown` - Trade breakdown by type
- `/markets/short-sale-report` - Outstanding short positions
- `/markets/margin-alert` - Margin trading alerts

**Indices:**
- `/indices/bars/daily` - Index prices
- `/indices/bars/daily/topix` - TOPIX prices

**Derivatives:**
- `/derivatives/bars/daily/futures` - Futures prices
- `/derivatives/bars/daily/options` - Options prices
- `/derivatives/bars/daily/options/225` - Nikkei 225 index options

## Environment Variables

```bash
JQUANTS_API_KEY=your_api_key  # Get from J-Quants dashboard
# Optional:
JQUANTS_CACHE_ENABLED=true
JQUANTS_CACHE_TTL=3600
JQUANTS_RATE_LIMIT=60  # V2 tiers: Free=5, Light=60, Standard=120, Premium=500
```

## Testing

Tests use mocking - no real API calls (100 tests):
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

## V2 Migration Notes

**V2 API Changes from V1:**
- Simple API key auth via `x-api-key` header (no more token flow)
- All endpoints use unified `data` response key
- Abbreviated field names in responses (O, H, L, C, Vo, Va, etc.)
- Rate limits vary by tier: Free=5, Light=60, Standard=120, Premium=500 req/min

**What Was Removed (V1 artifacts):**
- Token-based authentication (id_token, refresh_token)
- Paper trading module (`trading/`)
- Old architecture: `entities/`, `repositories/`, `collections/`, `core/`, `models/`, `utils/`
- Outdated notebooks
- Backward compatibility shims for V1
