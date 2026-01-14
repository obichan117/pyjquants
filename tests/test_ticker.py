"""Tests for Ticker class."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pyjquants.domain.ticker import Ticker, download, search
from pyjquants.infra.exceptions import TickerNotFoundError


class TestTicker:
    """Tests for Ticker class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        return session

    @pytest.fixture
    def sample_stock_info_response(self) -> dict[str, Any]:
        """Sample stock info API response (V2 uses 'data' key)."""
        return {
            "data": [
                {
                    "Code": "7203",
                    "CompanyName": "トヨタ自動車",
                    "CompanyNameEnglish": "Toyota Motor Corporation",
                    "Sector17Code": "6",
                    "Sector17CodeName": "自動車・輸送機",
                    "Sector33Code": "3050",
                    "Sector33CodeName": "輸送用機器",
                    "MarketCode": "0111",
                    "MarketCodeName": "プライム",
                    "ScaleCategory": "TOPIX Large70",
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
        """Create a mock session."""
        session = MagicMock()
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


class TestSearch:
    """Tests for search function."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session."""
        session = MagicMock()
        return session

    @pytest.fixture
    def sample_listed_info(self) -> list[dict[str, Any]]:
        """Sample listed info API response."""
        return [
            {
                "Code": "7203",
                "CompanyName": "トヨタ自動車",
                "CompanyNameEnglish": "Toyota Motor Corporation",
                "Sector17Code": "6",
                "Sector17CodeName": "自動車・輸送機",
                "Sector33Code": "3050",
                "Sector33CodeName": "輸送用機器",
                "MarketCode": "0111",
                "MarketCodeName": "プライム",
            },
            {
                "Code": "7201",
                "CompanyName": "日産自動車",
                "CompanyNameEnglish": "Nissan Motor Co., Ltd.",
                "Sector17Code": "6",
                "Sector17CodeName": "自動車・輸送機",
                "Sector33Code": "3050",
                "Sector33CodeName": "輸送用機器",
                "MarketCode": "0111",
                "MarketCodeName": "プライム",
            },
            {
                "Code": "6758",
                "CompanyName": "ソニーグループ",
                "CompanyNameEnglish": "Sony Group Corporation",
                "Sector17Code": "5",
                "Sector17CodeName": "電機・精密",
                "Sector33Code": "3650",
                "Sector33CodeName": "電気機器",
                "MarketCode": "0111",
                "MarketCodeName": "プライム",
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
