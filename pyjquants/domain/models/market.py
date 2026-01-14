"""Market-related models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class TradingCalendarDay(BaseModel):
    """Single trading calendar day (V2 API abbreviated field names)."""

    date: datetime.date = Field(alias="Date")
    holiday_division: str = Field(alias="HolDiv")

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")

    @property
    def is_trading_day(self) -> bool:
        return self.holiday_division == "0"

    @property
    def is_holiday(self) -> bool:
        return not self.is_trading_day


class MarginInterest(BaseModel):
    """Margin trading interest data."""

    code: str = Field(alias="Code")
    date: datetime.date = Field(alias="Date")
    margin_buying_balance: int | None = Field(alias="MarginBuyingBalance", default=None)
    margin_selling_balance: int | None = Field(alias="MarginSellingBalance", default=None)

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")


class ShortSelling(BaseModel):
    """Short selling data."""

    date: datetime.date = Field(alias="Date")
    sector_33_code: str = Field(alias="Sector33Code")
    selling_value: float | None = Field(alias="SellingValue", default=None)

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")


class InvestorTrades(BaseModel):
    """Trading by type of investors.

    Contains sell/buy/total/balance data for each investor category.
    """

    # Metadata
    pub_date: datetime.date = Field(alias="PubDate")
    start_date: datetime.date = Field(alias="StDate")
    end_date: datetime.date = Field(alias="EnDate")
    section: str | None = Field(alias="Section", default=None)

    # Proprietary trading
    prop_sell: int | None = Field(alias="PropSell", default=None)
    prop_buy: int | None = Field(alias="PropBuy", default=None)
    prop_total: int | None = Field(alias="PropTot", default=None)
    prop_balance: int | None = Field(alias="PropBal", default=None)

    # Individuals
    ind_sell: int | None = Field(alias="IndSell", default=None)
    ind_buy: int | None = Field(alias="IndBuy", default=None)
    ind_total: int | None = Field(alias="IndTot", default=None)
    ind_balance: int | None = Field(alias="IndBal", default=None)

    # Foreign investors
    frgn_sell: int | None = Field(alias="FrgnSell", default=None)
    frgn_buy: int | None = Field(alias="FrgnBuy", default=None)
    frgn_total: int | None = Field(alias="FrgnTot", default=None)
    frgn_balance: int | None = Field(alias="FrgnBal", default=None)

    # Investment trusts
    inv_tr_sell: int | None = Field(alias="InvTrSell", default=None)
    inv_tr_buy: int | None = Field(alias="InvTrBuy", default=None)
    inv_tr_total: int | None = Field(alias="InvTrTot", default=None)
    inv_tr_balance: int | None = Field(alias="InvTrBal", default=None)

    # Trust banks
    trst_bnk_sell: int | None = Field(alias="TrstBnkSell", default=None)
    trst_bnk_buy: int | None = Field(alias="TrstBnkBuy", default=None)
    trst_bnk_total: int | None = Field(alias="TrstBnkTot", default=None)
    trst_bnk_balance: int | None = Field(alias="TrstBnkBal", default=None)

    # Total
    total_sell: int | None = Field(alias="TotSell", default=None)
    total_buy: int | None = Field(alias="TotBuy", default=None)
    total_total: int | None = Field(alias="TotTot", default=None)
    total_balance: int | None = Field(alias="TotBal", default=None)

    @field_validator("pub_date", "start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")


class BreakdownTrade(BaseModel):
    """Breakdown trading data by trade type.

    Contains trading values and volumes categorized by:
    - Long selling/buying
    - Short selling (excluding margin)
    - Margin selling/buying (new and closing)
    """

    date: datetime.date = Field(alias="Date")
    code: str = Field(alias="Code")

    # Selling - Value
    long_sell_value: Decimal | None = Field(alias="LongSellVa", default=None)
    short_no_margin_value: Decimal | None = Field(alias="ShrtNoMrgnVa", default=None)
    margin_sell_new_value: Decimal | None = Field(alias="MrgnSellNewVa", default=None)
    margin_sell_close_value: Decimal | None = Field(alias="MrgnSellCloseVa", default=None)

    # Buying - Value
    long_buy_value: Decimal | None = Field(alias="LongBuyVa", default=None)
    margin_buy_new_value: Decimal | None = Field(alias="MrgnBuyNewVa", default=None)
    margin_buy_close_value: Decimal | None = Field(alias="MrgnBuyCloseVa", default=None)

    # Selling - Volume
    long_sell_volume: int | None = Field(alias="LongSellVo", default=None)
    short_no_margin_volume: int | None = Field(alias="ShrtNoMrgnVo", default=None)
    margin_sell_new_volume: int | None = Field(alias="MrgnSellNewVo", default=None)
    margin_sell_close_volume: int | None = Field(alias="MrgnSellCloseVo", default=None)

    # Buying - Volume
    long_buy_volume: int | None = Field(alias="LongBuyVo", default=None)
    margin_buy_new_volume: int | None = Field(alias="MrgnBuyNewVo", default=None)
    margin_buy_close_volume: int | None = Field(alias="MrgnBuyCloseVo", default=None)

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")

    @field_validator(
        "long_sell_value",
        "short_no_margin_value",
        "margin_sell_new_value",
        "margin_sell_close_value",
        "long_buy_value",
        "margin_buy_new_value",
        "margin_buy_close_value",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))


class ShortSaleReport(BaseModel):
    """Outstanding short selling positions reported.

    Contains reported short positions where ratio >= 0.5%.
    """

    disclosed_date: datetime.date = Field(alias="DisclosedDate")
    calculated_date: datetime.date = Field(alias="CalculatedDate")
    code: str = Field(alias="Code")
    stock_name: str | None = Field(alias="StockName", default=None)
    stock_name_english: str | None = Field(alias="StockNameEnglish", default=None)

    # Short seller info
    short_seller_name: str | None = Field(alias="ShortSellerName", default=None)
    short_seller_address: str | None = Field(alias="ShortSellerAddress", default=None)

    # Position data
    short_position_ratio: Decimal | None = Field(
        alias="ShortPositionsToSharesOutstandingRatio", default=None
    )
    short_position_shares: int | None = Field(
        alias="ShortPositionsInSharesNumber", default=None
    )
    short_position_units: int | None = Field(
        alias="ShortPositionsInTradingUnitsNumber", default=None
    )

    # Previous report
    prev_report_date: datetime.date | None = Field(
        alias="CalculationInPreviousReportingDate", default=None
    )
    prev_position_ratio: Decimal | None = Field(
        alias="ShortPositionsInPreviousReportingRatio", default=None
    )

    notes: str | None = Field(alias="Notes", default=None)

    @field_validator("disclosed_date", "calculated_date", "prev_report_date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date | None:
        if v is None or v == "":
            return None
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        return None

    @field_validator("short_position_ratio", "prev_position_ratio", mode="before")
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))


class MarginAlert(BaseModel):
    """Margin trading daily publication (alert) data.

    Contains margin trading outstanding for issues subject to daily publication.
    """

    pub_date: datetime.date = Field(alias="PubDate")
    code: str = Field(alias="Code")
    apply_date: datetime.date | None = Field(alias="AppDate", default=None)

    # Short positions
    short_outstanding: int | None = Field(alias="ShrtOut", default=None)
    short_outstanding_change: int | None = Field(alias="ShrtOutChg", default=None)
    short_outstanding_ratio: Decimal | None = Field(alias="ShrtOutRatio", default=None)

    # Long positions
    long_outstanding: int | None = Field(alias="LongOut", default=None)
    long_outstanding_change: int | None = Field(alias="LongOutChg", default=None)
    long_outstanding_ratio: Decimal | None = Field(alias="LongOutRatio", default=None)

    # Short/Long ratio
    sl_ratio: Decimal | None = Field(alias="SLRatio", default=None)

    # Negotiable/Standard breakdown
    short_neg_outstanding: int | None = Field(alias="ShrtNegOut", default=None)
    short_std_outstanding: int | None = Field(alias="ShrtStdOut", default=None)
    long_neg_outstanding: int | None = Field(alias="LongNegOut", default=None)
    long_std_outstanding: int | None = Field(alias="LongStdOut", default=None)

    @field_validator("pub_date", "apply_date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date | None:
        if v is None or v == "":
            return None
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        return None

    @field_validator(
        "short_outstanding_ratio",
        "long_outstanding_ratio",
        "sl_ratio",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))
