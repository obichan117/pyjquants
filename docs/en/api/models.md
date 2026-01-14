# Models & Enums

PyJQuants uses Pydantic models for type safety and validation.

## PriceBar

Represents a single OHLCV price bar.

::: pyjquants.domain.models.PriceBar
    options:
      show_source: false

### Example

```python
ticker = pjq.Ticker("7203")
df = ticker.history("1d")

# Or access raw model data
from pyjquants import PriceBar

bar = PriceBar(
    date=datetime.date(2024, 1, 15),
    open=Decimal("2500"),
    high=Decimal("2550"),
    low=Decimal("2480"),
    close=Decimal("2530"),
    volume=1000000,
)
print(f"Adjusted close: {bar.adjusted_close}")
```

## Sector

Represents an industry sector classification.

::: pyjquants.domain.models.Sector
    options:
      show_source: false

### Example

```python
ticker = pjq.Ticker("7203")

# Access sector via info
print(ticker.info.sector)      # "輸送用機器" (33-sector name)
print(ticker.info.sector_17)   # 17-sector name

# Or use Market for all sectors
market = pjq.Market()
for sector in market.sectors_33:
    print(f"{sector.code}: {sector.name}")
```

## StockInfo

Detailed stock information from the API.

::: pyjquants.domain.models.StockInfo
    options:
      show_source: false

## Enums

### MarketSegment

```python
from pyjquants import MarketSegment

# Available values
MarketSegment.TSE_PRIME     # TSE Prime Market
MarketSegment.TSE_STANDARD  # TSE Standard Market
MarketSegment.TSE_GROWTH    # TSE Growth Market
MarketSegment.TOKYO_PRO     # Tokyo Pro Market
MarketSegment.OTHER         # Other markets

# Convert from market code
segment = MarketSegment.from_code("0111")  # TSE_PRIME
```

## Type Hints

All models are fully typed. Use them for better IDE support:

```python
from pyjquants import Ticker, PriceBar
from pyjquants.domain.models import Sector

def get_latest_close(ticker: Ticker) -> float:
    df = ticker.history("1d")
    if df.empty:
        return 0.0
    return float(df["close"].iloc[-1])

def get_sector_name(ticker: Ticker) -> str:
    return ticker.info.sector
```
