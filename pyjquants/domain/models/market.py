"""Market-related models."""

from __future__ import annotations

import datetime
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class TradingCalendarDay(BaseModel):
    """Single trading calendar day."""

    date: datetime.date = Field(alias="Date")
    holiday_division: str = Field(alias="HolidayDivision")

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
