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
│       ├── price.py          # PriceBar, AMPriceBar, IndexPrice
│       ├── company.py        # StockInfo, Sector
│       ├── financial.py      # FinancialStatement, FinancialDetails, Dividend, EarningsAnnouncement
│       ├── market.py         # TradingCalendarDay, MarginInterest, ShortSelling, InvestorTrades, BreakdownTrade, ShortSaleReport, MarginAlert
│       └── derivatives.py    # FuturesPrice, OptionsPrice
├── infra/            # Infrastructure layer
│   ├── session.py        # HTTP session with API key auth (V2)
│   ├── client.py         # Generic fetch/parse client
│   ├── config.py         # Configuration + Tier enum
│   ├── decorators.py     # @requires_tier decorator
│   ├── cache.py          # Caching utilities
│   └── exceptions.py     # Exception hierarchy + TierError
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
df = ticker.history_am('30d')  # Morning session prices (Premium only)
df = ticker.financials        # Financial statements
df = ticker.financial_details # Detailed BS/PL/CF (Premium only)
df = ticker.dividends         # Dividend history (Premium only)

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
market.sectors_17             # TOPIX-17 sectors (Standard+, raises TierError)
market.sectors_33             # TOPIX-33 sectors (Standard+, raises TierError)
df = market.investor_trades() # Market-wide trading by investor type (Light+)
df = market.breakdown('7203') # Trade breakdown by type (Premium only)
df = market.short_positions() # Outstanding short positions (Standard+)
df = market.margin_alerts()   # Margin trading alerts (Standard+)
df = market.earnings_calendar()  # Earnings announcements
df = market.short_ratio()     # Short selling ratio (Standard+)
df = market.margin_interest() # Margin trading balances (Standard+)

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

All J-Quants V2 endpoints are supported.

**Tier legend:** *(L)* = Light+, *(S)* = Standard+, *(P)* = Premium only

**Equities:**
- `/equities/bars/daily` - Daily OHLCV prices
- `/equities/bars/daily/am` - Morning session prices *(P)*
- `/equities/master` - Listed company info
- `/equities/earnings-calendar` - Earnings announcements
- `/equities/investor-types` - Market-wide trading by investor type *(L)*

**Financials:**
- `/fins/summary` - Financial statements
- `/fins/dividend` - Dividends *(P)*
- `/fins/details` - Detailed BS/PL/CF *(P)*

**Markets:**
- `/markets/calendar` - Trading calendar
- `/markets/sectors/topix17` - 17-sector classification *(S)*
- `/markets/sectors/topix33` - 33-sector classification *(S)*
- `/markets/short-ratio` - Short selling ratio *(S)*
- `/markets/margin-interest` - Margin trading interest *(S)*
- `/markets/breakdown` - Trade breakdown by type *(P)*
- `/markets/short-sale-report` - Outstanding short positions *(S)*
- `/markets/margin-alert` - Margin trading alerts *(S)*

**Indices:**
- `/indices/bars/daily` - Index prices (Nikkei 225) *(S)*
- `/indices/bars/daily/topix` - TOPIX prices *(L)*

**Derivatives:**
- `/derivatives/bars/daily/futures` - Futures prices *(P)*
- `/derivatives/bars/daily/options` - Options prices *(P)*
- `/derivatives/bars/daily/options/225` - Nikkei 225 index options *(S)*

## Environment Variables

```bash
JQUANTS_API_KEY=your_api_key  # Get from J-Quants dashboard
# Optional:
JQUANTS_TIER=light            # free, light, standard, premium (default: light)
JQUANTS_CACHE_ENABLED=true
JQUANTS_CACHE_TTL=3600
# Legacy (backwards compat): JQUANTS_RATE_LIMIT=60 → infers tier from rate limit
```

## Testing

