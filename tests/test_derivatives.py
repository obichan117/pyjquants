"""Tests for Futures, Options, and IndexOptions classes."""

from __future__ import annotations

import datetime
from typing import Any
from unittest.mock import MagicMock, PropertyMock

import pandas as pd
import pytest

from pyjquants.domain.futures import Futures
from pyjquants.domain.options import IndexOptions, Options
from pyjquants.infra.config import Tier


class TestFutures:
    """Tests for Futures class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_futures_response(self) -> list[dict[str, Any]]:
        """Sample futures price data."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "NK225M",
                "ProdCat": "NK225M",
                "CM": "2024-03",
                "O": "35000.0",
                "H": "35500.0",
                "L": "34800.0",
                "C": "35200.0",
                "Vo": 100000,
                "OI": 50000,
                "Va": "3500000000.0",
                "Settle": "35200.0",
                "LTD": "2024-03-08",
                "SQD": "2024-03-08",
            }
        ]

    def test_futures_init(self, mock_session: MagicMock) -> None:
        """Test Futures initialization."""
        futures = Futures("NK225M", session=mock_session)
        assert futures.code == "NK225M"

    def test_futures_repr(self, mock_session: MagicMock) -> None:
        """Test Futures string representation."""
        futures = Futures("NK225M", session=mock_session)
        assert repr(futures) == "Futures('NK225M')"

    def test_futures_equality(self, mock_session: MagicMock) -> None:
        """Test Futures equality."""
        f1 = Futures("NK225M", session=mock_session)
        f2 = Futures("NK225M", session=mock_session)
        f3 = Futures("NK225", session=mock_session)

        assert f1 == f2
        assert f1 != f3
        assert f1 == "NK225M"

    def test_futures_hash(self, mock_session: MagicMock) -> None:
        """Test Futures can be hashed."""
        futures = Futures("NK225M", session=mock_session)
        assert hash(futures) == hash("NK225M")

    def test_futures_history(
        self, mock_session: MagicMock, sample_futures_response: list[dict[str, Any]]
    ) -> None:
        """Test Futures.history returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_futures_response)

        futures = Futures("NK225M", session=mock_session)
        df = futures.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "date" in df.columns
        assert "code" in df.columns
        assert "contract_month" in df.columns

    def test_futures_history_empty(self, mock_session: MagicMock) -> None:
        """Test Futures.history returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        futures = Futures("NK225M", session=mock_session)
        df = futures.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_futures_history_with_dates(
        self, mock_session: MagicMock, sample_futures_response: list[dict[str, Any]]
    ) -> None:
        """Test Futures.history with explicit start/end dates."""
        mock_session.get_paginated.return_value = iter(sample_futures_response)

        futures = Futures("NK225M", session=mock_session)
        df = futures.history(start="2024-01-01", end="2024-01-31")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1


class TestOptions:
    """Tests for Options class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_options_response(self) -> list[dict[str, Any]]:
        """Sample options price data."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "NK225C25000",
                "ProdCat": "NK225",
                "CM": "2024-03",
                "Strike": "35000.0",
                "PCDiv": "2",  # Call
                "O": "500.0",
                "H": "550.0",
                "L": "480.0",
                "C": "520.0",
                "Vo": 5000,
                "OI": 10000,
                "Settle": "520.0",
                "IV": "0.25",
                "LTD": "2024-03-08",
                "SQD": "2024-03-08",
            }
        ]

    def test_options_init(self, mock_session: MagicMock) -> None:
        """Test Options initialization."""
        options = Options("NK225C25000", session=mock_session)
        assert options.code == "NK225C25000"

    def test_options_repr(self, mock_session: MagicMock) -> None:
        """Test Options string representation."""
        options = Options("NK225C25000", session=mock_session)
        assert repr(options) == "Options('NK225C25000')"

    def test_options_equality(self, mock_session: MagicMock) -> None:
        """Test Options equality."""
        o1 = Options("NK225C25000", session=mock_session)
        o2 = Options("NK225C25000", session=mock_session)
        o3 = Options("NK225P25000", session=mock_session)

        assert o1 == o2
        assert o1 != o3
        assert o1 == "NK225C25000"

    def test_options_hash(self, mock_session: MagicMock) -> None:
        """Test Options can be hashed."""
        options = Options("NK225C25000", session=mock_session)
        assert hash(options) == hash("NK225C25000")

    def test_options_history(
        self, mock_session: MagicMock, sample_options_response: list[dict[str, Any]]
    ) -> None:
        """Test Options.history returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_options_response)

        options = Options("NK225C25000", session=mock_session)
        df = options.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "date" in df.columns
        assert "strike_price" in df.columns
        assert "put_call" in df.columns

    def test_options_history_empty(self, mock_session: MagicMock) -> None:
        """Test Options.history returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        options = Options("NK225C25000", session=mock_session)
        df = options.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestIndexOptions:
    """Tests for IndexOptions class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_index_options_response(self) -> list[dict[str, Any]]:
        """Sample index options price data."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "N225C35000",
                "ProdCat": "N225",
                "CM": "2024-03",
                "Strike": "35000.0",
                "PCDiv": "2",  # Call
                "O": "500.0",
                "H": "550.0",
                "L": "480.0",
                "C": "520.0",
                "Vo": 5000,
                "OI": 10000,
                "Settle": "520.0",
                "IV": "0.22",
                "LTD": "2024-03-08",
                "SQD": "2024-03-08",
            }
        ]

    def test_index_options_init(self, mock_session: MagicMock) -> None:
        """Test IndexOptions initialization."""
        idx_opts = IndexOptions(session=mock_session)
        assert repr(idx_opts) == "IndexOptions()"

    def test_index_options_str(self, mock_session: MagicMock) -> None:
        """Test IndexOptions string representation."""
        idx_opts = IndexOptions(session=mock_session)
        assert str(idx_opts) == "Nikkei 225 Index Options"

    def test_index_options_factory(self, mock_session: MagicMock) -> None:
        """Test IndexOptions.nikkei225 factory method."""
        idx_opts = IndexOptions.nikkei225(session=mock_session)
        assert isinstance(idx_opts, IndexOptions)

    def test_index_options_history(
        self, mock_session: MagicMock, sample_index_options_response: list[dict[str, Any]]
    ) -> None:
        """Test IndexOptions.history returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_index_options_response)

        idx_opts = IndexOptions(session=mock_session)
        df = idx_opts.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "date" in df.columns
        assert "strike_price" in df.columns

    def test_index_options_history_empty(self, mock_session: MagicMock) -> None:
        """Test IndexOptions.history returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        idx_opts = IndexOptions(session=mock_session)
        df = idx_opts.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_index_options_history_with_dates(
        self, mock_session: MagicMock, sample_index_options_response: list[dict[str, Any]]
    ) -> None:
        """Test IndexOptions.history with explicit start/end dates."""
        mock_session.get_paginated.return_value = iter(sample_index_options_response)

        idx_opts = IndexOptions(session=mock_session)
        df = idx_opts.history(start="2024-01-01", end="2024-01-31")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
