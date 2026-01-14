"""Integration tests for PyJQuants with real API calls.

These tests verify that the library works correctly with the actual J-Quants API.
They catch issues like:
- Wrong field names in models
- API response format changes
- Tier restrictions

Run all integration tests:
    uv run pytest tests/integration/ -v

Run only Free/Light tier tests:
    uv run pytest tests/integration/ -v -m "not standard_tier"
"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import pytest

import pyjquants as pjq


# =============================================================================
# FREE/LIGHT TIER TESTS (All tiers can run these)
# =============================================================================


class TestTickerIntegration:
    """Integration tests for Ticker class."""

    @pytest.mark.integration
    def test_ticker_info(self, api_key: str) -> None:
        """Test that ticker info loads correctly."""
        ticker = pjq.Ticker("7203")  # Toyota

        # API returns 5-digit codes (e.g., "72030" for Toyota)
        assert ticker.info.code.startswith("7203")
        assert ticker.info.name is not None
        assert len(ticker.info.name) > 0
        assert ticker.info.name_english is not None
        assert ticker.info.sector is not None
        assert ticker.info.market is not None

    @pytest.mark.integration
    def test_ticker_history(self, api_key: str) -> None:
        """Test that price history returns valid DataFrame."""
        ticker = pjq.Ticker("7203")
        df = ticker.history("30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

        # Check required columns exist
        required_cols = ["date", "open", "high", "low", "close", "volume"]
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"

        # Check data types
        assert df["date"].dtype == "object" or pd.api.types.is_datetime64_any_dtype(df["date"])
        assert pd.api.types.is_numeric_dtype(df["close"])

    @pytest.mark.integration
    def test_ticker_financials(self, api_key: str) -> None:
        """Test that financials returns valid DataFrame with correct columns."""
        ticker = pjq.Ticker("7203")
        df = ticker.financials

        assert isinstance(df, pd.DataFrame)
        # May be empty for some tickers, but should have correct structure
        if len(df) > 0:
            # These are the actual field names from FinancialStatement model
            expected_cols = ["disclosure_date", "type_of_document", "net_sales", "operating_profit"]
            for col in expected_cols:
                assert col in df.columns, f"Missing column: {col}"


class TestSearchIntegration:
    """Integration tests for search function."""

    @pytest.mark.integration
    def test_search_by_name(self, api_key: str) -> None:
        """Test search by company name."""
        results = pjq.search("toyota")

        assert len(results) > 0
        assert all(isinstance(t, pjq.Ticker) for t in results)

        # Toyota should be in results (API returns 5-digit codes)
        codes = [t.code for t in results]
        assert any(c.startswith("7203") for c in codes)

    @pytest.mark.integration
    def test_search_by_code(self, api_key: str) -> None:
        """Test search by stock code."""
        results = pjq.search("7203")

        assert len(results) >= 1
        # Ticker.code stores the API-returned code (5-digit)
        assert any(t.code.startswith("7203") for t in results)


class TestDownloadIntegration:
    """Integration tests for download function."""

    @pytest.mark.integration
    def test_download_multiple(self, api_key: str) -> None:
        """Test downloading multiple tickers."""
        codes = ["7203", "6758"]  # Toyota, Sony
        df = pjq.download(codes, period="10d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "date" in df.columns
        assert "7203" in df.columns
        assert "6758" in df.columns


class TestIndexIntegration:
    """Integration tests for Index class."""

    @pytest.mark.integration
    def test_topix_history(self, api_key: str) -> None:
        """Test TOPIX index (available on all tiers)."""
        topix = pjq.Index.topix()
        df = topix.history("30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "date" in df.columns
        assert "close" in df.columns


class TestMarketIntegration:
    """Integration tests for Market class."""

    @pytest.mark.integration
    def test_trading_calendar(self, api_key: str) -> None:
        """Test trading calendar."""
        market = pjq.Market()

        # Check a known holiday (New Year's Day)
        assert not market.is_trading_day(date(2024, 1, 1))

        # Check a known trading day
        assert market.is_trading_day(date(2024, 1, 4))

    @pytest.mark.integration
    def test_investor_trades(self, api_key: str) -> None:
        """Test investor trades (market-wide)."""
        market = pjq.Market()
        df = market.investor_trades(
            start=date(2024, 1, 1),
            end=date(2024, 1, 31)
        )

        assert isinstance(df, pd.DataFrame)
        # May be empty for some date ranges, but structure should be correct

    @pytest.mark.integration
    def test_earnings_calendar(self, api_key: str) -> None:
        """Test earnings calendar."""
        market = pjq.Market()
        df = market.earnings_calendar(
            start=date(2024, 10, 1),
            end=date(2024, 10, 31)
        )

        assert isinstance(df, pd.DataFrame)
        if len(df) > 0:
            # Check correct column names from EarningsAnnouncement model
            expected_cols = ["code", "company_name", "announcement_date"]
            for col in expected_cols:
                assert col in df.columns, f"Missing column: {col}"

# =============================================================================
# STANDARD+ TIER TESTS
# =============================================================================


class TestStandardTierIntegration:
    """Integration tests requiring Standard+ tier."""

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_ticker_history_am(self, api_key: str, is_standard_tier: bool) -> None:
        """Test morning session prices (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        ticker = pjq.Ticker("7203")
        df = ticker.history_am("30d")

        assert isinstance(df, pd.DataFrame)
        if len(df) > 0:
            required_cols = ["date", "open", "high", "low", "close", "volume"]
            for col in required_cols:
                assert col in df.columns, f"Missing column: {col}"

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_ticker_dividends(self, api_key: str, is_standard_tier: bool) -> None:
        """Test dividend history (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        ticker = pjq.Ticker("7203")
        df = ticker.dividends

        assert isinstance(df, pd.DataFrame)
        if len(df) > 0:
            # Check correct column names from Dividend model
            expected_cols = ["record_date", "dividend_per_share", "payment_date"]
            for col in expected_cols:
                assert col in df.columns, f"Missing column: {col}"

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_ticker_financial_details(self, api_key: str, is_standard_tier: bool) -> None:
        """Test detailed financials (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        ticker = pjq.Ticker("7203")
        df = ticker.financial_details

        assert isinstance(df, pd.DataFrame)
        if len(df) > 0:
            # Check correct column names from FinancialDetails model
            # Note: FinancialDetails uses disclosed_date, not disclosure_date
            assert "disclosed_date" in df.columns or "code" in df.columns

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_nikkei225_history(self, api_key: str, is_standard_tier: bool) -> None:
        """Test Nikkei 225 index (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        nikkei = pjq.Index.nikkei225()
        df = nikkei.history("30d")

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "close" in df.columns

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_market_sectors(self, api_key: str, is_standard_tier: bool) -> None:
        """Test sector classifications (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        sectors = market.sectors_33

        # Should return list of sectors on Standard+ tier
        assert isinstance(sectors, list)
        if len(sectors) > 0:
            assert hasattr(sectors[0], "code")
            assert hasattr(sectors[0], "name")

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_market_breakdown(self, api_key: str, is_standard_tier: bool) -> None:
        """Test trade breakdown (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        df = market.breakdown("7203")

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_market_short_ratio(self, api_key: str, is_standard_tier: bool) -> None:
        """Test short selling ratio (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        df = market.short_ratio()

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_market_short_positions(self, api_key: str, is_standard_tier: bool) -> None:
        """Test short positions report (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        df = market.short_positions()

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_market_margin_alerts(self, api_key: str, is_standard_tier: bool) -> None:
        """Test margin alerts (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        df = market.margin_alerts()

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_margin_interest(self, api_key: str, is_standard_tier: bool) -> None:
        """Test margin interest data (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        market = pjq.Market()
        df = market.margin_interest(code="7203")

        assert isinstance(df, pd.DataFrame)
        # Structure check if data exists
        if len(df) > 0:
            assert "code" in df.columns
            assert "date" in df.columns

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_futures_history(self, api_key: str, is_standard_tier: bool) -> None:
        """Test futures data (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        futures = pjq.Futures("NK225M")
        df = futures.history("30d")

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_options_history(self, api_key: str, is_standard_tier: bool) -> None:
        """Test options data (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        # Use a recent expiry/strike that's likely to have data
        options = pjq.Options("NK225C40000")
        df = options.history("30d")

        assert isinstance(df, pd.DataFrame)

    @pytest.mark.integration
    @pytest.mark.standard_tier
    def test_index_options_history(self, api_key: str, is_standard_tier: bool) -> None:
        """Test index options data (Standard+ only)."""
        if not is_standard_tier:
            pytest.skip("Requires Standard+ tier")

        idx_opts = pjq.IndexOptions.nikkei225()
        df = idx_opts.history("30d")

        assert isinstance(df, pd.DataFrame)
