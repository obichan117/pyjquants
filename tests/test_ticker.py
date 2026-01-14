"""Tests for Ticker class."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, PropertyMock, patch

import pandas as pd
import pytest

from pyjquants.domain.ticker import Ticker, download, search
from pyjquants.infra.config import Tier
from pyjquants.infra.exceptions import TickerNotFoundError


class TestTicker:
    """Tests for Ticker class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_stock_info_response(self) -> dict[str, Any]:
        """Sample stock info API response (V2 abbreviated field names)."""
        return {
            "data": [
                {
                    "Code": "7203",
                    "CoName": "トヨタ自動車",
                    "CoNameEn": "Toyota Motor Corporation",
                    "S17": "6",
                    "S17Nm": "自動車・輸送機",
                    "S33": "3050",
                    "S33Nm": "輸送用機器",
                    "Mkt": "0111",
                    "MktNm": "プライム",
                    "ScaleCat": "TOPIX Large70",
                    "Date": "2024-01-15",
                }
            ]
        }

    @pytest.fixture
    def sample_price_response(self) -> list[dict[str, Any]]:
        """Sample price data API response (V2 abbreviated field names)."""
        return [
            {
                "Date": "2024-01-15",
                "O": "2500.0",
                "H": "2550.0",
                "L": "2480.0",
                "C": "2530.0",
                "Vo": 1000000,
                "AdjFactor": "1.0",
            },
            {
                "Date": "2024-01-16",
                "O": "2530.0",
                "H": "2580.0",
                "L": "2520.0",
                "C": "2570.0",
                "Vo": 1200000,
                "AdjFactor": "1.0",
            },
        ]

    def test_ticker_init(self, mock_session: MagicMock) -> None:
        """Test Ticker initialization."""
        ticker = Ticker("7203", session=mock_session)
        assert ticker.code == "7203"

    def test_ticker_repr(self, mock_session: MagicMock) -> None:
        """Test Ticker string representation."""
        ticker = Ticker("7203", session=mock_session)
        assert repr(ticker) == "Ticker('7203')"

    def test_ticker_info(
        self, mock_session: MagicMock, sample_stock_info_response: dict[str, Any]
    ) -> None:
        """Test Ticker.info property loads and caches data."""
        mock_session.get.return_value = sample_stock_info_response
        mock_session.get_paginated.return_value = iter(sample_stock_info_response["data"])

        ticker = Ticker("7203", session=mock_session)
        info = ticker.info

        assert info.code == "7203"
        assert info.name == "トヨタ自動車"
        assert info.name_english == "Toyota Motor Corporation"
        assert info.sector == "輸送用機器"
        assert info.market == "Prime"

        # Should be cached - accessing again shouldn't make another API call
        info2 = ticker.info
        assert info2 is info

    def test_ticker_info_not_found(self, mock_session: MagicMock) -> None:
        """Test Ticker.info raises error for unknown ticker."""
        mock_session.get.return_value = {"data": []}
        mock_session.get_paginated.return_value = iter([])

        ticker = Ticker("9999", session=mock_session)

        with pytest.raises(TickerNotFoundError) as exc_info:
            _ = ticker.info

        assert exc_info.value.code == "9999"

    def test_ticker_history(
        self, mock_session: MagicMock, sample_price_response: list[dict[str, Any]]
    ) -> None:
        """Test Ticker.history returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_price_response)

        ticker = Ticker("7203", session=mock_session)
        df = ticker.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "date" in df.columns
        assert "close" in df.columns

    def test_ticker_history_empty(self, mock_session: MagicMock) -> None:
        """Test Ticker.history returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        ticker = Ticker("7203", session=mock_session)
        df = ticker.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_ticker_history_with_dates(
        self, mock_session: MagicMock, sample_price_response: list[dict[str, Any]]
    ) -> None:
        """Test Ticker.history with explicit start/end dates."""
        mock_session.get_paginated.return_value = iter(sample_price_response)

        ticker = Ticker("7203", session=mock_session)
        df = ticker.history(start="2024-01-01", end="2024-01-31")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_ticker_refresh(
        self, mock_session: MagicMock, sample_stock_info_response: dict[str, Any]
    ) -> None:
        """Test Ticker.refresh clears cache."""
        mock_session.get.return_value = sample_stock_info_response
        mock_session.get_paginated.return_value = iter(sample_stock_info_response["data"])

        ticker = Ticker("7203", session=mock_session)

        # Load info to populate cache
        _ = ticker.info
        assert ticker._info_cache is not None

        # Refresh should clear cache
        ticker.refresh()
        assert ticker._info_cache is None
        assert ticker._ticker_info_cache is None


