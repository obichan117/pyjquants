"""Tests for pyjquants models."""

from __future__ import annotations

import datetime
from decimal import Decimal

from pyjquants.domain.models import (
    BreakdownTrade,
    FinancialDetails,
    FuturesPrice,
    InvestorTrades,
    MarginAlert,
    MarketSegment,
    OptionsPrice,
    PriceBar,
    Sector,
    ShortSaleReport,
    StockInfo,
    TradingCalendarDay,
)


class TestPriceBar:
    """Tests for PriceBar model."""

    def test_create_from_dict(self) -> None:
        """Test creating PriceBar from API response dict (V2 abbreviated names)."""
        data = {
            "Date": "2024-01-15",
            "O": "2500.0",
            "H": "2550.0",
            "L": "2480.0",
            "C": "2530.0",
            "Vo": 1000000,
        }
        bar = PriceBar.model_validate(data)

        assert bar.date == datetime.date(2024, 1, 15)
        assert bar.open == Decimal("2500.0")
        assert bar.high == Decimal("2550.0")
        assert bar.low == Decimal("2480.0")
        assert bar.close == Decimal("2530.0")
        assert bar.volume == 1000000

    def test_create_with_yyyymmdd_date(self) -> None:
        """Test parsing YYYYMMDD date format."""
        data = {
            "Date": "20240115",
            "O": "2500.0",
            "H": "2550.0",
            "L": "2480.0",
            "C": "2530.0",
            "Vo": 1000000,
        }
        bar = PriceBar.model_validate(data)
        assert bar.date == datetime.date(2024, 1, 15)

    def test_adjusted_prices_default(self, sample_price_bar: PriceBar) -> None:
        """Test adjusted prices with factor 1.0."""
        assert sample_price_bar.adjusted_open == sample_price_bar.open
        assert sample_price_bar.adjusted_close == sample_price_bar.close
        assert sample_price_bar.adjusted_volume == sample_price_bar.volume

    def test_adjusted_prices_with_factor(self) -> None:
        """Test adjusted prices with adjustment factor."""
        bar = PriceBar(
            date=datetime.date(2024, 1, 15),
            open=Decimal("2500.0"),
            high=Decimal("2550.0"),
            low=Decimal("2480.0"),
            close=Decimal("2530.0"),
            volume=1000000,
            adjustment_factor=Decimal("2.0"),
        )
        assert bar.adjusted_open == Decimal("5000.0")
        assert bar.adjusted_close == Decimal("5060.0")

    def test_to_dict(self, sample_price_bar: PriceBar) -> None:
        """Test converting to dictionary."""
        d = sample_price_bar.to_dict()
        assert d["date"] == datetime.date(2024, 1, 15)
        assert d["close"] == 2530.0
        assert d["volume"] == 1000000


class TestSector:
    """Tests for Sector model."""

    def test_create_sector(self) -> None:
        """Test creating a Sector."""
        sector = Sector(code="3050", name="輸送用機器", name_english="Transportation Equipment")
        assert sector.code == "3050"
        assert sector.name == "輸送用機器"
        assert str(sector) == "輸送用機器"

    def test_sector_equality(self) -> None:
        """Test Sector equality."""
        s1 = Sector(code="3050", name="輸送用機器")
        s2 = Sector(code="3050", name="輸送用機器")
        s3 = Sector(code="3100", name="電気機器")

        assert s1 == s2
        assert s1 != s3
        assert s1 == "3050"  # Can compare with code string

    def test_sector_hash(self) -> None:
        """Test Sector can be used in sets."""
        s1 = Sector(code="3050", name="輸送用機器")
        s2 = Sector(code="3050", name="輸送用機器")

        sector_set = {s1, s2}
        assert len(sector_set) == 1


class TestStockInfo:
    """Tests for StockInfo model."""

    def test_create_from_api_data(self, sample_stock_info_data: dict) -> None:
        """Test creating StockInfo from API response."""
        info = StockInfo.model_validate(sample_stock_info_data)

        assert info.code == "7203"
        assert info.company_name == "トヨタ自動車"
        assert info.company_name_english == "Toyota Motor Corporation"
        assert info.sector_33_code == "3050"

    def test_sector_properties(self, sample_stock_info: StockInfo) -> None:
        """Test sector property accessors."""
        assert sample_stock_info.sector_17.code == "6"
        assert sample_stock_info.sector_33.code == "3050"

    def test_market_segment(self, sample_stock_info: StockInfo) -> None:
        """Test market segment conversion."""
        assert sample_stock_info.market_segment == MarketSegment.TSE_PRIME

    def test_listing_date(self, sample_stock_info: StockInfo) -> None:
        """Test listing date parsing."""
        assert sample_stock_info.listing_date == datetime.date(2024, 1, 15)


