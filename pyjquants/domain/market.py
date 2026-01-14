"""Market utilities for trading calendar and sector information."""

from __future__ import annotations

from datetime import date, timedelta
from functools import cached_property
from typing import TYPE_CHECKING

import pandas as pd

from pyjquants.adapters.endpoints import (
    BREAKDOWN,
    MARGIN_ALERT,
    SECTORS_17,
    SECTORS_33,
    SHORT_SALE_REPORT,
    TRADING_CALENDAR,
)
from pyjquants.infra.client import JQuantsClient
from pyjquants.infra.session import _get_global_session

if TYPE_CHECKING:
    from pyjquants.domain.models import Sector, TradingCalendarDay
    from pyjquants.infra.session import Session


class Market:
    """Market utilities for trading calendar and sector information.

    Example:
        >>> market = Market()
        >>> market.is_trading_day(date(2024, 12, 25))  # False
        >>> market.sectors  # List of sectors
    """

    def __init__(self, session: Session | None = None) -> None:
        """Initialize Market.

        Args:
            session: Optional session (uses global session if not provided)
        """
        self._session = session or _get_global_session()
        self._client = JQuantsClient(self._session)

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

    def next_trading_day(self, from_date: date) -> date:
        """Get the next trading day after a given date."""
        check_date = from_date + timedelta(days=1)
        for _ in range(10):
            if self.is_trading_day(check_date):
                return check_date
            check_date += timedelta(days=1)
        return check_date

    def prev_trading_day(self, from_date: date) -> date:
        """Get the previous trading day before a given date."""
        check_date = from_date - timedelta(days=1)
        for _ in range(10):
            if self.is_trading_day(check_date):
                return check_date
            check_date -= timedelta(days=1)
        return check_date

    # === SECTORS ===

    @cached_property
    def sectors(self) -> list[Sector]:
        """Get 33-sector classification list (alias for sectors_33)."""
        return self.sectors_33

    @cached_property
    def sectors_33(self) -> list[Sector]:
        """Get 33-sector classification list."""
        return self._client.fetch_list(SECTORS_33)

    @cached_property
    def sectors_17(self) -> list[Sector]:
        """Get 17-sector classification list."""
        return self._client.fetch_list(SECTORS_17)

    # === MARKET DATA ===

    def breakdown(
        self,
        code: str,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get breakdown trading data by trade type.

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

    def short_positions(
        self,
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get outstanding short selling positions reported.

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

    def margin_alerts(
        self,
        code: str | None = None,
        start: date | None = None,
        end: date | None = None,
    ) -> pd.DataFrame:
        """Get margin trading daily publication (alert) data.

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