class TestDownload:
    """Tests for download function."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    def test_download_empty_codes(self, mock_session: MagicMock) -> None:
        """Test download with empty codes list."""
        df = download([], session=mock_session)
        assert df.empty

    def test_download_single_ticker(self, mock_session: MagicMock) -> None:
        """Test download with single ticker."""
        price_data = [
            {
                "Date": "2024-01-15",
                "O": "2500.0",
                "H": "2550.0",
                "L": "2480.0",
                "C": "2530.0",
                "Vo": 1000000,
                "AdjFactor": "1.0",
            }
        ]
        mock_session.get_paginated.return_value = iter(price_data)

        df = download(["7203"], period="30d", session=mock_session)

        assert isinstance(df, pd.DataFrame)
        assert "date" in df.columns
        assert "7203" in df.columns

    def test_download_multiple_tickers(self, mock_session: MagicMock) -> None:
        """Test download with multiple tickers."""
        price_data_7203 = [
            {
                "Date": "2024-01-15",
                "O": "2500.0",
                "H": "2550.0",
                "L": "2480.0",
                "C": "2530.0",
                "Vo": 1000000,
                "AdjFactor": "1.0",
            }
        ]
        price_data_6758 = [
            {
                "Date": "2024-01-15",
                "O": "1200.0",
                "H": "1220.0",
                "L": "1190.0",
                "C": "1210.0",
                "Vo": 500000,
                "AdjFactor": "1.0",
            }
        ]

        # Mock returns different data for each call
        mock_session.get_paginated.side_effect = [
            iter(price_data_7203),
            iter(price_data_6758),
        ]

        df = download(["7203", "6758"], period="30d", session=mock_session)

        assert isinstance(df, pd.DataFrame)
        assert "date" in df.columns
        assert "7203" in df.columns
        assert "6758" in df.columns

    def test_download_sequential(self, mock_session: MagicMock) -> None:
        """Test download with threads=False (sequential mode)."""
        price_data = [
            {
                "Date": "2024-01-15",
                "O": "2500.0",
                "H": "2550.0",
                "L": "2480.0",
                "C": "2530.0",
                "Vo": 1000000,
                "AdjFactor": "1.0",
            }
        ]
        mock_session.get_paginated.return_value = iter(price_data)

        df = download(["7203"], period="30d", session=mock_session, threads=False)

        assert isinstance(df, pd.DataFrame)
        assert "7203" in df.columns

    def test_download_with_thread_count(self, mock_session: MagicMock) -> None:
        """Test download with specific thread count."""
        price_data_7203 = [
            {
                "Date": "2024-01-15",
                "O": "2500.0",
                "H": "2550.0",
                "L": "2480.0",
                "C": "2530.0",
                "Vo": 1000000,
                "AdjFactor": "1.0",
            }
        ]
        price_data_6758 = [
            {
                "Date": "2024-01-15",
                "O": "1200.0",
                "H": "1220.0",
                "L": "1190.0",
                "C": "1210.0",
                "Vo": 500000,
                "AdjFactor": "1.0",
            }
        ]

        mock_session.get_paginated.side_effect = [
            iter(price_data_7203),
            iter(price_data_6758),
        ]

        df = download(["7203", "6758"], period="30d", session=mock_session, threads=2)

        assert isinstance(df, pd.DataFrame)
        assert "7203" in df.columns
        assert "6758" in df.columns


class TestSearch:
    """Tests for search function."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_listed_info(self) -> list[dict[str, Any]]:
        """Sample listed info API response (V2 abbreviated field names)."""
        return [
            {
                "Code": "7203",
                "CoName": "トヨタ自動車",
                "CoNameEn": "Toyota Motor Corporation",
                "S17": "6",
                "S17Nm": "自動車・輸送機",
                "S33": "3050",
                "S33Nm": "輸送用機器",
                "Mkt": "0111",
                "MktNm": "プライム",
            },
            {
                "Code": "7201",
                "CoName": "日産自動車",
                "CoNameEn": "Nissan Motor Co., Ltd.",
                "S17": "6",
                "S17Nm": "自動車・輸送機",
                "S33": "3050",
                "S33Nm": "輸送用機器",
                "Mkt": "0111",
                "MktNm": "プライム",
            },
            {
                "Code": "6758",
                "CoName": "ソニーグループ",
                "CoNameEn": "Sony Group Corporation",
                "S17": "5",
                "S17Nm": "電機・精密",
                "S33": "3650",
                "S33Nm": "電気機器",
                "Mkt": "0111",
                "MktNm": "プライム",
            },
        ]

    def test_search_by_name_japanese(
        self, mock_session: MagicMock, sample_listed_info: list[dict[str, Any]]
    ) -> None:
        """Test search by Japanese company name."""
        mock_session.get_paginated.return_value = iter(sample_listed_info)

        with patch("pyjquants.domain.ticker._get_global_session", return_value=mock_session):
            results = search("トヨタ", session=mock_session)

        assert len(results) == 1
        assert results[0].code == "7203"

    def test_search_by_name_english(
        self, mock_session: MagicMock, sample_listed_info: list[dict[str, Any]]
    ) -> None:
        """Test search by English company name."""
        mock_session.get_paginated.return_value = iter(sample_listed_info)

        with patch("pyjquants.domain.ticker._get_global_session", return_value=mock_session):
            results = search("Toyota", session=mock_session)

        assert len(results) == 1
        assert results[0].code == "7203"

    def test_search_by_code(
        self, mock_session: MagicMock, sample_listed_info: list[dict[str, Any]]
    ) -> None:
        """Test search by stock code."""
        mock_session.get_paginated.return_value = iter(sample_listed_info)

        with patch("pyjquants.domain.ticker._get_global_session", return_value=mock_session):
            results = search("7203", session=mock_session)

        assert len(results) == 1
        assert results[0].code == "7203"

    def test_search_no_results(
        self, mock_session: MagicMock, sample_listed_info: list[dict[str, Any]]
    ) -> None:
        """Test search with no matches."""
        mock_session.get_paginated.return_value = iter(sample_listed_info)

        with patch("pyjquants.domain.ticker._get_global_session", return_value=mock_session):
            results = search("NonExistent", session=mock_session)

        assert len(results) == 0

    def test_search_case_insensitive(
        self, mock_session: MagicMock, sample_listed_info: list[dict[str, Any]]
    ) -> None:
        """Test search is case insensitive."""
        mock_session.get_paginated.return_value = iter(sample_listed_info)

        with patch("pyjquants.domain.ticker._get_global_session", return_value=mock_session):
            results = search("TOYOTA", session=mock_session)

        assert len(results) == 1
        assert results[0].code == "7203"


