"""Tests for Market class."""

from __future__ import annotations

import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest

from pyjquants.domain.market import Market


class TestMarket:
    """Tests for Market class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        return session

    @pytest.fixture
    def sample_calendar_response(self) -> list[dict[str, Any]]:
        """Sample trading calendar API response."""
        return [
            {"Date": "2024-01-15", "HolidayDivision": "0"},  # Trading day
            {"Date": "2024-01-16", "HolidayDivision": "0"},  # Trading day
            {"Date": "2024-01-17", "HolidayDivision": "1"},  # Holiday
        ]

    @pytest.fixture
    def sample_sectors_response(self) -> list[dict[str, Any]]:
        """Sample sectors API response."""
        return [
            {"code": "0050", "name": "情報通信・サービスその他"},
            {"code": "3050", "name": "輸送用機器"},
            {"code": "3650", "name": "電気機器"},
        ]

    def test_market_init(self, mock_session: MagicMock) -> None:
        """Test Market initialization."""
        market = Market(session=mock_session)
        assert repr(market) == "Market()"

    def test_trading_calendar(
        self, mock_session: MagicMock, sample_calendar_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.trading_calendar returns list of TradingCalendarDay."""
        mock_session.get.return_value = {"trading_calendar": sample_calendar_response}

        market = Market(session=mock_session)
        calendar = market.trading_calendar(
            start=datetime.date(2024, 1, 15),
            end=datetime.date(2024, 1, 17),
        )

        assert len(calendar) == 3
        assert calendar[0].date == datetime.date(2024, 1, 15)
        assert calendar[0].is_trading_day is True
        assert calendar[2].is_holiday is True

    def test_is_trading_day_true(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.is_trading_day returns True for trading day."""
        mock_session.get.return_value = {
            "trading_calendar": [{"Date": "2024-01-15", "HolidayDivision": "0"}]
        }

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2024, 1, 15))

        assert result is True

    def test_is_trading_day_false(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.is_trading_day returns False for holiday."""
        mock_session.get.return_value = {
            "trading_calendar": [{"Date": "2024-01-01", "HolidayDivision": "1"}]
        }

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2024, 1, 1))

        assert result is False

    def test_is_trading_day_not_found(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.is_trading_day returns False when date not found."""
        mock_session.get.return_value = {"trading_calendar": []}

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2099, 1, 1))

        assert result is False

    def test_trading_days(
        self, mock_session: MagicMock, sample_calendar_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.trading_days returns list of trading days."""
        mock_session.get.return_value = {"trading_calendar": sample_calendar_response}

        market = Market(session=mock_session)
        days = market.trading_days(
            start=datetime.date(2024, 1, 15),
            end=datetime.date(2024, 1, 17),
        )

        assert len(days) == 2
        assert datetime.date(2024, 1, 15) in days
        assert datetime.date(2024, 1, 16) in days
        assert datetime.date(2024, 1, 17) not in days  # Holiday

    def test_next_trading_day(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.next_trading_day."""
        # First call returns holiday, second returns trading day
        mock_session.get.side_effect = [
            {"trading_calendar": [{"Date": "2024-01-14", "HolidayDivision": "1"}]},
            {"trading_calendar": [{"Date": "2024-01-15", "HolidayDivision": "0"}]},
        ]

        market = Market(session=mock_session)
        result = market.next_trading_day(datetime.date(2024, 1, 13))

        assert result == datetime.date(2024, 1, 15)

    def test_prev_trading_day(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.prev_trading_day."""
        # First call returns holiday, second returns trading day
        mock_session.get.side_effect = [
            {"trading_calendar": [{"Date": "2024-01-14", "HolidayDivision": "1"}]},
            {"trading_calendar": [{"Date": "2024-01-13", "HolidayDivision": "0"}]},
        ]

        market = Market(session=mock_session)
        result = market.prev_trading_day(datetime.date(2024, 1, 15))

        assert result == datetime.date(2024, 1, 13)

    def test_sectors_33(
        self, mock_session: MagicMock, sample_sectors_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.sectors_33 property."""
        mock_session.get.return_value = {"sectors_topix33": sample_sectors_response}

        market = Market(session=mock_session)
        sectors = market.sectors_33

        assert len(sectors) == 3
        assert sectors[0].code == "0050"
        assert sectors[0].name == "情報通信・サービスその他"

    def test_sectors_17(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.sectors_17 property."""
        sectors_17_response = [
            {"code": "1", "name": "食品"},
            {"code": "2", "name": "エネルギー資源"},
        ]
        mock_session.get.return_value = {"sectors_topix17": sectors_17_response}

        market = Market(session=mock_session)
        sectors = market.sectors_17

        assert len(sectors) == 2

    def test_sectors_alias(
        self, mock_session: MagicMock, sample_sectors_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.sectors is alias for sectors_33."""
        mock_session.get.return_value = {"sectors_topix33": sample_sectors_response}

        market = Market(session=mock_session)

        # Access sectors (should be same as sectors_33)
        sectors = market.sectors

        assert len(sectors) == 3