class TestMarketSegment:
    """Tests for MarketSegment enum."""

    def test_from_code(self) -> None:
        """Test converting market codes."""
        assert MarketSegment.from_code("0111") == MarketSegment.TSE_PRIME
        assert MarketSegment.from_code("0112") == MarketSegment.TSE_STANDARD
        assert MarketSegment.from_code("0113") == MarketSegment.TSE_GROWTH
        assert MarketSegment.from_code("0105") == MarketSegment.TOKYO_PRO
        assert MarketSegment.from_code("0109") == MarketSegment.OTHER
        assert MarketSegment.from_code("9999") == MarketSegment.OTHER


class TestTradingCalendarDay:
    """Tests for TradingCalendarDay model."""

    def test_trading_day(self) -> None:
        """Test trading day identification."""
        day = TradingCalendarDay(
            date=datetime.date(2024, 1, 15),
            holiday_division="1",  # "1" = trading day
        )
        assert day.is_trading_day is True
        assert day.is_holiday is False

    def test_holiday(self) -> None:
        """Test holiday identification."""
        day = TradingCalendarDay(
            date=datetime.date(2024, 1, 1),
            holiday_division="0",  # "0" = holiday
        )
        assert day.is_trading_day is False
        assert day.is_holiday is True


class TestInvestorTrades:
    """Tests for InvestorTrades model."""

    def test_create_from_api_data(self) -> None:
        """Test creating InvestorTrades from API response."""
        data = {
            "PubDate": "2024-01-15",
            "StDate": "2024-01-08",
            "EnDate": "2024-01-12",
            "Section": "TSE1",
            "PropSell": 1000000,
            "PropBuy": 1200000,
            "IndSell": 500000,
            "IndBuy": 600000,
            "FrgnSell": 2000000,
            "FrgnBuy": 2500000,
        }
        trades = InvestorTrades.model_validate(data)

        assert trades.pub_date == datetime.date(2024, 1, 15)
        assert trades.start_date == datetime.date(2024, 1, 8)
        assert trades.end_date == datetime.date(2024, 1, 12)
        assert trades.section == "TSE1"
        assert trades.prop_sell == 1000000
        assert trades.prop_buy == 1200000
        assert trades.ind_sell == 500000
        assert trades.frgn_buy == 2500000

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "PubDate": "20240115",
            "StDate": "20240108",
            "EnDate": "20240112",
        }
        trades = InvestorTrades.model_validate(data)

        assert trades.pub_date == datetime.date(2024, 1, 15)
        assert trades.prop_sell is None
        assert trades.ind_buy is None
        assert trades.total_total is None


class TestFinancialDetails:
    """Tests for FinancialDetails model."""

    def test_create_from_api_data(self) -> None:
        """Test creating FinancialDetails from API response."""
        data = {
            "LocalCode": "7203",
            "DisclosedDate": "2024-01-15",
            "TypeOfDocument": "Annual",
            "TotalAssets": "1000000000",
            "NetAssets": "500000000",
            "NetSales": "200000000",
            "OperatingProfit": "50000000",
            "Profit": "30000000",
            "CashFlowsFromOperatingActivities": "40000000",
            "CashFlowsFromInvestingActivities": "-20000000",
            "CashFlowsFromFinancingActivities": "-10000000",
        }
        details = FinancialDetails.model_validate(data)

        assert details.code == "7203"
        assert details.disclosed_date == datetime.date(2024, 1, 15)
        assert details.total_assets == Decimal("1000000000")
        assert details.net_assets == Decimal("500000000")
        assert details.net_sales == Decimal("200000000")
        assert details.operating_profit == Decimal("50000000")
        assert details.profit == Decimal("30000000")
        assert details.cf_operating == Decimal("40000000")
        assert details.cf_investing == Decimal("-20000000")
        assert details.cf_financing == Decimal("-10000000")

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "LocalCode": "7203",
            "DisclosedDate": "20240115",
        }
        details = FinancialDetails.model_validate(data)

        assert details.code == "7203"
        assert details.total_assets is None
        assert details.cf_operating is None
        assert details.gross_profit is None


