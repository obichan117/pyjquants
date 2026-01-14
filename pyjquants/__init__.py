"""
PyJQuants - yfinance-style Python library for J-Quants API (V2).

Usage:
    import pyjquants as pjq

    # Set JQUANTS_API_KEY environment variable
    ticker = pjq.Ticker("7203")
    ticker.info.name          # "トヨタ自動車"
    df = ticker.history("30d")  # Recent 30 days DataFrame

    # Multi-ticker download
    df = pjq.download(["7203", "6758"], period="1y")

    # Search by name
    tickers = pjq.search("トヨタ")

    # Market indices
    topix = pjq.Index.topix()
    df = topix.history("1y")

    # Market utilities
    market = pjq.Market()
    market.is_trading_day(date(2024, 12, 25))
"""

# Domain entities
from pyjquants.domain import (
    AMPriceBar,
    BreakdownTrade,
    Dividend,
    EarningsAnnouncement,
    FinancialDetails,
    FinancialStatement,
    Futures,
    FuturesPrice,
    Index,
    IndexOptions,
    IndexPrice,
    InvestorTrades,
    MarginAlert,
    MarginInterest,
    Market,
    MarketSegment,
    Options,
    OptionsPrice,
    PriceBar,
    Sector,
    ShortSaleReport,
    ShortSelling,
    StockInfo,
    Ticker,
    TradingCalendarDay,
    download,
    search,
)

# Infrastructure
from pyjquants.infra import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NotFoundError,
    PyJQuantsError,
    RateLimitError,
    Session,
    TierError,
    ValidationError,
)

__version__ = "0.2.2"

__all__ = [
    # Version
    "__version__",
    # Main API (yfinance-style)
    "Ticker",
    "download",
    "search",
    # Entities
    "Index",
    "Market",
    "Futures",
    "Options",
    "IndexOptions",
    # Session
    "Session",
    # Exceptions
    "PyJQuantsError",
    "AuthenticationError",
    "APIError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "ConfigurationError",
    "TierError",
    # Models
    "PriceBar",
    "AMPriceBar",
    "StockInfo",
    "Sector",
    "FinancialStatement",
    "FinancialDetails",
    "Dividend",
    "EarningsAnnouncement",
    "TradingCalendarDay",
    "IndexPrice",
    "MarginInterest",
    "ShortSelling",
    "InvestorTrades",
    "BreakdownTrade",
    "ShortSaleReport",
    "MarginAlert",
    "FuturesPrice",
    "OptionsPrice",
    # Enums
    "MarketSegment",
]
