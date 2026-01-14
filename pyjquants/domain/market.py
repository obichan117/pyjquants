"""Market utilities for trading calendar and sector information."""

from __future__ import annotations

from datetime import date, timedelta
from functools import cached_property
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import (
    BREAKDOWN,
    EARNINGS_CALENDAR,
    INVESTOR_TYPES,
    MARGIN_ALERT,
    MARGIN_INTEREST,
    SECTORS_17,
    SECTORS_33,
    SHORT_SALE_REPORT,
    SHORT_SELLING,
    TRADING_CALENDAR,
)
from pyjquants.domain.base import DomainEntity
from pyjquants.infra.config import Tier
from pyjquants.infra.decorators import requires_tier

if TYPE_CHECKING:
    from pyjquants.domain.models import Sector, TradingCalendarDay
    from pyjquants.infra.session import Session


class Market(DomainEntity):
    """Market utilities for trading calendar and sector information.

    Example:
        >>> market = Market()
        >>> market.is_trading_day(date(2024, 12, 25))  # False
        >>> market.sectors  # List of sectors
    """

    _MAX_TRADING_DAY_SEARCH = 20  # Cover extended holiday periods (e.g., Golden Week + weekends)

    def __init__(self, session: Session | None = None) -> None:
        """Initialize Market.

        Args:
            session: Optional session (uses global session if not provided)
        """
        super().__init__(session)

    def __repr__(self) -> str:
        return "Market()"

    # === TRADING CALENDAR ===

    def trading_calendar(self, start: date, end: date) -> list[TradingCalendarDay]:
        """Get trading calendar for date range."""
        params = self._client.date_params(start=start, end=end)
        return self._client.fetch_list(TRADING_CALENDAR, params)

    def is_trading_day(self, d: date) -> bool:
        """Check if a date is a trading day."""
        params = self._client.date_params(start=d, end=d)
        days = self._client.fetch_list(TRADING_CALENDAR, params)
        if not days:
            return False
        return days[0].is_trading_day

    def trading_days(self, start: date, end: date) -> list[date]:
        """Get list of trading days in a range."""
        calendar = self.trading_calendar(start, end)
        return [day.date for day in calendar if day.is_trading_day]

    def _find_trading_day(self, from_date: date, direction: int) -> date:
        """Find adjacent trading day in given direction.

        Args:
            from_date: Starting date
            direction: 1 for next, -1 for previous

        Returns:
            The next/previous trading day

        Raises:
            ValueError: If no trading day found within search limit
        """
        check_date = from_date + timedelta(days=direction)
        for _ in range(self._MAX_TRADING_DAY_SEARCH):
            if self.is_trading_day(check_date):
                return check_date
            check_date += timedelta(days=direction)
        raise ValueError(
            f"No trading day found within {self._MAX_TRADING_DAY_SEARCH} days of {from_date}"
        )

    def next_trading_day(self, from_date: date) -> date:
        """Get the next trading day after a given date."""
        return self._find_trading_day(from_date, direction=1)

    def prev_trading_day(self, from_date: date) -> date:
        """Get the previous trading day before a given date."""
        return self._find_trading_day(from_date, direction=-1)

    # === SECTORS ===

    @cached_property
    @requires_tier(Tier.STANDARD)
    def sectors(self) -> list[Sector]:
        """Get 33-sector classification list (alias for sectors_33).

        Requires Standard tier or higher.
        """
        return self._client.fetch_list(SECTORS_33)

    @cached_property
    @requires_tier(Tier.STANDARD)
    def sectors_33(self) -> list[Sector]:
        """Get 33-sector classification list.

        Requires Standard tier or higher.
        """
        return self._client.fetch_list(SECTORS_33)

    @cached_property
    @requires_tier(Tier.STANDARD)
    def sectors_17(self) -> list[Sector]:
        """Get 17-sector classification list.

        Requires Standard tier or higher.
        """
        return self._client.fetch_list(SECTORS_17)

    # === INVESTOR TRADING ===

    def investor_trades(
        self,
        start: date | None = None,
        end: date | None = None,
        section: str | None = None,
    ) -> pd.DataFrame:
        """Get market-wide trading by investor type.

        Returns aggregate trading volumes broken down by investor category:
        - Proprietary (prop_*)
        - Brokers (brk_*)
        - Individual (ind_*)
        - Foreign (frgn_*)
        - Securities companies (sec_co_*)
        - Investment trusts (inv_tr_*)
        - Business corporations (bus_co_*)
        - Insurance companies (ins_co_*)
        - Banks (bank_*)
        - Trust banks (trst_bnk_*)
        - Other financials (oth_fin_*)
        - Total (total_*)

        Args:
            start: Start date (optional)
            end: End date (optional)
            section: Market section filter (optional)

        Returns:
            DataFrame with investor trading data
        """
        params = self._client.date_params(start=start, end=end)
        if section:
            params["section"] = section
        return self._client.fetch_dataframe(INVESTOR_TYPES, params)

    # === MARKET DATA ===

    @requires_tier(Tier.PREMIUM)
    def breakdown(
        self,
        code: str,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get breakdown trading data by trade type.

        Requires Premium tier.

        Contains trading values and volumes categorized by:
        - Long selling/buying
        - Short selling (excluding margin)
        - Margin selling/buying (new and closing)

        Args:
            code: Stock code (e.g., "7203")
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with breakdown trading data
        """
        params = self._client.date_params(code=code, start=start, end=end)
        return self._client.fetch_dataframe(BREAKDOWN, params)

    @requires_tier(Tier.STANDARD)
    def short_positions(
        self,
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get outstanding short selling positions reported.

        Requires Standard tier or higher.

        Contains reported short positions where ratio >= 0.5%.

        Args:
            code: Stock code (optional, returns all if not specified)
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with short position reports
        """
        params = self._client.date_params(code=code, start=start, end=end)
        return self._client.fetch_dataframe(SHORT_SALE_REPORT, params)

    @requires_tier(Tier.STANDARD)
    def margin_alerts(
        self,
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get margin trading daily publication (alert) data.

        Requires Standard tier or higher.

        Contains margin trading outstanding for issues subject to daily publication.

        Args:
            code: Stock code (optional, returns all if not specified)
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with margin alert data
        """
        params = self._client.date_params(code=code, start=start, end=end)
        return self._client.fetch_dataframe(MARGIN_ALERT, params)

    def earnings_calendar(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get earnings announcement calendar.

        Returns scheduled earnings announcements for listed companies.

        Args:
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with earnings calendar data including:
            - code: Stock code
            - company_name: Company name
            - announcement_date: Scheduled announcement date
            - fiscal_year: Fiscal year
            - fiscal_quarter: Fiscal quarter
        """
        params = self._client.date_params(start=start, end=end)
        return self._client.fetch_dataframe(EARNINGS_CALENDAR, params)

    @requires_tier(Tier.STANDARD)
    def short_ratio(
        self,
        sector: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get short selling ratio data by sector.

        Requires Standard tier or higher.

        Returns short selling statistics aggregated by TOPIX-33 sector.

        Args:
            sector: Sector code (optional, returns all sectors if not specified)
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with short selling ratio data including:
            - date: Trading date
            - sector_33_code: TOPIX-33 sector code
            - selling_value: Short selling value
        """
        params = self._client.date_params(start=start, end=end)
        if sector:
            params["sector33code"] = sector
        return self._client.fetch_dataframe(SHORT_SELLING, params)

    @requires_tier(Tier.STANDARD)
    def margin_interest(
        self,
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get margin trading interest (balance) data.

        Requires Standard tier or higher.

        Returns margin buying and selling balances for stocks.

        Args:
            code: Stock code (optional, returns all if not specified)
            start: Start date (optional)
            end: End date (optional)

        Returns:
            DataFrame with margin interest data including:
            - code: Stock code
            - date: Date
            - margin_buying_balance: Outstanding margin buy balance
            - margin_selling_balance: Outstanding margin sell balance
        """
        params = self._client.date_params(code=code, start=start, end=end)
        return self._client.fetch_dataframe(MARGIN_INTEREST, params)
