"""J-Quants API adapters."""

from pyjquants.adapters.endpoints import (
    DAILY_QUOTES,
    DIVIDENDS,
    EARNINGS_CALENDAR,
    INDEX_PRICES,
    LISTED_INFO,
    MARGIN_INTEREST,
    SECTORS_17,
    SECTORS_33,
    SHORT_SELLING,
    STATEMENTS,
    TRADING_CALENDAR,
    Endpoint,
)

__all__ = [
    "Endpoint",
    "DAILY_QUOTES",
    "LISTED_INFO",
    "STATEMENTS",
    "DIVIDENDS",
    "EARNINGS_CALENDAR",
    "TRADING_CALENDAR",
    "SECTORS_17",
    "SECTORS_33",
    "SHORT_SELLING",
    "MARGIN_INTEREST",
    "INDEX_PRICES",
]
