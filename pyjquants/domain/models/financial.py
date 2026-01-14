"""Financial-related models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class FinancialStatement(BaseModel):
    """Financial statement data."""

    code: str = Field(alias="LocalCode")
    disclosure_date: datetime.date = Field(alias="DisclosedDate")

    type_of_document: str | None = Field(alias="TypeOfDocument", default=None)
    net_sales: Decimal | None = Field(alias="NetSales", default=None)
    operating_profit: Decimal | None = Field(alias="OperatingProfit", default=None)
    ordinary_profit: Decimal | None = Field(alias="OrdinaryProfit", default=None)
    profit: Decimal | None = Field(alias="Profit", default=None)

    earnings_per_share: Decimal | None = Field(alias="EarningsPerShare", default=None)
    book_value_per_share: Decimal | None = Field(alias="BookValuePerShare", default=None)
    total_assets: Decimal | None = Field(alias="TotalAssets", default=None)
    equity: Decimal | None = Field(alias="Equity", default=None)

    roe: float | None = Field(alias="ROE", default=None)
    roa: float | None = Field(alias="ROA", default=None)

    @field_validator("disclosure_date", mode="before")
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
        "net_sales",
        "operating_profit",
        "ordinary_profit",
        "profit",
        "earnings_per_share",
        "book_value_per_share",
        "total_assets",
        "equity",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))


class Dividend(BaseModel):
    """Dividend data."""

    code: str = Field(alias="Code")
    record_date: datetime.date = Field(alias="RecordDate")
    ex_dividend_date: datetime.date | None = Field(alias="ExDividendDate", default=None)
    payment_date: datetime.date | None = Field(alias="PaymentDate", default=None)
    dividend_per_share: Decimal = Field(alias="DividendPerShare")

    @field_validator("record_date", "ex_dividend_date", "payment_date", mode="before")
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

    @field_validator("dividend_per_share", mode="before")
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))


class EarningsAnnouncement(BaseModel):
    """Earnings announcement calendar entry."""

    code: str = Field(alias="Code")
    company_name: str = Field(alias="CompanyName")
    announcement_date: datetime.date = Field(alias="Date")

    @field_validator("announcement_date", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> datetime.date:
        if isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            if "-" in v:
                return datetime.date.fromisoformat(v)
            return datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        raise ValueError(f"Cannot parse date: {v}")