class TestTickerNewMethods:
    """Tests for new Ticker methods (history_am, financial_details)."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_am_price_response(self) -> list[dict[str, Any]]:
        """Sample AM price data (uses MO, MH, ML, MC for morning session)."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "72030",
                "MO": "2500.0",
                "MH": "2530.0",
                "ML": "2495.0",
                "MC": "2520.0",
                "MVo": 500000,
                "MVa": "1250000000",
            },
        ]

    @pytest.fixture
    def sample_financial_details_response(self) -> list[dict[str, Any]]:
        """Sample financial details data."""
        return [
            {
                "LocalCode": "7203",
                "DisclosedDate": "2024-01-15",
                "TypeOfDocument": "Annual",
                "TotalAssets": "1000000000",
                "NetAssets": "500000000",
                "NetSales": "200000000",
                "OperatingProfit": "50000000",
                "Profit": "30000000",
            },
        ]

    def test_history_am(
        self, mock_session: MagicMock, sample_am_price_response: list[dict[str, Any]]
    ) -> None:
        """Test Ticker.history_am returns AM session prices."""
        # AM endpoint is not paginated, so mock get() instead of get_paginated()
        mock_session.get.return_value = {"data": sample_am_price_response}

        ticker = Ticker("7203", session=mock_session)
        df = ticker.history_am(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "date" in df.columns
        assert "close" in df.columns

    def test_history_am_empty(self, mock_session: MagicMock) -> None:
        """Test Ticker.history_am returns empty DataFrame when no data."""
        mock_session.get.return_value = {"data": []}

        ticker = Ticker("7203", session=mock_session)
        df = ticker.history_am(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_financial_details(
        self, mock_session: MagicMock, sample_financial_details_response: list[dict[str, Any]]
    ) -> None:
        """Test Ticker.financial_details property."""
        mock_session.get_paginated.return_value = iter(sample_financial_details_response)

        ticker = Ticker("7203", session=mock_session)
        df = ticker.financial_details

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "code" in df.columns
        assert "total_assets" in df.columns

    def test_financial_details_empty(self, mock_session: MagicMock) -> None:
        """Test Ticker.financial_details returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        ticker = Ticker("7203", session=mock_session)
        df = ticker.financial_details

        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestTierRestrictions:
    """Tests for tier-restricted methods."""

    @pytest.fixture
    def mock_session_light(self) -> MagicMock:
        """Create a mock session with Light tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.LIGHT)
        return session

    def test_history_am_requires_premium(self, mock_session_light: MagicMock) -> None:
        """Test Ticker.history_am raises TierError for Light tier."""
        from pyjquants.infra.exceptions import TierError

        ticker = Ticker("7203", session=mock_session_light)

        with pytest.raises(TierError) as exc_info:
            ticker.history_am(period="30d")

        assert "history_am" in str(exc_info.value)
        assert "premium" in str(exc_info.value).lower()
        assert "light" in str(exc_info.value).lower()

    def test_dividends_requires_premium(self, mock_session_light: MagicMock) -> None:
        """Test Ticker.dividends raises TierError for Light tier."""
        from pyjquants.infra.exceptions import TierError

        ticker = Ticker("7203", session=mock_session_light)

        with pytest.raises(TierError) as exc_info:
            _ = ticker.dividends

        assert "dividends" in str(exc_info.value)
        assert "premium" in str(exc_info.value).lower()

    def test_financial_details_requires_premium(self, mock_session_light: MagicMock) -> None:
        """Test Ticker.financial_details raises TierError for Light tier."""
        from pyjquants.infra.exceptions import TierError

        ticker = Ticker("7203", session=mock_session_light)

        with pytest.raises(TierError) as exc_info:
            _ = ticker.financial_details

        assert "financial_details" in str(exc_info.value)
        assert "premium" in str(exc_info.value).lower()