### Unit Tests (mocked, no API key needed)
```bash
uv run pytest                    # Run all unit tests (109 tests)
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
# Edit .env: JQUANTS_TIER=standard  (or premium)
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

## Documentation

The docs support English and Japanese with `mkdocs-static-i18n` plugin.

**English (default):** Technical documentation for developers
```
docs/
├── index.md              # Landing page with tier table
├── getting-started.md    # Setup and basic usage
├── architecture.md       # DDD architecture overview
├── api-spec.md           # J-Quants API mapping
├── api/                  # API reference (mkdocstrings)
└── examples/
    └── quickstart.ipynb  # English Colab notebook
```

**Japanese:** Simplified docs for non-technical Japanese investors
```
docs/ja/
├── index.md              # ホーム（投資家向け紹介）
├── setup.md              # セットアップ（APIキー取得方法）
├── basic-usage.md        # 基本的な使い方（コピペサンプル）
├── tier-guide.md         # プラン別ガイド（料金・機能比較）
└── examples/
    └── quickstart_ja.ipynb  # 日本語クイックスタート
```

**Key differences in Japanese docs:**
- Beginner-friendly explanations (「APIキーとは？」など)
- Step-by-step setup with platform-specific instructions
- Copy-paste ready examples with Japanese comments
- Tier comparison with pricing in yen
- No API reference or architecture docs (link to English)

**Build & serve:**
```bash
uv run mkdocs build --strict   # Build both languages
uv run mkdocs serve            # Preview at localhost:8000
```

**URLs:**
- English: https://obichan117.github.io/pyjquants/
- Japanese: https://obichan117.github.io/pyjquants/ja/

## Tier-Aware Client

The library validates subscription tier **before** making API calls and fails fast with `TierError`:

```python
from pyjquants.infra.exceptions import TierError

# If your tier is Light and you try to use a Standard+ method:
try:
    df = ticker.history_am()  # Requires Standard+
except TierError as e:
    print(e)  # "history_am() requires standard+ tier, but you have light"
