"""J-Quants API endpoint definitions.

All J-Quants endpoints defined in one place for easy maintenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from pyjquants.domain.models import (
        Dividend,
        EarningsAnnouncement,
        FinancialStatement,
        IndexPrice,
        MarginInterest,
        PriceBar,
        Sector,
        ShortSelling,
        StockInfo,
        TradingCalendarDay,
    )

T = TypeVar("T")


@dataclass(frozen=True)
class Endpoint(Generic[T]):
    """Declarative endpoint definition.

    Attributes:
        path: API endpoint path (e.g., "/prices/daily_quotes")
        response_key: Key in JSON response containing data
        model: Pydantic model class for parsing
        paginated: Whether endpoint uses pagination
    """

    path: str
    response_key: str
    model: type[T]
    paginated: bool = False


# === PRICES ===

DAILY_QUOTES: Endpoint[PriceBar] = Endpoint(
    path="/prices/daily_quotes",
    response_key="daily_quotes",
    model="PriceBar",  # type: ignore[arg-type]
    paginated=True,
)

PRICES_AM: Endpoint[PriceBar] = Endpoint(
    path="/prices/prices_am",
    response_key="prices_am",
    model="PriceBar",  # type: ignore[arg-type]
)


# === COMPANY INFO ===

LISTED_INFO: Endpoint[StockInfo] = Endpoint(
    path="/listed/info",
    response_key="info",
    model="StockInfo",  # type: ignore[arg-type]
    paginated=True,
)


# === FINANCIALS ===

STATEMENTS: Endpoint[FinancialStatement] = Endpoint(
    path="/fins/statements",
    response_key="statements",
    model="FinancialStatement",  # type: ignore[arg-type]
    paginated=True,
)

DIVIDENDS: Endpoint[Dividend] = Endpoint(
    path="/fins/dividend",
    response_key="dividend",
    model="Dividend",  # type: ignore[arg-type]
    paginated=True,
)

EARNINGS_CALENDAR: Endpoint[EarningsAnnouncement] = Endpoint(
    path="/fins/announcement",
    response_key="announcement",
    model="EarningsAnnouncement",  # type: ignore[arg-type]
    paginated=True,
)


# === MARKET DATA ===

TRADING_CALENDAR: Endpoint[TradingCalendarDay] = Endpoint(
    path="/markets/trading_calendar",
    response_key="trading_calendar",
    model="TradingCalendarDay",  # type: ignore[arg-type]
)

SECTORS_17: Endpoint[Sector] = Endpoint(
    path="/markets/sectors/topix17",
    response_key="sectors_topix17",
    model="Sector",  # type: ignore[arg-type]
)

SECTORS_33: Endpoint[Sector] = Endpoint(
    path="/markets/sectors/topix33",
    response_key="sectors_topix33",
    model="Sector",  # type: ignore[arg-type]
)

SHORT_SELLING: Endpoint[ShortSelling] = Endpoint(
    path="/markets/short_selling",
    response_key="short_selling",
    model="ShortSelling",  # type: ignore[arg-type]
    paginated=True,
)

MARGIN_INTEREST: Endpoint[MarginInterest] = Endpoint(
    path="/markets/weekly_margin_interest",
    response_key="weekly_margin_interest",
    model="MarginInterest",  # type: ignore[arg-type]
    paginated=True,
)


# === INDEX ===

INDEX_PRICES: Endpoint[IndexPrice] = Endpoint(
    path="/indices",
    response_key="indices",
    model="IndexPrice",  # type: ignore[arg-type]
    paginated=True,
)

TOPIX: Endpoint[IndexPrice] = Endpoint(
    path="/indices/topix",
    response_key="topix",
    model="IndexPrice",  # type: ignore[arg-type]
    paginated=True,
)


# === ENDPOINT REGISTRY ===

ALL_ENDPOINTS = {
    "daily_quotes": DAILY_QUOTES,
    "prices_am": PRICES_AM,
    "listed_info": LISTED_INFO,
    "statements": STATEMENTS,
    "dividends": DIVIDENDS,
    "earnings_calendar": EARNINGS_CALENDAR,
    "trading_calendar": TRADING_CALENDAR,
    "sectors_17": SECTORS_17,
    "sectors_33": SECTORS_33,
    "short_selling": SHORT_SELLING,
    "margin_interest": MARGIN_INTEREST,
    "index_prices": INDEX_PRICES,
    "topix": TOPIX,
}