class TestBreakdownTrade:
    """Tests for BreakdownTrade model."""

    def test_create_from_api_data(self) -> None:
        """Test creating BreakdownTrade from API response."""
        data = {
            "Date": "2024-01-15",
            "Code": "7203",
            "LongSellVa": "1000000.5",
            "ShrtNoMrgnVa": "500000.0",
            "MrgnSellNewVa": "200000.0",
            "MrgnSellCloseVa": "150000.0",
            "LongBuyVa": "1200000.0",
            "MrgnBuyNewVa": "100000.0",
            "MrgnBuyCloseVa": "50000.0",
            "LongSellVo": 10000,
            "ShrtNoMrgnVo": 5000,
            "MrgnSellNewVo": 2000,
            "MrgnSellCloseVo": 1500,
            "LongBuyVo": 12000,
            "MrgnBuyNewVo": 1000,
            "MrgnBuyCloseVo": 500,
        }
        trade = BreakdownTrade.model_validate(data)

        assert trade.date == datetime.date(2024, 1, 15)
        assert trade.code == "7203"
        assert trade.long_sell_value == Decimal("1000000.5")
        assert trade.short_no_margin_value == Decimal("500000.0")
        assert trade.margin_sell_new_value == Decimal("200000.0")
        assert trade.long_buy_value == Decimal("1200000.0")
        assert trade.long_sell_volume == 10000
        assert trade.short_no_margin_volume == 5000

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "Date": "20240115",
            "Code": "7203",
        }
        trade = BreakdownTrade.model_validate(data)

        assert trade.date == datetime.date(2024, 1, 15)
        assert trade.code == "7203"
        assert trade.long_sell_value is None
        assert trade.long_sell_volume is None


class TestShortSaleReport:
    """Tests for ShortSaleReport model."""

    def test_create_from_api_data(self) -> None:
        """Test creating ShortSaleReport from API response."""
        data = {
            "DisclosedDate": "2024-01-15",
            "CalculatedDate": "2024-01-12",
            "Code": "7203",
            "StockName": "トヨタ自動車",
            "StockNameEnglish": "Toyota Motor Corporation",
            "ShortSellerName": "Goldman Sachs",
            "ShortSellerAddress": "New York, USA",
            "ShortPositionsToSharesOutstandingRatio": "0.52",
            "ShortPositionsInSharesNumber": 1000000,
            "ShortPositionsInTradingUnitsNumber": 10000,
            "CalculationInPreviousReportingDate": "2024-01-05",
            "ShortPositionsInPreviousReportingRatio": "0.48",
        }
        report = ShortSaleReport.model_validate(data)

        assert report.disclosed_date == datetime.date(2024, 1, 15)
        assert report.calculated_date == datetime.date(2024, 1, 12)
        assert report.code == "7203"
        assert report.stock_name == "トヨタ自動車"
        assert report.short_seller_name == "Goldman Sachs"
        assert report.short_position_ratio == Decimal("0.52")
        assert report.short_position_shares == 1000000
        assert report.prev_report_date == datetime.date(2024, 1, 5)
        assert report.prev_position_ratio == Decimal("0.48")

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "DisclosedDate": "20240115",
            "CalculatedDate": "20240112",
            "Code": "7203",
        }
        report = ShortSaleReport.model_validate(data)

        assert report.disclosed_date == datetime.date(2024, 1, 15)
        assert report.code == "7203"
        assert report.stock_name is None
        assert report.short_position_ratio is None
        assert report.prev_report_date is None


class TestMarginAlert:
    """Tests for MarginAlert model."""

    def test_create_from_api_data(self) -> None:
        """Test creating MarginAlert from API response."""
        data = {
            "PubDate": "2024-01-15",
            "Code": "7203",
            "AppDate": "2024-01-14",
            "ShrtOut": 500000,
            "ShrtOutChg": 10000,
            "ShrtOutRatio": "1.5",
            "LongOut": 800000,
            "LongOutChg": -5000,
            "LongOutRatio": "2.4",
            "SLRatio": "0.625",
            "ShrtNegOut": 100000,
            "ShrtStdOut": 400000,
            "LongNegOut": 200000,
            "LongStdOut": 600000,
        }
        alert = MarginAlert.model_validate(data)

        assert alert.pub_date == datetime.date(2024, 1, 15)
        assert alert.code == "7203"
        assert alert.apply_date == datetime.date(2024, 1, 14)
        assert alert.short_outstanding == 500000
        assert alert.short_outstanding_change == 10000
        assert alert.short_outstanding_ratio == Decimal("1.5")
        assert alert.long_outstanding == 800000
        assert alert.long_outstanding_change == -5000
        assert alert.sl_ratio == Decimal("0.625")
        assert alert.short_neg_outstanding == 100000
        assert alert.short_std_outstanding == 400000

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "PubDate": "20240115",
            "Code": "7203",
        }
        alert = MarginAlert.model_validate(data)

        assert alert.pub_date == datetime.date(2024, 1, 15)
        assert alert.code == "7203"
        assert alert.apply_date is None
        assert alert.short_outstanding is None
        assert alert.sl_ratio is None


