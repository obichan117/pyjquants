"""J-Quants API V2 endpoint definitions.

All J-Quants V2 endpoints defined in one place for easy maintenance.
V2 uses unified 'data' response key for all endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from pyjquants.domain.models import (
        AMPriceBar,
        BreakdownTrade,
        Dividend,
        EarningsAnnouncement,
        FinancialDetails,
        FinancialStatement,
        FuturesPrice,
        IndexPrice,
        InvestorTrades,
        MarginAlert,
        MarginInterest,
        OptionsPrice,
        PriceBar,
        Sector,
        ShortSaleReport,
        ShortSelling,
        StockInfo,
        TradingCalendarDay,
    )

T = TypeVar("T")


@dataclass(frozen=True)
class Endpoint(Generic[T]):
    """Declarative endpoint definition.

    Attributes:
        path: API endpoint path (e.g., "/equities/bars/daily")
        response_key: Key in JSON response containing data (V2 uses "data" for all)
        model: Pydantic model class for parsing
        paginated: Whether endpoint uses pagination
    """

    path: str
    response_key: str
    model: type[T]
    paginated: bool = False


# === EQUITIES ===

DAILY_QUOTES: Endpoint[PriceBar] = Endpoint(
    path="/equities/bars/daily",
    response_key="data",
    model="PriceBar",  # type: ignore[arg-type]
    paginated=True,
)

LISTED_INFO: Endpoint[StockInfo] = Endpoint(
    path="/equities/master",
    response_key="data",
    model="StockInfo",  # type: ignore[arg-type]
    paginated=True,
)

EARNINGS_CALENDAR: Endpoint[EarningsAnnouncement] = Endpoint(
    path="/equities/earnings-calendar",
    response_key="data",
    model="EarningsAnnouncement",  # type: ignore[arg-type]
    paginated=True,
)

DAILY_QUOTES_AM: Endpoint[AMPriceBar] = Endpoint(
    path="/equities/bars/daily/am",
    response_key="data",
    model="AMPriceBar",  # type: ignore[arg-type]
)

INVESTOR_TYPES: Endpoint[InvestorTrades] = Endpoint(
    path="/equities/investor-types",
    response_key="data",
    model="InvestorTrades",  # type: ignore[arg-type]
    paginated=True,
)


# === FINANCIALS ===

STATEMENTS: Endpoint[FinancialStatement] = Endpoint(
    path="/fins/summary",
    response_key="data",
    model="FinancialStatement",  # type: ignore[arg-type]
    paginated=True,
)

DIVIDENDS: Endpoint[Dividend] = Endpoint(
    path="/fins/dividend",
    response_key="data",
    model="Dividend",  # type: ignore[arg-type]
    paginated=True,
)

FINANCIAL_DETAILS: Endpoint[FinancialDetails] = Endpoint(
    path="/fins/details",
    response_key="data",
    model="FinancialDetails",  # type: ignore[arg-type]
    paginated=True,
)


# === MARKET DATA ===

TRADING_CALENDAR: Endpoint[TradingCalendarDay] = Endpoint(
    path="/markets/calendar",
    response_key="data",
    model="TradingCalendarDay",  # type: ignore[arg-type]
)

# Note: Sector endpoints require Standard+ tier (return 403 on Free/Light)
SECTORS_17: Endpoint[Sector] = Endpoint(
    path="/markets/sectors/topix17",
    response_key="data",
    model="Sector",  # type: ignore[arg-type]
)

SECTORS_33: Endpoint[Sector] = Endpoint(
    path="/markets/sectors/topix33",
    response_key="data",
    model="Sector",  # type: ignore[arg-type]
)

SHORT_SELLING: Endpoint[ShortSelling] = Endpoint(
    path="/markets/short-ratio",
    response_key="data",
    model="ShortSelling",  # type: ignore[arg-type]
    paginated=True,
)

MARGIN_INTEREST: Endpoint[MarginInterest] = Endpoint(
    path="/markets/margin-interest",
    response_key="data",
    model="MarginInterest",  # type: ignore[arg-type]
    paginated=True,
)

BREAKDOWN: Endpoint[BreakdownTrade] = Endpoint(
    path="/markets/breakdown",
    response_key="data",
    model="BreakdownTrade",  # type: ignore[arg-type]
    paginated=True,
)

SHORT_SALE_REPORT: Endpoint[ShortSaleReport] = Endpoint(
    path="/markets/short-sale-report",
    response_key="data",
    model="ShortSaleReport",  # type: ignore[arg-type]
    paginated=True,
)

MARGIN_ALERT: Endpoint[MarginAlert] = Endpoint(
    path="/markets/margin-alert",
    response_key="data",
    model="MarginAlert",  # type: ignore[arg-type]
    paginated=True,
)


# === INDICES ===

INDEX_PRICES: Endpoint[IndexPrice] = Endpoint(
    path="/indices/bars/daily",
    response_key="data",
    model="IndexPrice",  # type: ignore[arg-type]
    paginated=True,
)

TOPIX: Endpoint[IndexPrice] = Endpoint(
    path="/indices/bars/daily/topix",
    response_key="data",
    model="IndexPrice",  # type: ignore[arg-type]
    paginated=True,
)


# === DERIVATIVES ===

FUTURES: Endpoint[FuturesPrice] = Endpoint(
    path="/derivatives/bars/daily/futures",
    response_key="data",
    model="FuturesPrice",  # type: ignore[arg-type]
    paginated=True,
)

OPTIONS: Endpoint[OptionsPrice] = Endpoint(
    path="/derivatives/bars/daily/options",
    response_key="data",
    model="OptionsPrice",  # type: ignore[arg-type]
    paginated=True,
)

INDEX_OPTIONS: Endpoint[OptionsPrice] = Endpoint(
    path="/derivatives/bars/daily/options/225",
    response_key="data",
    model="OptionsPrice",  # type: ignore[arg-type]
    paginated=True,
)
