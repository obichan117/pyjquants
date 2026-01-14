"""Tests for Market class."""

from __future__ import annotations

import datetime
from typing import Any
from unittest.mock import MagicMock, PropertyMock

import pytest

from pyjquants.domain.market import Market
from pyjquants.infra.config import Tier


class TestMarket:
    """Tests for Market class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_calendar_response(self) -> list[dict[str, Any]]:
        """Sample trading calendar API response (V2 abbreviated field names)."""
        return [
            {"Date": "2024-01-15", "HolDiv": "1"},  # Trading day
            {"Date": "2024-01-16", "HolDiv": "1"},  # Trading day
            {"Date": "2024-01-17", "HolDiv": "0"},  # Holiday
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
        # V2 uses "data" key for all responses
        mock_session.get.return_value = {"data": sample_calendar_response}

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
            "data": [{"Date": "2024-01-15", "HolDiv": "1"}]
        }

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2024, 1, 15))

        assert result is True

    def test_is_trading_day_false(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.is_trading_day returns False for holiday."""
        mock_session.get.return_value = {
            "data": [{"Date": "2024-01-01", "HolDiv": "0"}]
        }

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2024, 1, 1))

        assert result is False

    def test_is_trading_day_not_found(
        self, mock_session: MagicMock
    ) -> None:
        """Test Market.is_trading_day returns False when date not found."""
        mock_session.get.return_value = {"data": []}

        market = Market(session=mock_session)
        result = market.is_trading_day(datetime.date(2099, 1, 1))

        assert result is False

    def test_trading_days(
        self, mock_session: MagicMock, sample_calendar_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.trading_days returns list of trading days."""
        mock_session.get.return_value = {"data": sample_calendar_response}

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
            {"data": [{"Date": "2024-01-14", "HolDiv": "0"}]},
            {"data": [{"Date": "2024-01-15", "HolDiv": "1"}]},
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
            {"data": [{"Date": "2024-01-14", "HolDiv": "0"}]},
            {"data": [{"Date": "2024-01-13", "HolDiv": "1"}]},
        ]

        market = Market(session=mock_session)
        result = market.prev_trading_day(datetime.date(2024, 1, 15))

        assert result == datetime.date(2024, 1, 13)

    def test_sectors_33(
        self, mock_session: MagicMock, sample_sectors_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.sectors_33 property."""
        mock_session.get.return_value = {"data": sample_sectors_response}

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
        mock_session.get.return_value = {"data": sectors_17_response}

        market = Market(session=mock_session)
        sectors = market.sectors_17

        assert len(sectors) == 2

    def test_sectors_alias(
        self, mock_session: MagicMock, sample_sectors_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.sectors is alias for sectors_33."""
        mock_session.get.return_value = {"data": sample_sectors_response}

        market = Market(session=mock_session)

        # Access sectors (should be same as sectors_33)
        sectors = market.sectors

        assert len(sectors) == 3

    # === MARKET DATA METHODS ===

    @pytest.fixture
    def sample_breakdown_response(self) -> list[dict[str, Any]]:
        """Sample breakdown trading data."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "7203",
                "LongSellVa": "1000000.0",
                "ShrtNoMrgnVa": "500000.0",
                "MrgnSellNewVa": "200000.0",
                "LongBuyVa": "1200000.0",
                "LongSellVo": 10000,
                "ShrtNoMrgnVo": 5000,
            }
        ]

    @pytest.fixture
    def sample_short_report_response(self) -> list[dict[str, Any]]:
        """Sample short sale report data."""
        return [
            {
                "DisclosedDate": "2024-01-15",
                "CalculatedDate": "2024-01-12",
                "Code": "7203",
                "StockName": "トヨタ自動車",
                "ShortSellerName": "Goldman Sachs",
                "ShortPositionsToSharesOutstandingRatio": "0.52",
                "ShortPositionsInSharesNumber": 1000000,
            }
        ]

    @pytest.fixture
    def sample_margin_alert_response(self) -> list[dict[str, Any]]:
        """Sample margin alert data."""
        return [
            {
                "PubDate": "2024-01-15",
                "Code": "7203",
                "AppDate": "2024-01-14",
                "ShrtOut": 500000,
                "ShrtOutChg": 10000,
                "ShrtOutRatio": "1.5",
                "LongOut": 800000,
                "LongOutChg": -5000,
                "SLRatio": "0.625",
            }
        ]

    def test_breakdown(
        self, mock_session: MagicMock, sample_breakdown_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.breakdown returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_breakdown_response)

        market = Market(session=mock_session)
        df = market.breakdown(
            code="7203",
            start=datetime.date(2024, 1, 15),
            end=datetime.date(2024, 1, 15),
        )

        assert len(df) == 1
        assert "code" in df.columns
        assert "long_sell_value" in df.columns
        assert df.iloc[0]["code"] == "7203"

    def test_breakdown_empty(self, mock_session: MagicMock) -> None:
        """Test Market.breakdown returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.breakdown(code="9999")

        assert df.empty

    def test_short_positions(
        self, mock_session: MagicMock, sample_short_report_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.short_positions returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_short_report_response)

        market = Market(session=mock_session)
        df = market.short_positions(code="7203")

        assert len(df) == 1
        assert "code" in df.columns
        assert "short_position_ratio" in df.columns
        assert df.iloc[0]["code"] == "7203"

    def test_short_positions_empty(self, mock_session: MagicMock) -> None:
        """Test Market.short_positions returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.short_positions(code="9999")

        assert df.empty

    def test_margin_alerts(
        self, mock_session: MagicMock, sample_margin_alert_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.margin_alerts returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_margin_alert_response)

        market = Market(session=mock_session)
        df = market.margin_alerts(code="7203")

        assert len(df) == 1
        assert "code" in df.columns
        assert "short_outstanding" in df.columns
        assert df.iloc[0]["code"] == "7203"

    def test_margin_alerts_empty(self, mock_session: MagicMock) -> None:
        """Test Market.margin_alerts returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.margin_alerts(code="9999")

        assert df.empty

    # === INVESTOR TRADES ===

    @pytest.fixture
    def sample_investor_trades_response(self) -> list[dict[str, Any]]:
        """Sample investor trades data."""
        return [
            {
                "PubDate": "2024-01-15",
                "StDate": "2024-01-08",
                "EnDate": "2024-01-12",
                "Section": "TokyoNagoya",
                "PropSell": 1000000.0,
                "PropBuy": 1200000.0,
                "BrkSell": 500000.0,
                "BrkBuy": 600000.0,
                "IndSell": 300000.0,
                "IndBuy": 400000.0,
                "FrgnSell": 2000000.0,
                "FrgnBuy": 2500000.0,
                "TotSell": 3800000.0,
                "TotBuy": 4700000.0,
            },
        ]

    def test_investor_trades(
        self, mock_session: MagicMock, sample_investor_trades_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.investor_trades returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_investor_trades_response)

        market = Market(session=mock_session)
        df = market.investor_trades()

        assert len(df) == 1
        assert "prop_sell" in df.columns
        assert "brk_sell" in df.columns
        assert "frgn_buy" in df.columns

    def test_investor_trades_empty(self, mock_session: MagicMock) -> None:
        """Test Market.investor_trades returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.investor_trades()

        assert df.empty

    # === EARNINGS CALENDAR ===

    @pytest.fixture
    def sample_earnings_calendar_response(self) -> list[dict[str, Any]]:
        """Sample earnings calendar data."""
        return [
            {
                "Code": "7203",
                "CoName": "トヨタ自動車",
                "Date": "2024-02-06",
                "FY": "2024",
                "FQ": "3Q",
                "SectorNm": "輸送用機器",
                "Section": "Prime",
            },
            {
                "Code": "6758",
                "CoName": "ソニーグループ",
                "Date": "2024-02-14",
                "FY": "2024",
                "FQ": "3Q",
                "SectorNm": "電気機器",
                "Section": "Prime",
            },
        ]

    def test_earnings_calendar(
        self, mock_session: MagicMock, sample_earnings_calendar_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.earnings_calendar returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_earnings_calendar_response)

        market = Market(session=mock_session)
        df = market.earnings_calendar(
            start=datetime.date(2024, 2, 1),
            end=datetime.date(2024, 2, 28),
        )

        assert len(df) == 2
        assert "code" in df.columns
        assert "company_name" in df.columns
        assert "announcement_date" in df.columns
        assert df.iloc[0]["code"] == "7203"

    def test_earnings_calendar_empty(self, mock_session: MagicMock) -> None:
        """Test Market.earnings_calendar returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.earnings_calendar()

        assert df.empty

    # === SHORT RATIO ===

    @pytest.fixture
    def sample_short_ratio_response(self) -> list[dict[str, Any]]:
        """Sample short selling ratio data (V2 API field names)."""
        return [
            {
                "Date": "2024-01-15",
                "S33": "3050",
                "SellExShortVa": 1000000000.0,
                "ShrtWithResVa": 300000000.0,
                "ShrtNoResVa": 200000000.0,
            },
            {
                "Date": "2024-01-15",
                "S33": "3650",
                "SellExShortVa": 1500000000.0,
                "ShrtWithResVa": 400000000.0,
                "ShrtNoResVa": 100000000.0,
            },
        ]

    def test_short_ratio(
        self, mock_session: MagicMock, sample_short_ratio_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.short_ratio returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_short_ratio_response)

        market = Market(session=mock_session)
        df = market.short_ratio(
            start=datetime.date(2024, 1, 15),
            end=datetime.date(2024, 1, 15),
        )

        assert len(df) == 2
        assert "date" in df.columns
        assert "sector_33_code" in df.columns
        assert "long_selling_value" in df.columns

    def test_short_ratio_empty(self, mock_session: MagicMock) -> None:
        """Test Market.short_ratio returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.short_ratio()

        assert df.empty

    # === MARGIN INTEREST ===

    @pytest.fixture
    def sample_margin_interest_response(self) -> list[dict[str, Any]]:
        """Sample margin interest data."""
        return [
            {
                "Code": "7203",
                "Date": "2024-01-15",
                "MarginBuyingBalance": 5000000,
                "MarginSellingBalance": 3000000,
            },
            {
                "Code": "6758",
                "Date": "2024-01-15",
                "MarginBuyingBalance": 2000000,
                "MarginSellingBalance": 1500000,
            },
        ]

    def test_margin_interest(
        self, mock_session: MagicMock, sample_margin_interest_response: list[dict[str, Any]]
    ) -> None:
        """Test Market.margin_interest returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_margin_interest_response)

        market = Market(session=mock_session)
        df = market.margin_interest(
            start=datetime.date(2024, 1, 15),
            end=datetime.date(2024, 1, 15),
        )

        assert len(df) == 2
        assert "code" in df.columns
        assert "date" in df.columns
        assert "margin_buying_balance" in df.columns
        assert "margin_selling_balance" in df.columns

    def test_margin_interest_empty(self, mock_session: MagicMock) -> None:
        """Test Market.margin_interest returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        market = Market(session=mock_session)
        df = market.margin_interest()

        assert df.empty
