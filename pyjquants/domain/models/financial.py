"""Financial-related models."""

from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from pyjquants.domain.models.base import BaseModel


class FinancialStatement(BaseModel):
    """Financial statement data (V2 API abbreviated field names).

    Contains 107 fields covering:
    - Current period actuals (consolidated and non-consolidated)
    - Current FY forecasts
    - Next FY forecasts
    - Dividend data (actual and forecast)
    - Share data
    """

    # === Metadata ===
    code: str = Field(alias="Code")
    disclosure_date: datetime.date = Field(alias="DiscDate")
    disclosure_time: str | None = Field(alias="DiscTime", default=None)
    disclosure_number: str | None = Field(alias="DiscNo", default=None)
    type_of_document: str | None = Field(alias="DocType", default=None)

    # === Period Information ===
    current_period_type: str | None = Field(alias="CurPerType", default=None)
    current_period_start: str | None = Field(alias="CurPerSt", default=None)
    current_period_end: str | None = Field(alias="CurPerEn", default=None)
    current_fy_start: str | None = Field(alias="CurFYSt", default=None)
    current_fy_end: str | None = Field(alias="CurFYEn", default=None)
    next_fy_start: str | None = Field(alias="NxtFYSt", default=None)
    next_fy_end: str | None = Field(alias="NxtFYEn", default=None)

    # === Current Period Actuals (Consolidated) ===
    net_sales: Decimal | None = Field(alias="Sales", default=None)
    operating_profit: Decimal | None = Field(alias="OP", default=None)
    ordinary_profit: Decimal | None = Field(alias="OdP", default=None)
    profit: Decimal | None = Field(alias="NP", default=None)
    earnings_per_share: Decimal | None = Field(alias="EPS", default=None)
    diluted_eps: Decimal | None = Field(alias="DEPS", default=None)
    total_assets: Decimal | None = Field(alias="TA", default=None)
    equity: Decimal | None = Field(alias="Eq", default=None)
    equity_ratio: Decimal | None = Field(alias="EqAR", default=None)
    book_value_per_share: Decimal | None = Field(alias="BPS", default=None)
    cf_operating: Decimal | None = Field(alias="CFO", default=None)
    cf_investing: Decimal | None = Field(alias="CFI", default=None)
    cf_financing: Decimal | None = Field(alias="CFF", default=None)
    cash_equivalents: Decimal | None = Field(alias="CashEq", default=None)

    # === Dividends (Actual) ===
    dividend_q1: Decimal | None = Field(alias="Div1Q", default=None)
    dividend_q2: Decimal | None = Field(alias="Div2Q", default=None)
    dividend_q3: Decimal | None = Field(alias="Div3Q", default=None)
    dividend_fy: Decimal | None = Field(alias="DivFY", default=None)
    dividend_annual: Decimal | None = Field(alias="DivAnn", default=None)
    dividend_unit: str | None = Field(alias="DivUnit", default=None)
    dividend_total_annual: Decimal | None = Field(alias="DivTotalAnn", default=None)
    payout_ratio_annual: Decimal | None = Field(alias="PayoutRatioAnn", default=None)

    # === Current FY Forecast Dividends ===
    forecast_dividend_q1: Decimal | None = Field(alias="FDiv1Q", default=None)
    forecast_dividend_q2: Decimal | None = Field(alias="FDiv2Q", default=None)
    forecast_dividend_q3: Decimal | None = Field(alias="FDiv3Q", default=None)
    forecast_dividend_fy: Decimal | None = Field(alias="FDivFY", default=None)
    forecast_dividend_annual: Decimal | None = Field(alias="FDivAnn", default=None)
    forecast_dividend_unit: str | None = Field(alias="FDivUnit", default=None)
    forecast_dividend_total_annual: Decimal | None = Field(alias="FDivTotalAnn", default=None)
    forecast_payout_ratio_annual: Decimal | None = Field(alias="FPayoutRatioAnn", default=None)

    # === Next FY Forecast Dividends ===
    next_forecast_dividend_q1: Decimal | None = Field(alias="NxFDiv1Q", default=None)
    next_forecast_dividend_q2: Decimal | None = Field(alias="NxFDiv2Q", default=None)
    next_forecast_dividend_q3: Decimal | None = Field(alias="NxFDiv3Q", default=None)
    next_forecast_dividend_fy: Decimal | None = Field(alias="NxFDivFY", default=None)
    next_forecast_dividend_annual: Decimal | None = Field(alias="NxFDivAnn", default=None)
    next_forecast_dividend_unit: str | None = Field(alias="NxFDivUnit", default=None)
    next_forecast_payout_ratio_annual: Decimal | None = Field(alias="NxFPayoutRatioAnn", default=None)

    # === Current FY Forecast (2Q Cumulative) ===
    forecast_sales_2q: Decimal | None = Field(alias="FSales2Q", default=None)
    forecast_op_2q: Decimal | None = Field(alias="FOP2Q", default=None)
    forecast_odp_2q: Decimal | None = Field(alias="FOdP2Q", default=None)
    forecast_np_2q: Decimal | None = Field(alias="FNP2Q", default=None)
    forecast_eps_2q: Decimal | None = Field(alias="FEPS2Q", default=None)

    # === Next FY Forecast (2Q Cumulative) ===
    next_forecast_sales_2q: Decimal | None = Field(alias="NxFSales2Q", default=None)
    next_forecast_op_2q: Decimal | None = Field(alias="NxFOP2Q", default=None)
    next_forecast_odp_2q: Decimal | None = Field(alias="NxFOdP2Q", default=None)
    next_forecast_np_2q: Decimal | None = Field(alias="NxFNp2Q", default=None)
    next_forecast_eps_2q: Decimal | None = Field(alias="NxFEPS2Q", default=None)

    # === Current FY Forecast (Full Year) ===
    forecast_sales: Decimal | None = Field(alias="FSales", default=None)
    forecast_op: Decimal | None = Field(alias="FOP", default=None)
    forecast_odp: Decimal | None = Field(alias="FOdP", default=None)
    forecast_np: Decimal | None = Field(alias="FNP", default=None)
    forecast_eps: Decimal | None = Field(alias="FEPS", default=None)

    # === Next FY Forecast (Full Year) ===
    next_forecast_sales: Decimal | None = Field(alias="NxFSales", default=None)
    next_forecast_op: Decimal | None = Field(alias="NxFOP", default=None)
    next_forecast_odp: Decimal | None = Field(alias="NxFOdP", default=None)
    next_forecast_np: Decimal | None = Field(alias="NxFNp", default=None)
    next_forecast_eps: Decimal | None = Field(alias="NxFEPS", default=None)

    # === Change Flags ===
    material_change_subsidiaries: str | None = Field(alias="MatChgSub", default=None)
    significant_change_in_scope: str | None = Field(alias="SigChgInC", default=None)
    change_by_accounting_standard_revision: str | None = Field(alias="ChgByASRev", default=None)
    change_not_accounting_standard_revision: str | None = Field(alias="ChgNoASRev", default=None)
    change_in_accounting_estimates: str | None = Field(alias="ChgAcEst", default=None)
    retrospective_restatement: str | None = Field(alias="RetroRst", default=None)

    # === Share Data ===
    shares_outstanding_fy: Decimal | None = Field(alias="ShOutFY", default=None)
    treasury_shares_fy: Decimal | None = Field(alias="TrShFY", default=None)
    average_shares: Decimal | None = Field(alias="AvgSh", default=None)

    # === Non-Consolidated Actuals ===
    nc_sales: Decimal | None = Field(alias="NCSales", default=None)
    nc_op: Decimal | None = Field(alias="NCOP", default=None)
    nc_odp: Decimal | None = Field(alias="NCOdP", default=None)
    nc_np: Decimal | None = Field(alias="NCNP", default=None)
    nc_eps: Decimal | None = Field(alias="NCEPS", default=None)
    nc_ta: Decimal | None = Field(alias="NCTA", default=None)
    nc_eq: Decimal | None = Field(alias="NCEq", default=None)
    nc_eq_ratio: Decimal | None = Field(alias="NCEqAR", default=None)
    nc_bps: Decimal | None = Field(alias="NCBPS", default=None)

    # === Non-Consolidated Current FY Forecast (2Q) ===
    forecast_nc_sales_2q: Decimal | None = Field(alias="FNCSales2Q", default=None)
    forecast_nc_op_2q: Decimal | None = Field(alias="FNCOP2Q", default=None)
    forecast_nc_odp_2q: Decimal | None = Field(alias="FNCOdP2Q", default=None)
    forecast_nc_np_2q: Decimal | None = Field(alias="FNCNP2Q", default=None)
    forecast_nc_eps_2q: Decimal | None = Field(alias="FNCEPS2Q", default=None)

    # === Non-Consolidated Next FY Forecast (2Q) ===
    next_forecast_nc_sales_2q: Decimal | None = Field(alias="NxFNCSales2Q", default=None)
    next_forecast_nc_op_2q: Decimal | None = Field(alias="NxFNCOP2Q", default=None)
    next_forecast_nc_odp_2q: Decimal | None = Field(alias="NxFNCOdP2Q", default=None)
    next_forecast_nc_np_2q: Decimal | None = Field(alias="NxFNCNP2Q", default=None)
    next_forecast_nc_eps_2q: Decimal | None = Field(alias="NxFNCEPS2Q", default=None)

    # === Non-Consolidated Current FY Forecast (Full Year) ===
    forecast_nc_sales: Decimal | None = Field(alias="FNCSales", default=None)
    forecast_nc_op: Decimal | None = Field(alias="FNCOP", default=None)
    forecast_nc_odp: Decimal | None = Field(alias="FNCOdP", default=None)
    forecast_nc_np: Decimal | None = Field(alias="FNCNP", default=None)
    forecast_nc_eps: Decimal | None = Field(alias="FNCEPS", default=None)

    # === Non-Consolidated Next FY Forecast (Full Year) ===
    next_forecast_nc_sales: Decimal | None = Field(alias="NxFNCSales", default=None)
    next_forecast_nc_op: Decimal | None = Field(alias="NxFNCOP", default=None)
    next_forecast_nc_odp: Decimal | None = Field(alias="NxFNCOdP", default=None)
    next_forecast_nc_np: Decimal | None = Field(alias="NxFNCNP", default=None)
    next_forecast_nc_eps: Decimal | None = Field(alias="NxFNCEPS", default=None)

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
