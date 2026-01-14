"""Pytest configuration and fixtures."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any
from unittest.mock import MagicMock

import pytest

from pyjquants.domain.models import PriceBar, StockInfo
from pyjquants.infra.session import Session


@pytest.fixture
def mock_session() -> MagicMock:
    """Create a mock session for testing."""
    session = MagicMock(spec=Session)
    session.get.return_value = {}
    session.get_paginated.return_value = iter([])
    return session


@pytest.fixture
def sample_price_bar() -> PriceBar:
    """Create a sample PriceBar for testing."""
    return PriceBar(
        date=datetime.date(2024, 1, 15),
        open=Decimal("2500.0"),
        high=Decimal("2550.0"),
        low=Decimal("2480.0"),
        close=Decimal("2530.0"),
        volume=1000000,
        adjustment_factor=Decimal("1.0"),
    )


@pytest.fixture
def sample_price_data() -> list[dict[str, Any]]:
    """Sample price data as returned by V2 API (abbreviated field names)."""
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


@pytest.fixture
def sample_stock_info_data() -> dict[str, Any]:
    """Sample stock info as returned by API."""
    return {
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


@pytest.fixture
def sample_stock_info(sample_stock_info_data: dict[str, Any]) -> StockInfo:
    """Create a sample StockInfo for testing."""
    return StockInfo.model_validate(sample_stock_info_data)
