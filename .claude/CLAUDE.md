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
├── __init__.py       # Public API exports (version 0.2.2)
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
    └── endpoints.py      # Declarative endpoint definitions (21 V2 endpoints)
```

## Public API (yfinance-style)

```python
import pyjquants as pjq

# Single ticker
ticker = pjq.Ticker('7203')
ticker.info.name          # "トヨタ自動車"
df = ticker.history('30d')
df = ticker.history_am('30d')  # Morning session prices (Standard+)
df = ticker.financials        # Financial statements
df = ticker.financial_details # Detailed BS/PL/CF (Standard+)
df = ticker.dividends         # Dividend history (Standard+)

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
market.sectors_17             # TOPIX-17 sectors (Standard+, returns [] on lower tiers)
market.sectors_33             # TOPIX-33 sectors (Standard+, returns [] on lower tiers)
df = market.investor_trades() # Market-wide trading by investor type
df = market.breakdown('7203') # Trade breakdown by type (Standard+)
df = market.short_positions() # Outstanding short positions (Standard+)
df = market.margin_alerts()   # Margin trading alerts (Standard+)
df = market.earnings_calendar()  # Earnings announcements
df = market.short_ratio()     # Short selling ratio (Standard+)
df = market.margin_interest() # Margin trading balances

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
| `pyjquants/adapters/endpoints.py` | Declarative API endpoints (21 V2 endpoints) |
| `pyproject.toml` | Dependencies and tools config |

## V2 API Endpoints Coverage

All J-Quants V2 endpoints are supported. Endpoints marked with *(Standard+)* require Standard tier or higher.

**Equities:**
- `/equities/bars/daily` - Daily OHLCV prices
- `/equities/bars/daily/am` - Morning session prices *(Standard+)*
- `/equities/master` - Listed company info
- `/equities/earnings-calendar` - Earnings announcements
- `/equities/investor-types` - Market-wide trading by investor type (not per-stock)

**Financials:**
- `/fins/summary` - Financial statements
- `/fins/dividend` - Dividends *(Standard+)*
- `/fins/details` - Detailed BS/PL/CF *(Standard+)*

**Markets:**
- `/markets/calendar` - Trading calendar
- `/markets/sectors/topix17` - 17-sector classification *(Standard+)*
- `/markets/sectors/topix33` - 33-sector classification *(Standard+)*
- `/markets/short-ratio` - Short selling ratio *(Standard+)*
- `/markets/margin-interest` - Margin trading interest
- `/markets/breakdown` - Trade breakdown by type *(Standard+)*
- `/markets/short-sale-report` - Outstanding short positions *(Standard+)*
- `/markets/margin-alert` - Margin trading alerts *(Standard+)*

**Indices:**
- `/indices/bars/daily` - Index prices *(Standard+)*
- `/indices/bars/daily/topix` - TOPIX prices

**Derivatives:**
- `/derivatives/bars/daily/futures` - Futures prices *(Standard+)*
- `/derivatives/bars/daily/options` - Options prices *(Standard+)*
- `/derivatives/bars/daily/options/225` - Nikkei 225 index options *(Standard+)*

## Environment Variables

```bash
JQUANTS_API_KEY=your_api_key  # Get from J-Quants dashboard
# Optional:
JQUANTS_CACHE_ENABLED=true
JQUANTS_CACHE_TTL=3600
JQUANTS_RATE_LIMIT=60  # V2 tiers: Free=5, Light=60, Standard=120, Premium=500
```

## Testing

### Unit Tests (mocked, no API key needed)
```bash
uv run pytest                    # Run all unit tests (106 tests)
uv run pytest --cov=pyjquants    # With coverage
```

### Integration Tests (requires real API key)
```bash
# 1. Copy .env.example to .env and add your API key
cp .env.example .env
# Edit .env: JQUANTS_API_KEY=your_key_here

# 2. Run integration tests
uv run pytest tests/integration/ -v                    # All integration tests
uv run pytest tests/integration/ -v -m "not standard_tier"  # Free/Light tier only

# 3. Set tier for Standard+ tests
# Edit .env: JQUANTS_RATE_LIMIT=120  (or 500 for Premium)
uv run pytest tests/integration/ -v                    # Includes Standard+ tests
```

Integration tests validate:
- Correct field names match API responses
- All endpoints work with real data
- Tier restrictions handled properly

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

## Audit Notes (Jan 2026)

**Previous Issues Found and Fixed:**

1. **`investor_trades` moved from Ticker to Market**: The `/equities/investor-types` endpoint returns market-wide aggregate data, not per-stock data. Moved from `Ticker.investor_trades` to `Market.investor_trades()`.

2. **Sectors endpoints require Standard+ tier**: `Market.sectors_17` and `Market.sectors_33` return 403 on Free/Light tiers. Fixed to return empty list gracefully instead of raising an error.

3. **InvestorTrades model missing fields**: API returns many more investor categories (BrkSell, SecCoSell, BusCoSell, OthCoSell, InsCoSell, BankSell, OthFinSell, etc.). Added all missing fields and changed types from `int` to `float`.

4. **Stock codes are 5-digit in API**: J-Quants uses 5-digit codes (e.g., "72030" for Toyota). The library handles this internally.

**Tier Availability**: Many endpoints are restricted to Standard+ tier. The library handles 403 errors gracefully for tier-restricted endpoints like sectors.

**Latest Audit (Jan 14, 2026):**

Documentation inconsistencies fixed:
- `investor_trades` incorrectly documented as `Ticker` property in docs → fixed to `Market().investor_trades()`
- Missing Market methods in API reference (`breakdown`, `short_positions`, `margin_alerts`, `investor_trades`) → added
- Pricing table inconsistency between `getting-started.md` and `api-spec.md` → unified
- `TOPIX` endpoint not exported in `adapters/__init__.py` → added
- Outdated sector endpoint comment ("may not exist") → updated to clarify tier requirement
- Quickstart notebook "Next Steps" section incomplete → expanded with derivatives and more features

**Notebook/README Tier Organization (Jan 14, 2026):**

Reorganized `docs/examples/quickstart.ipynb` and documentation for clear tier separation:
- **Part 1 (Sections 1-6)**: All tiers (Free/Light/Standard/Premium)
  - Setup, Single Ticker, Price History, Multi-Ticker Download
  - Financial Statements, Market Information (TOPIX, calendar, earnings, investor trades, margin interest)
- **Part 2 (Sections 7-12)**: Standard+ tier only
  - Morning Session Prices, Dividends & Detailed Financials
  - Nikkei 225 Index, Sector Classifications
  - Short Selling & Margin Data, Derivatives
- All Standard+ cells wrapped in try/except with tier restriction messages
- README.md updated with "Feature Availability by Tier" matrix
- API endpoint mapping tables updated with tier markers in README and getting-started.md

**Codebase Status**: Clean. All 106 tests pass, docs build with `--strict`.
