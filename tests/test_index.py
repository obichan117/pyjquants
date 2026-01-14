"""Tests for Index class."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, PropertyMock, patch

import pandas as pd
import pytest

from pyjquants.domain.index import NIKKEI225_CODE, TOPIX_CODE, Index
from pyjquants.infra.config import Tier


class TestIndex:
    """Tests for Index class."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        session.get.return_value = {}
        session.get_paginated.return_value = iter([])
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    @pytest.fixture
    def sample_index_price_response(self) -> list[dict[str, Any]]:
        """Sample index price API response (V2 abbreviated field names)."""
        return [
            {
                "Date": "2024-01-15",
                "Code": "0000",
                "O": "2500.0",
                "H": "2520.0",
                "L": "2480.0",
                "C": "2510.0",
            },
            {
                "Date": "2024-01-16",
                "Code": "0000",
                "O": "2510.0",
                "H": "2530.0",
                "L": "2500.0",
                "C": "2520.0",
            },
        ]

    def test_index_init(self, mock_session: MagicMock) -> None:
        """Test Index initialization."""
        index = Index(code="0000", name="TOPIX", session=mock_session)
        assert index.code == "0000"
        assert index.name == "TOPIX"

    def test_index_init_known_index(self, mock_session: MagicMock) -> None:
        """Test Index initialization with known index code."""
        index = Index(code=TOPIX_CODE, session=mock_session)
        assert index.code == TOPIX_CODE
        assert index.name == "TOPIX"

    def test_index_repr(self, mock_session: MagicMock) -> None:
        """Test Index string representation."""
        index = Index(code="0000", session=mock_session)
        assert repr(index) == "Index('0000')"

    def test_index_str(self, mock_session: MagicMock) -> None:
        """Test Index str representation."""
        index = Index(code="0000", name="TOPIX", session=mock_session)
        assert str(index) == "TOPIX (0000)"

    def test_index_equality(self, mock_session: MagicMock) -> None:
        """Test Index equality comparison."""
        index1 = Index(code="0000", session=mock_session)
        index2 = Index(code="0000", session=mock_session)
        index3 = Index(code="0001", session=mock_session)

        assert index1 == index2
        assert index1 != index3
        assert index1 == "0000"
        assert index1 != "0001"

    def test_index_hash(self, mock_session: MagicMock) -> None:
        """Test Index can be used in sets."""
        index1 = Index(code="0000", session=mock_session)
        index2 = Index(code="0000", session=mock_session)

        index_set = {index1, index2}
        assert len(index_set) == 1

    def test_index_history(
        self, mock_session: MagicMock, sample_index_price_response: list[dict[str, Any]]
    ) -> None:
        """Test Index.history returns DataFrame."""
        mock_session.get_paginated.return_value = iter(sample_index_price_response)

        index = Index(code=NIKKEI225_CODE, session=mock_session)
        df = index.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "date" in df.columns
        assert "close" in df.columns

    def test_index_history_empty(self, mock_session: MagicMock) -> None:
        """Test Index.history returns empty DataFrame when no data."""
        mock_session.get_paginated.return_value = iter([])

        index = Index(code=TOPIX_CODE, session=mock_session)
        df = index.history(period="30d")

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_index_history_with_dates(
        self, mock_session: MagicMock, sample_index_price_response: list[dict[str, Any]]
    ) -> None:
        """Test Index.history with explicit start/end dates."""
        mock_session.get_paginated.return_value = iter(sample_index_price_response)

        index = Index(code=TOPIX_CODE, session=mock_session)
        df = index.history(start="2024-01-01", end="2024-01-31")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2


class TestIndexFactoryMethods:
    """Tests for Index factory methods."""

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with Standard tier."""
        session = MagicMock()
        type(session).tier = PropertyMock(return_value=Tier.PREMIUM)
        return session

    def test_topix_factory(self, mock_session: MagicMock) -> None:
        """Test Index.topix() factory method."""
        with patch("pyjquants.domain.index._get_global_session", return_value=mock_session):
            index = Index.topix(session=mock_session)

        assert index.code == TOPIX_CODE
        assert index.name == "TOPIX"

    def test_nikkei225_factory(self, mock_session: MagicMock) -> None:
        """Test Index.nikkei225() factory method."""
        with patch("pyjquants.domain.index._get_global_session", return_value=mock_session):
            index = Index.nikkei225(session=mock_session)

        assert index.code == NIKKEI225_CODE
        assert index.name == "Nikkei 225"

    def test_all_factory(self, mock_session: MagicMock) -> None:
        """Test Index.all() factory method."""
        with patch("pyjquants.domain.index._get_global_session", return_value=mock_session):
            indices = Index.all(session=mock_session)

        assert len(indices) == 2
        codes = [i.code for i in indices]
        assert TOPIX_CODE in codes
        assert NIKKEI225_CODE in codes
