"""Financial-related models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class FinancialStatement(BaseModel):
    """Financial statement data (V2 API abbreviated field names)."""

    code: str = Field(alias="Code")
    disclosure_date: datetime.date = Field(alias="DiscDate")
    disclosure_time: str | None = Field(alias="DiscTime", default=None)

    type_of_document: str | None = Field(alias="DocType", default=None)
    current_period_type: str | None = Field(alias="CurPerType", default=None)
    current_period_start: str | None = Field(alias="CurPerSt", default=None)
    current_period_end: str | None = Field(alias="CurPerEn", default=None)
    current_fy_start: str | None = Field(alias="CurFYSt", default=None)
    current_fy_end: str | None = Field(alias="CurFYEn", default=None)

    # Income Statement (abbreviated names)
    net_sales: Decimal | None = Field(alias="Sales", default=None)
    operating_profit: Decimal | None = Field(alias="OP", default=None)
    ordinary_profit: Decimal | None = Field(alias="OdP", default=None)
    profit: Decimal | None = Field(alias="NP", default=None)

    # Per Share Data
    earnings_per_share: Decimal | None = Field(alias="EPS", default=None)
    diluted_eps: Decimal | None = Field(alias="DEPS", default=None)
    book_value_per_share: Decimal | None = Field(alias="BPS", default=None)

    # Balance Sheet
    total_assets: Decimal | None = Field(alias="TA", default=None)
    equity: Decimal | None = Field(alias="Eq", default=None)
    equity_ratio: Decimal | None = Field(alias="EqAR", default=None)

    # Cash Flow
    cf_operating: Decimal | None = Field(alias="CFO", default=None)
    cf_investing: Decimal | None = Field(alias="CFI", default=None)
    cf_financing: Decimal | None = Field(alias="CFF", default=None)
    cash_equivalents: Decimal | None = Field(alias="CashEq", default=None)

    # Dividends
    dividend_q1: Decimal | None = Field(alias="Div1Q", default=None)
    dividend_q2: Decimal | None = Field(alias="Div2Q", default=None)
    dividend_q3: Decimal | None = Field(alias="Div3Q", default=None)
    dividend_fy: Decimal | None = Field(alias="DivFY", default=None)
    dividend_annual: Decimal | None = Field(alias="DivAnn", default=None)

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
        "diluted_eps",
        "book_value_per_share",
        "total_assets",
        "equity",
        "equity_ratio",
        "cf_operating",
        "cf_investing",
        "cf_financing",
        "cash_equivalents",
        "dividend_q1",
        "dividend_q2",
        "dividend_q3",
        "dividend_fy",
        "dividend_annual",
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
    """Earnings announcement calendar entry (V2 API abbreviated field names)."""

    code: str = Field(alias="Code")
    company_name: str = Field(alias="CoName")
    announcement_date: datetime.date = Field(alias="Date")
    fiscal_year: str | None = Field(alias="FY", default=None)
    fiscal_quarter: str | None = Field(alias="FQ", default=None)
    sector_name: str | None = Field(alias="SectorNm", default=None)
    section: str | None = Field(alias="Section", default=None)

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


class FinancialDetails(BaseModel):
    """Full financial statement data (BS/PL/CF).

    Provides detailed balance sheet, income statement, and cash flow data.
    """

    code: str = Field(alias="LocalCode")
    disclosed_date: datetime.date = Field(alias="DisclosedDate")
    type_of_document: str | None = Field(alias="TypeOfDocument", default=None)

    # Balance Sheet
    total_assets: Decimal | None = Field(alias="TotalAssets", default=None)
    total_liabilities: Decimal | None = Field(alias="TotalLiabilities", default=None)
    net_assets: Decimal | None = Field(alias="NetAssets", default=None)
    current_assets: Decimal | None = Field(alias="CurrentAssets", default=None)
    non_current_assets: Decimal | None = Field(alias="NoncurrentAssets", default=None)
    current_liabilities: Decimal | None = Field(alias="CurrentLiabilities", default=None)
    non_current_liabilities: Decimal | None = Field(
        alias="NoncurrentLiabilities", default=None
    )

    # Income Statement
    net_sales: Decimal | None = Field(alias="NetSales", default=None)
    cost_of_sales: Decimal | None = Field(alias="CostOfSales", default=None)
    gross_profit: Decimal | None = Field(alias="GrossProfit", default=None)
    operating_profit: Decimal | None = Field(alias="OperatingProfit", default=None)
    ordinary_profit: Decimal | None = Field(alias="OrdinaryProfit", default=None)
    profit_before_tax: Decimal | None = Field(alias="ProfitBeforeTax", default=None)
    profit: Decimal | None = Field(alias="Profit", default=None)

    # Cash Flow
    cf_operating: Decimal | None = Field(
        alias="CashFlowsFromOperatingActivities", default=None
    )
    cf_investing: Decimal | None = Field(
        alias="CashFlowsFromInvestingActivities", default=None
    )
    cf_financing: Decimal | None = Field(
        alias="CashFlowsFromFinancingActivities", default=None
    )
    cash_end_of_period: Decimal | None = Field(
        alias="CashAndCashEquivalents", default=None
    )

    @field_validator("disclosed_date", mode="before")
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
        "total_assets",
        "total_liabilities",
        "net_assets",
        "current_assets",
        "non_current_assets",
        "current_liabilities",
        "non_current_liabilities",
        "net_sales",
        "cost_of_sales",
        "gross_profit",
        "operating_profit",
        "ordinary_profit",
        "profit_before_tax",
        "profit",
        "cf_operating",
        "cf_investing",
        "cf_financing",
        "cash_end_of_period",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal | None:
        if v is None or v == "":
            return None
        return Decimal(str(v))
