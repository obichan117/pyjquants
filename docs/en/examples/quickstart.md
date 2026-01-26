# PyJQuants Quickstart

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/en/examples/quickstart.ipynb)

This notebook demonstrates the basic usage of PyJQuants - a yfinance-style Python library for [J-Quants API](https://jpx.gitbook.io/j-quants-en).

## Tier Information

J-Quants API has different subscription tiers with varying access levels:

| Tier | Requests/min | Monthly Fee | Best For |
|------|-------------|-------------|----------|
| **Free** | 5 | ¥0 | Testing, learning (12-week delayed data) |
| **Light** | 60 | ~¥1,650 | Personal projects |
| **Standard** | 120 | ~¥3,300 | Active trading |
| **Premium** | 500 | ~¥16,500 | Production systems |

This notebook is organized by tier:

- **Sections 1-5**: Work with **Free/Light** tiers
- **Sections 6-8**: Require **Standard** tier or higher
- **Sections 9-11**: Require **Premium** tier only

## Contents

### Free/Light Tiers
1. [Setup](#1-setup)
2. [Single Ticker](#2-single-ticker)
3. [Price History](#3-price-history)
4. [Multi-Ticker Download](#4-multi-ticker-download)
5. [Financial Statements & Market Info](#5-financial-statements-market-info)

### Standard+ Tier
6. [Standard Tier Features](#6-standard-tier-features)
7. [Morning Session & Detailed Financials](#7-morning-session-detailed-financials-premium)
8. [Trade Breakdown](#8-trade-breakdown-premium)

### Premium Tier Only
9. [Derivatives](#9-derivatives-premium)

---
# Part 1: Free/Light Tiers

The following sections work with **Free and Light subscription tiers**.

(Free tier has 12-week delayed data)

---

## 1. Setup

### Install PyJQuants


```python
# Install/upgrade PyJQuants to latest version
!pip install -q pyjquants --upgrade --no-cache-dir

import pyjquants
print(f'PyJQuants v{pyjquants.__version__} installed')
```

### Configure API Key

You need a J-Quants account. [Sign up here](https://application.jpx-jquants.com/) (free tier available).

Get your API key from the [J-Quants dashboard](https://application.jpx-jquants.com/), then run the cell below.

**Option 1 (Recommended for Colab):** Use Colab's Secrets manager:
1. Click the key icon in the left sidebar
2. Add a secret named `JQUANTS_API_KEY` with your API key
3. Toggle "Notebook access" ON

**Option 2:** Paste your API key directly when prompted below.


```python
import os

# Try multiple sources for API key
api_key = None

# 1. Check environment variable (already set)
if os.environ.get('JQUANTS_API_KEY'):
    api_key = os.environ['JQUANTS_API_KEY']
    print('API key found in environment')

# 2. Try Colab secrets (if running in Colab)
if not api_key:
    try:
        from google.colab import userdata
        api_key = userdata.get('JQUANTS_API_KEY')
        os.environ['JQUANTS_API_KEY'] = api_key
        print('API key loaded from Colab Secrets')
    except:
        pass

# 3. Prompt user to paste API key
if not api_key:
    print('=' * 50)
    print('Paste your J-Quants API key below and press Enter:')
    print('(Get it from: https://application.jpx-jquants.com/)')
    print('=' * 50)
    api_key = input('API Key: ').strip()
    
    if api_key:
        os.environ['JQUANTS_API_KEY'] = api_key
        print('API key set!')
    else:
        print('No API key provided. Please set JQUANTS_API_KEY.')

# Verify
if os.environ.get('JQUANTS_API_KEY'):
    print(f"\nAPI key configured (ends with ...{os.environ['JQUANTS_API_KEY'][-4:]})")
```

### Import the Library


```python
import pyjquants as pjq

print(f'PyJQuants version: {pjq.__version__}')
```

## 2. Single Ticker

Create a `Ticker` object using the stock code. This follows the yfinance API style.


```python
# Create a ticker object (Toyota)
ticker = pjq.Ticker('7203')

# Access stock information (lazy-loaded from API)
print(f'Code: {ticker.info.code}')
print(f'Name: {ticker.info.name}')
print(f'English Name: {ticker.info.name_english}')
print(f'Sector: {ticker.info.sector}')
print(f'Market: {ticker.info.market}')
```

### Search for Tickers


```python
# Search by name
tickers = pjq.search('toyota')
print(f'Found {len(tickers)} tickers matching "toyota":')
for t in tickers[:5]:  # Show first 5
    print(f'  {t.code}: {t.info.name}')
```

## 3. Price History

Use the `.history()` method to get price data, just like yfinance.

### Recent Prices


```python
# Get recent 30 days of price data (default)
df = ticker.history('30d')

print(f'Data points: {len(df)}')
print(f'Columns: {list(df.columns)}')
print()
df[['date', 'open', 'high', 'low', 'close', 'volume']].tail()
```

### Different Time Periods


```python
# Various period formats
df_1y = ticker.history('1y')     # 1 year
df_6mo = ticker.history('6mo')   # 6 months
df_1w = ticker.history('1w')     # 1 week

print(f'1 year: {len(df_1y)} days')
print(f'6 months: {len(df_6mo)} days')
print(f'1 week: {len(df_1w)} days')
```

### Custom Date Range


```python
from datetime import date

# Get prices for a specific date range
df_custom = ticker.history(start='2024-01-01', end='2024-06-30')

# Or using date objects
df_custom = ticker.history(start=date(2024, 1, 1), end=date(2024, 6, 30))

print(f'Custom range: {len(df_custom)} trading days')
df_custom[['date', 'close']].head(10)
```

### Visualize Prices


```python
import matplotlib.pyplot as plt

# Enable Japanese font support in Colab
try:
    import japanize_matplotlib
except ImportError:
    !pip install -q japanize-matplotlib
    import japanize_matplotlib

# Get 1 year of data for visualization
df = ticker.history('1y')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['date'], df['close'], 'b-', linewidth=2)
ax.set_title(f'{ticker.info.name} ({ticker.code}) - Stock Price', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Close Price (JPY)')
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 4. Multi-Ticker Download

Download price data for multiple tickers at once using `pjq.download()`.


```python
# Download close prices for multiple tickers
codes = ['7203', '6758', '7974', '9984']  # Toyota, Sony, Nintendo, SoftBank

df_multi = pjq.download(codes, period='30d')

print(f'Shape: {df_multi.shape}')
df_multi.tail()
```


```python
# Plot multiple stocks
fig, ax = plt.subplots(figsize=(12, 6))

for code in codes:
    ax.plot(df_multi['date'], df_multi[code], label=code, linewidth=2)

ax.set_title('Stock Price Comparison', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Close Price (JPY)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 5. Financial Statements & Market Info

### Financial Statements (Summary)

Access financial statement summaries (available on Free/Light tiers).


```python
# Get financial statements
financials = ticker.financials

print(f'Financial records: {len(financials)}')
if len(financials) > 0:
    # Show recent records
    financials[['disclosure_date', 'type_of_document', 'net_sales', 'operating_profit']].head()
```

### Trading Calendar & Earnings (Free/Light)


```python
from datetime import date

market = pjq.Market()

# Check trading days
test_date = date(2024, 12, 25)  # Christmas
print(f'Is {test_date} a trading day? {market.is_trading_day(test_date)}')

# Get next trading day
new_year = date(2025, 1, 1)
next_day = market.next_trading_day(new_year)
print(f'Next trading day after {new_year}: {next_day}')
```

### Earnings Calendar


```python
# Get earnings announcements for a date range
df_earnings = market.earnings_calendar(
    start=date(2024, 10, 1),
    end=date(2024, 10, 31)
)

print(f'Earnings announcements in Oct 2024: {len(df_earnings)}')
if len(df_earnings) > 0:
    df_earnings[['code', 'company_name', 'announcement_date']].head(10)
```

### Investor Trades (Light+ tier)

Market-wide trading by investor type (requires Light tier or higher).


```python
# Get market-wide trading by investor type (Light+ tier)
try:
    df_investors = market.investor_trades(
        start=date(2024, 1, 1),
        end=date(2024, 3, 31)
    )
    print(f'Investor trade records: {len(df_investors)}')
    if len(df_investors) > 0:
        df_investors.head()
except Exception as e:
    print(f'Error: {e}')
    print('This endpoint requires Light tier or higher.')
```

### TOPIX Index (Light+ tier)


```python
# Get TOPIX index (Light+ tier)
try:
    topix = pjq.Index.topix()
    print(f'Index: {topix.name}')
    
    # Get TOPIX history
    df_topix = topix.history('30d')
    print(f'\nRecent TOPIX prices ({len(df_topix)} records):')
    df_topix[['date', 'close']].tail()
except Exception as e:
    print(f'Error: {e}')
    print('TOPIX requires Light tier or higher.')
```

---
# Part 2: Standard+ Tier

The following sections require **Standard tier or higher**.

If you're on the Free or Light tier, these cells will raise `TierError` or return 403 errors.

---

## 6. Standard Tier Features

### Nikkei 225 Index (Standard+)

While TOPIX is available on Light tier, Nikkei 225 requires Standard+.


```python
# Nikkei 225 index (Standard+ tier)
try:
    nikkei = pjq.Index.nikkei225()
    df_nikkei = nikkei.history('30d')
    print(f'Nikkei 225 data points: {len(df_nikkei)}')
    if len(df_nikkei) > 0:
        print(f'Latest close: {df_nikkei["close"].iloc[-1]:,.0f}')
        df_nikkei[['date', 'close']].tail()
except Exception as e:
    print(f'Error: {e}')
    print('Nikkei 225 requires Standard tier or higher.')
```

### Sector Classifications (Standard+)


```python
# TOPIX-17 and TOPIX-33 sectors (Standard+ tier)
try:
    sectors_17 = market.sectors_17
    if len(sectors_17) > 0:
        print(f'TOPIX-17 sectors: {len(sectors_17)}')
        for s in sectors_17[:5]:
            print(f'  {s.code}: {s.name}')
    
    print()
    
    sectors_33 = market.sectors_33
    if len(sectors_33) > 0:
        print(f'TOPIX-33 sectors: {len(sectors_33)}')
        for s in sectors_33[:5]:
            print(f'  {s.code}: {s.name}')
except Exception as e:
    print(f'Error: {e}')
    print('Sector classifications require Standard tier or higher.')
```

### Margin Interest (Standard+)


```python
# Margin trading interest (Standard+ tier)
try:
    df_margin = market.margin_interest(code='7203')
    print(f'Margin interest records: {len(df_margin)}')
    if len(df_margin) > 0:
        df_margin.head()
except Exception as e:
    print(f'Error: {e}')
    print('Margin interest requires Standard tier or higher.')
```

### Short Selling & Margin Alerts (Standard+)


```python
# Short selling ratio (Standard+ tier)
try:
    df_short = market.short_ratio()
    print(f'Short ratio records: {len(df_short)}')
    if len(df_short) > 0:
        df_short.head()
except Exception as e:
    print(f'Error: {e}')
    print('Short ratio requires Standard tier or higher.')
```


```python
# Outstanding short positions (Standard+ tier)
try:
    df_positions = market.short_positions()
    print(f'Short position records: {len(df_positions)}')
    if len(df_positions) > 0:
        df_positions.head()
except Exception as e:
    print(f'Error: {e}')
    print('Short positions requires Standard tier or higher.')
```


```python
# Margin trading alerts (Standard+ tier)
try:
    df_alerts = market.margin_alerts()
    print(f'Margin alert records: {len(df_alerts)}')
    if len(df_alerts) > 0:
        df_alerts.head()
except Exception as e:
    print(f'Error: {e}')
    print('Margin alerts requires Standard tier or higher.')
```

### Index Options (Standard+)


```python
# Nikkei 225 index options (Standard+ tier)
try:
    idx_opts = pjq.IndexOptions.nikkei225()
    df_idx_opts = idx_opts.history('30d')
    print(f'Index options data points: {len(df_idx_opts)}')
    if len(df_idx_opts) > 0:
        df_idx_opts.head()
except Exception as e:
    print(f'Error: {e}')
    print('Index options requires Standard tier or higher.')
```

---
# Part 3: Premium Tier Only

The following sections require **Premium tier**.

These endpoints have no access on Free, Light, or Standard tiers.

---

## 7. Morning Session & Detailed Financials (Premium)


```python
# Morning session prices (Premium tier only)
try:
    df_am = ticker.history_am('30d')
    print(f'AM session data points: {len(df_am)}')
    if len(df_am) > 0:
        df_am[['date', 'open', 'high', 'low', 'close', 'volume']].tail()
except Exception as e:
    print(f'Error: {e}')
    print('Morning session prices require Premium tier.')
```


```python
# Dividend history (Premium tier only)
try:
    dividends = ticker.dividends
    print(f'Dividend records: {len(dividends)}')
    if len(dividends) > 0:
        dividends.head()
except Exception as e:
    print(f'Error: {e}')
    print('Dividend data requires Premium tier.')
```


```python
# Detailed financials BS/PL/CF (Premium tier only)
try:
    details = ticker.financial_details
    print(f'Financial detail records: {len(details)}')
    if len(details) > 0:
        details.head()
except Exception as e:
    print(f'Error: {e}')
    print('Detailed financials require Premium tier.')
```

## 8. Trade Breakdown (Premium)


```python
# Trade breakdown by type (Premium tier only)
try:
    df_breakdown = market.breakdown('7203')
    print(f'Breakdown records: {len(df_breakdown)}')
    if len(df_breakdown) > 0:
        df_breakdown.head()
except Exception as e:
    print(f'Error: {e}')
    print('Trade breakdown requires Premium tier.')
```

## 9. Derivatives (Premium)

### Futures


```python
# Nikkei 225 mini futures (Premium tier only)
try:
    futures = pjq.Futures('NK225M')
    df_futures = futures.history('30d')
    print(f'Futures data points: {len(df_futures)}')
    if len(df_futures) > 0:
        df_futures.head()
except Exception as e:
    print(f'Error: {e}')
    print('Futures data requires Premium tier.')
```

### Options


```python
# Options (Premium tier only)
try:
    options = pjq.Options('NK225C40000')
    df_options = options.history('30d')
    print(f'Options data points: {len(df_options)}')
    if len(df_options) > 0:
        df_options.head()
except Exception as e:
    print(f'Error: {e}')
    print('Options data requires Premium tier.')
```

---
## Summary

### Feature Availability by Tier

| Feature | Free | Light | Standard | Premium |
|---------|:----:|:-----:|:--------:|:-------:|
| Daily prices | ✓* | ✓ | ✓ | ✓ |
| Stock info & search | ✓* | ✓ | ✓ | ✓ |
| Financial statements (summary) | ✓* | ✓ | ✓ | ✓ |
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

### Resources

- [PyJQuants Documentation](https://obichan117.github.io/pyjquants)
- [GitHub Repository](https://github.com/obichan117/pyjquants)
- [J-Quants API Documentation](https://jpx-jquants.com/en/spec/)
- [J-Quants Pricing](https://jpx-jquants.com/)
