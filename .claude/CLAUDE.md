# PyJQuants

OOP Python library for J-Quants API (Japanese stock market data).

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

```
pyjquants/
├── core/           # Session, config, cache, exceptions
│   ├── session.py      # HTTP session with auth
│   ├── async_session.py # Async variant
│   ├── config.py       # TOML/env config loading
│   ├── cache.py        # Disk cache wrapper
│   └── exceptions.py   # Custom exceptions
├── entities/       # High-level OOP interfaces
│   ├── stock.py        # Stock("7203") - lazy-loaded
│   └── index.py        # Index.topix()
├── models/         # Pydantic data models
│   ├── price.py        # PriceBar
│   ├── company.py      # StockInfo, Sector
│   ├── financials.py   # Financial statements
│   ├── market.py       # Market data models
│   └── enums.py        # MarketSegment, OrderSide, etc.
├── repositories/   # API data access layer
│   ├── base.py         # BaseRepository
│   ├── stock.py        # StockRepository
│   ├── company.py      # CompanyRepository
│   ├── market.py       # MarketRepository
│   └── index.py        # IndexRepository
├── collections/    # Multi-entity operations
│   ├── universe.py     # Universe.all().filter_by_market()
│   └── market.py       # Market calendar, sectors
├── trading/        # Paper trading simulation
│   ├── trader.py       # Trader interface
│   ├── order.py        # Order, Execution
│   └── portfolio.py    # Portfolio, Position
└── utils/          # Helpers
    └── date.py         # Date parsing/formatting
```

## Key Design Patterns

- **Lazy Loading**: `Stock.name` fetches on first access, then cached
- **Repository Pattern**: Repositories handle API calls, return typed models
- **Entity Pattern**: Entities (`Stock`, `Index`) provide OOP interface over repositories
- **Session Singleton**: Global session auto-authenticates from env vars

## Key Files

| File | Purpose |
|------|---------|
| `pyjquants/__init__.py` | Public API exports |
| `pyjquants/entities/stock.py` | Main `Stock` class |
| `pyjquants/core/session.py` | Auth and HTTP handling |
| `pyjquants/trading/trader.py` | Paper trading logic |
| `pyproject.toml` | Dependencies and tools config |

## Environment Variables

```bash
JQUANTS_MAIL_ADDRESS=your_email@example.com
JQUANTS_PASSWORD=your_password
# Optional:
JQUANTS_REFRESH_TOKEN=...
JQUANTS_CACHE_ENABLED=true
JQUANTS_CACHE_TTL=3600
```

## Testing

Tests use mocking - no real API calls. Run with:
```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=pyjquants --cov-report=term-missing
```

## Publishing

```bash
uv build
uv run twine upload dist/* -u __token__ -p $PYPI_TOKEN
```
