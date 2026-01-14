"""Market-related models."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pyjquants.domain.models.base import (
    BaseModel,
    JQuantsDate,
    JQuantsDateOptional,
    JQuantsDecimal,
)


class TradingCalendarDay(BaseModel):
    """Single trading calendar day (V2 API abbreviated field names)."""

    date: JQuantsDate = Field(alias="Date")
    holiday_division: str = Field(alias="HolDiv")

    @property
    def is_trading_day(self) -> bool:
        # HolDiv: "0" = holiday/weekend, "1" = trading day
        return self.holiday_division == "1"

    @property
    def is_holiday(self) -> bool:
        return not self.is_trading_day


class MarginInterest(BaseModel):
    """Margin trading interest data."""

    code: str = Field(alias="Code")
    date: JQuantsDate = Field(alias="Date")
    margin_buying_balance: int | None = Field(alias="MarginBuyingBalance", default=None)
    margin_selling_balance: int | None = Field(alias="MarginSellingBalance", default=None)


class ShortSelling(BaseModel):
    """Short sale value and ratio by sector.

    Data from J-Quants /markets/short-ratio endpoint.
    Contains long selling and short selling (with/without price restrictions) by 33-sector.
    """

    date: JQuantsDate = Field(alias="Date")
    sector_33_code: str = Field(alias="S33")
    long_selling_value: JQuantsDecimal = Field(alias="SellExShortVa", default=None)
    short_with_restriction_value: JQuantsDecimal = Field(alias="ShrtWithResVa", default=None)
    short_no_restriction_value: JQuantsDecimal = Field(alias="ShrtNoResVa", default=None)


class InvestorTrades(BaseModel):
    """Market-wide trading by type of investors.

    Contains sell/buy/total/balance data for each investor category.
    Note: This is aggregate market data, not per-stock data.
    """

    # Metadata
    pub_date: JQuantsDate = Field(alias="PubDate")
    start_date: JQuantsDate = Field(alias="StDate")
    end_date: JQuantsDate = Field(alias="EnDate")
    section: str | None = Field(alias="Section", default=None)

    # Proprietary trading
    prop_sell: float | None = Field(alias="PropSell", default=None)
    prop_buy: float | None = Field(alias="PropBuy", default=None)
    prop_total: float | None = Field(alias="PropTot", default=None)
    prop_balance: float | None = Field(alias="PropBal", default=None)

    # Brokers
    brk_sell: float | None = Field(alias="BrkSell", default=None)
    brk_buy: float | None = Field(alias="BrkBuy", default=None)
    brk_total: float | None = Field(alias="BrkTot", default=None)
    brk_balance: float | None = Field(alias="BrkBal", default=None)

    # Individuals
    ind_sell: float | None = Field(alias="IndSell", default=None)
    ind_buy: float | None = Field(alias="IndBuy", default=None)
    ind_total: float | None = Field(alias="IndTot", default=None)
    ind_balance: float | None = Field(alias="IndBal", default=None)

    # Foreign investors
    frgn_sell: float | None = Field(alias="FrgnSell", default=None)
    frgn_buy: float | None = Field(alias="FrgnBuy", default=None)
    frgn_total: float | None = Field(alias="FrgnTot", default=None)
    frgn_balance: float | None = Field(alias="FrgnBal", default=None)

    # Securities companies
    sec_co_sell: float | None = Field(alias="SecCoSell", default=None)
    sec_co_buy: float | None = Field(alias="SecCoBuy", default=None)
    sec_co_total: float | None = Field(alias="SecCoTot", default=None)
    sec_co_balance: float | None = Field(alias="SecCoBal", default=None)

    # Investment trusts
    inv_tr_sell: float | None = Field(alias="InvTrSell", default=None)
    inv_tr_buy: float | None = Field(alias="InvTrBuy", default=None)
    inv_tr_total: float | None = Field(alias="InvTrTot", default=None)
    inv_tr_balance: float | None = Field(alias="InvTrBal", default=None)

    # Business corporations
    bus_co_sell: float | None = Field(alias="BusCoSell", default=None)
    bus_co_buy: float | None = Field(alias="BusCoBuy", default=None)
    bus_co_total: float | None = Field(alias="BusCoTot", default=None)
    bus_co_balance: float | None = Field(alias="BusCoBal", default=None)

    # Other corporations
    oth_co_sell: float | None = Field(alias="OthCoSell", default=None)
    oth_co_buy: float | None = Field(alias="OthCoBuy", default=None)
    oth_co_total: float | None = Field(alias="OthCoTot", default=None)
    oth_co_balance: float | None = Field(alias="OthCoBal", default=None)

    # Insurance companies
    ins_co_sell: float | None = Field(alias="InsCoSell", default=None)
    ins_co_buy: float | None = Field(alias="InsCoBuy", default=None)
    ins_co_total: float | None = Field(alias="InsCoTot", default=None)
    ins_co_balance: float | None = Field(alias="InsCoBal", default=None)

    # Banks
    bank_sell: float | None = Field(alias="BankSell", default=None)
    bank_buy: float | None = Field(alias="BankBuy", default=None)
    bank_total: float | None = Field(alias="BankTot", default=None)
    bank_balance: float | None = Field(alias="BankBal", default=None)

    # Trust banks
    trst_bnk_sell: float | None = Field(alias="TrstBnkSell", default=None)
    trst_bnk_buy: float | None = Field(alias="TrstBnkBuy", default=None)
    trst_bnk_total: float | None = Field(alias="TrstBnkTot", default=None)
    trst_bnk_balance: float | None = Field(alias="TrstBnkBal", default=None)

    # Other financials
    oth_fin_sell: float | None = Field(alias="OthFinSell", default=None)
    oth_fin_buy: float | None = Field(alias="OthFinBuy", default=None)
    oth_fin_total: float | None = Field(alias="OthFinTot", default=None)
    oth_fin_balance: float | None = Field(alias="OthFinBal", default=None)

    # Total
    total_sell: float | None = Field(alias="TotSell", default=None)
    total_buy: float | None = Field(alias="TotBuy", default=None)
    total_total: float | None = Field(alias="TotTot", default=None)
    total_balance: float | None = Field(alias="TotBal", default=None)


class BreakdownTrade(BaseModel):
    """Breakdown trading data by trade type.

    Contains trading values and volumes categorized by:
    - Long selling/buying
    - Short selling (excluding margin)
    - Margin selling/buying (new and closing)
    """

    date: JQuantsDate = Field(alias="Date")
    code: str = Field(alias="Code")

    # Selling - Value
    long_sell_value: JQuantsDecimal = Field(alias="LongSellVa", default=None)
    short_no_margin_value: JQuantsDecimal = Field(alias="ShrtNoMrgnVa", default=None)
    margin_sell_new_value: JQuantsDecimal = Field(alias="MrgnSellNewVa", default=None)
    margin_sell_close_value: JQuantsDecimal = Field(alias="MrgnSellCloseVa", default=None)

    # Buying - Value
    long_buy_value: JQuantsDecimal = Field(alias="LongBuyVa", default=None)
    margin_buy_new_value: JQuantsDecimal = Field(alias="MrgnBuyNewVa", default=None)
    margin_buy_close_value: JQuantsDecimal = Field(alias="MrgnBuyCloseVa", default=None)

    # Selling - Volume
    long_sell_volume: int | None = Field(alias="LongSellVo", default=None)
    short_no_margin_volume: int | None = Field(alias="ShrtNoMrgnVo", default=None)
    margin_sell_new_volume: int | None = Field(alias="MrgnSellNewVo", default=None)
    margin_sell_close_volume: int | None = Field(alias="MrgnSellCloseVo", default=None)

    # Buying - Volume
    long_buy_volume: int | None = Field(alias="LongBuyVo", default=None)
    margin_buy_new_volume: int | None = Field(alias="MrgnBuyNewVo", default=None)
    margin_buy_close_volume: int | None = Field(alias="MrgnBuyCloseVo", default=None)


class ShortSaleReport(BaseModel):
    """Outstanding short selling positions reported.

    Contains reported short positions where ratio >= 0.5%.
    """

    disclosed_date: JQuantsDate = Field(alias="DisclosedDate")
    calculated_date: JQuantsDate = Field(alias="CalculatedDate")
    code: str = Field(alias="Code")
    stock_name: str | None = Field(alias="StockName", default=None)
    stock_name_english: str | None = Field(alias="StockNameEnglish", default=None)

    # Short seller info
    short_seller_name: str | None = Field(alias="ShortSellerName", default=None)
    short_seller_address: str | None = Field(alias="ShortSellerAddress", default=None)

    # Position data
    short_position_ratio: JQuantsDecimal = Field(
        alias="ShortPositionsToSharesOutstandingRatio", default=None
    )
    short_position_shares: int | None = Field(
        alias="ShortPositionsInSharesNumber", default=None
    )
    short_position_units: int | None = Field(
        alias="ShortPositionsInTradingUnitsNumber", default=None
    )

    # Previous report
    prev_report_date: JQuantsDateOptional = Field(
        alias="CalculationInPreviousReportingDate", default=None
    )
    prev_position_ratio: JQuantsDecimal = Field(
        alias="ShortPositionsInPreviousReportingRatio", default=None
    )

    notes: str | None = Field(alias="Notes", default=None)


class MarginAlert(BaseModel):
    """Margin trading daily publication (alert) data.

    Contains margin trading outstanding for issues subject to daily publication.
    Includes both negotiable and standardized margin positions.
    """

    pub_date: JQuantsDate = Field(alias="PubDate")
    code: str = Field(alias="Code")
    apply_date: JQuantsDateOptional = Field(alias="AppDate", default=None)

    # Publication reason (map of flags)
    pub_reason: dict[str, Any] | None = Field(alias="PubReason", default=None)

    # Total short positions
    short_outstanding: int | None = Field(alias="ShrtOut", default=None)
    short_outstanding_change: int | str | None = Field(alias="ShrtOutChg", default=None)
    short_outstanding_ratio: JQuantsDecimal = Field(alias="ShrtOutRatio", default=None)

    # Total long positions
    long_outstanding: int | None = Field(alias="LongOut", default=None)
    long_outstanding_change: int | str | None = Field(alias="LongOutChg", default=None)
    long_outstanding_ratio: JQuantsDecimal = Field(alias="LongOutRatio", default=None)

    # Short/Long ratio
    sl_ratio: JQuantsDecimal = Field(alias="SLRatio", default=None)

    # Negotiable short breakdown
    short_neg_outstanding: int | None = Field(alias="ShrtNegOut", default=None)
    short_neg_outstanding_change: int | str | None = Field(alias="ShrtNegOutChg", default=None)

    # Standardized short breakdown
    short_std_outstanding: int | None = Field(alias="ShrtStdOut", default=None)
    short_std_outstanding_change: int | str | None = Field(alias="ShrtStdOutChg", default=None)

    # Negotiable long breakdown
    long_neg_outstanding: int | None = Field(alias="LongNegOut", default=None)
    long_neg_outstanding_change: int | str | None = Field(alias="LongNegOutChg", default=None)

    # Standardized long breakdown
    long_std_outstanding: int | None = Field(alias="LongStdOut", default=None)
    long_std_outstanding_change: int | str | None = Field(alias="LongStdOutChg", default=None)

    # TSE margin regulation classification
    tse_margin_reg_class: str | None = Field(alias="TSEMrgnRegCls", default=None)