```

**Tier Hierarchy:** `FREE < LIGHT < STANDARD < PREMIUM`

**Methods with tier restrictions:**

*Light+ tier:*
- `Market.investor_trades()` - Market-wide trading by investor type
- `Index.topix().history()` - TOPIX index prices

*Standard+ tier:*
- `Market.sectors`, `sectors_17`, `sectors_33` - Sector classifications
- `Market.short_positions()`, `margin_alerts()` - Short/margin alerts
- `Market.short_ratio()`, `margin_interest()` - Short/margin data
- `Index.nikkei225().history()` - Nikkei 225 index
- `IndexOptions.nikkei225().history()` - Nikkei 225 index options

*Premium tier only:*
- `Ticker.history_am()` - Morning session prices
- `Ticker.dividends` - Dividend history
- `Ticker.financial_details` - Detailed BS/PL/CF
- `Market.breakdown()` - Trade breakdown by type
- `Futures.history()` - Futures prices
- `Options.history()` - Options prices

**Implementation:**
- `Tier` enum in `pyjquants/infra/config.py` with comparison operators
- `TierError` exception in `pyjquants/infra/exceptions.py`
- `@requires_tier(Tier.STANDARD)` decorator in `pyjquants/infra/decorators.py`
- `Session.tier` property exposes the configured tier

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

**Integration Tests Added (Jan 14, 2026):**

Integration tests with real API key added in `tests/integration/`:
- Tests require `JQUANTS_API_KEY` in `.env` file
- Free/Light tier tests (10 tests): Ticker, Search, Download, Index (TOPIX), Market
- Standard+ tier tests (13 tests): morning session, dividends, Nikkei 225, sectors, derivatives
- Run with: `uv run pytest tests/integration/ -v -m "not standard_tier"`
- Unit tests exclude integration by default via `addopts = "--ignore=tests/integration/"`

Bugs found and fixed via integration tests:
1. **`TradingCalendarDay.is_trading_day` inverted**: HolDiv "0" = holiday, "1" = trading day (was reversed)
2. **Stock codes are 5-digit**: API returns "72030" for Toyota, not "7203"
3. **`margin_interest` requires Standard+ tier**: Was incorrectly documented as Free/Light

**Codebase Status**: Clean. All 109 unit tests + 10 integration tests pass, docs build with `--strict`.

**Comprehensive API Field Audit (Jan 14, 2026):**

Compared official J-Quants V2 API documentation (https://jpx-jquants.com/en/spec/) against actual API responses and Pydantic models. All inconsistencies found and fixed:

1. **PriceBar model** - Added missing `UL` (upper limit) and `LL` (lower limit) fields

2. **AMPriceBar model** - **CRITICAL BUG FIXED**: Created new model for `/equities/bars/daily/am` endpoint. The AM session API uses different field names (MO, MH, ML, MC, MVo, MVa) than regular daily quotes (O, H, L, C, Vo, Va). Previous code incorrectly used PriceBar model which would fail to parse AM session data.

3. **FinancialStatement model** - Added 79 missing fields to match actual API response (107 total fields):
   - Metadata: DiscNo, NxtFYSt, NxtFYEn
   - Dividends: DivUnit, DivTotalAnn, PayoutRatioAnn, FDiv*, NxFDiv*
   - Forecasts: FSales*, FOP*, FOdP*, FNP*, FEPS*, NxF* (2Q and full year)
   - Non-consolidated: NC* actuals and forecasts
   - Change flags: MatChgSub, SigChgInC, ChgByASRev, ChgNoASRev, ChgAcEst, RetroRst
   - Share data: ShOutFY, TrShFY, AvgSh

4. **ShortSelling model** - Fixed field names to match actual API:
   - `Sector33Code` → `S33`
   - `SellingValue` → `SellExShortVa` (long selling value)
   - Added: `ShrtWithResVa` (short with price restrictions), `ShrtNoResVa` (short without restrictions)

5. **MarginAlert model** - Added missing fields:
   - `PubReason` (publication reason flags)
   - `ShrtNegOutChg`, `ShrtStdOutChg` (short breakdown changes)
   - `LongNegOutChg`, `LongStdOutChg` (long breakdown changes)
   - `TSEMrgnRegCls` (TSE margin regulation classification)

**Tier Corrections:**
- `/markets/margin-interest` - Actually requires Standard+ tier (was incorrectly documented as Free/Light)
- `/markets/short-ratio` - Requires Standard+ tier

**Model Field Validation Status (against actual API):**
- `equities/bars/daily` (PriceBar): ✅ All 16 fields match
- `equities/master` (StockInfo): ✅ All 13 fields match
- `equities/earnings-calendar` (EarningsAnnouncement): ✅ All 7 fields match
- `equities/investor-types` (InvestorTrades): ✅ All 56 fields match
- `fins/summary` (FinancialStatement): ✅ All 107 fields match
- `markets/calendar` (TradingCalendarDay): ✅ All 2 fields match
- `indices/bars/daily/topix` (IndexPrice): ✅ All 5 fields match

**Sources:**
- Official V2 API docs: https://jpx-jquants.com/en/spec/
- Stock Prices: https://jpx-jquants.com/en/spec/eq-bars-daily
- AM Session: https://jpx-jquants.com/en/spec/eq-bars-daily-am
- Indices: https://jpx-jquants.com/en/spec/idx-bars-daily

**Tier-Aware Client Added (Jan 14, 2026):**

Implemented fail-fast tier validation:
- Added `Tier` enum (FREE, LIGHT, STANDARD, PREMIUM) with comparison operators
- Added `TierError` exception for clear error messages
- Added `@requires_tier(Tier.STANDARD)` decorator for tier-restricted methods
- Session exposes `tier` property from config
- Config supports both `JQUANTS_TIER` (explicit) and `JQUANTS_RATE_LIMIT` (backwards compat)
- All tier-restricted methods now raise `TierError` before making API calls if tier is insufficient
- Added 3 new tier restriction tests (109 total tests)