class TestFuturesPrice:
    """Tests for FuturesPrice model."""

    def test_create_from_api_data(self) -> None:
        """Test creating FuturesPrice from API response."""
        data = {
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
            "MO": "35100.0",
            "MC": "35150.0",
            "CCMFlag": "1",
        }
        price = FuturesPrice.model_validate(data)

        assert price.date == datetime.date(2024, 1, 15)
        assert price.code == "NK225M"
        assert price.product_category == "NK225M"
        assert price.contract_month == "2024-03"
        assert price.open == Decimal("35000.0")
        assert price.high == Decimal("35500.0")
        assert price.low == Decimal("34800.0")
        assert price.close == Decimal("35200.0")
        assert price.volume == 100000
        assert price.open_interest == 50000
        assert price.settlement_price == Decimal("35200.0")
        assert price.last_trading_day == datetime.date(2024, 3, 8)
        assert price.morning_open == Decimal("35100.0")
        assert price.central_contract_month_flag == "1"

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "Date": "20240115",
            "Code": "NK225M",
            "ProdCat": "NK225M",
            "CM": "2024-03",
        }
        price = FuturesPrice.model_validate(data)

        assert price.date == datetime.date(2024, 1, 15)
        assert price.code == "NK225M"
        assert price.open is None
        assert price.volume is None
        assert price.settlement_price is None
        assert price.morning_open is None


class TestOptionsPrice:
    """Tests for OptionsPrice model."""

    def test_create_from_api_data(self) -> None:
        """Test creating OptionsPrice from API response."""
        data = {
            "Date": "2024-01-15",
            "Code": "NK225C35000",
            "ProdCat": "NK225",
            "CM": "2024-03",
            "Strike": "35000.0",
            "PCDiv": "2",  # Call
            "UndSSO": "-",
            "O": "500.0",
            "H": "550.0",
            "L": "480.0",
            "C": "520.0",
            "Vo": 5000,
            "OI": 10000,
            "Settle": "520.0",
            "Theo": "515.0",
            "IV": "0.22",
            "BaseVol": "0.20",
            "UnderPx": "35200.0",
            "IR": "0.001",
            "LTD": "2024-03-08",
            "SQD": "2024-03-08",
        }
        price = OptionsPrice.model_validate(data)

        assert price.date == datetime.date(2024, 1, 15)
        assert price.code == "NK225C35000"
        assert price.product_category == "NK225"
        assert price.contract_month == "2024-03"
        assert price.strike_price == Decimal("35000.0")
        assert price.put_call_division == "2"
        assert price.is_call is True
        assert price.is_put is False
        assert price.open == Decimal("500.0")
        assert price.close == Decimal("520.0")
        assert price.volume == 5000
        assert price.open_interest == 10000
        assert price.implied_volatility == Decimal("0.22")
        assert price.theoretical_price == Decimal("515.0")
        assert price.underlying_price == Decimal("35200.0")

    def test_put_option(self) -> None:
        """Test is_put property for put options."""
        data = {
            "Date": "2024-01-15",
            "Code": "NK225P35000",
            "ProdCat": "NK225",
            "CM": "2024-03",
            "PCDiv": "1",  # Put
        }
        price = OptionsPrice.model_validate(data)

        assert price.is_put is True
        assert price.is_call is False

    def test_optional_fields(self) -> None:
        """Test that optional fields default to None."""
        data = {
            "Date": "20240115",
            "Code": "NK225C35000",
            "ProdCat": "NK225",
            "CM": "2024-03",
        }
        price = OptionsPrice.model_validate(data)

        assert price.date == datetime.date(2024, 1, 15)
        assert price.code == "NK225C35000"
        assert price.strike_price is None
        assert price.implied_volatility is None
        assert price.put_call_division is None
        assert price.is_put is False
        assert price.is_call is False
