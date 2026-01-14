"""Financial-related models."""

from __future__ import annotations

from pydantic import Field

from pyjquants.domain.models.base import (
    BaseModel,
    JQuantsDate,
    JQuantsDateOptional,
    JQuantsDecimal,
    JQuantsDecimalRequired,
)


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
    disclosure_date: JQuantsDate = Field(alias="DiscDate")
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
    net_sales: JQuantsDecimal = Field(alias="Sales", default=None)
    operating_profit: JQuantsDecimal = Field(alias="OP", default=None)
    ordinary_profit: JQuantsDecimal = Field(alias="OdP", default=None)
    profit: JQuantsDecimal = Field(alias="NP", default=None)
    earnings_per_share: JQuantsDecimal = Field(alias="EPS", default=None)
    diluted_eps: JQuantsDecimal = Field(alias="DEPS", default=None)
    total_assets: JQuantsDecimal = Field(alias="TA", default=None)
    equity: JQuantsDecimal = Field(alias="Eq", default=None)
    equity_ratio: JQuantsDecimal = Field(alias="EqAR", default=None)
    book_value_per_share: JQuantsDecimal = Field(alias="BPS", default=None)
    cf_operating: JQuantsDecimal = Field(alias="CFO", default=None)
    cf_investing: JQuantsDecimal = Field(alias="CFI", default=None)
    cf_financing: JQuantsDecimal = Field(alias="CFF", default=None)
    cash_equivalents: JQuantsDecimal = Field(alias="CashEq", default=None)

    # === Dividends (Actual) ===
    dividend_q1: JQuantsDecimal = Field(alias="Div1Q", default=None)
    dividend_q2: JQuantsDecimal = Field(alias="Div2Q", default=None)
    dividend_q3: JQuantsDecimal = Field(alias="Div3Q", default=None)
    dividend_fy: JQuantsDecimal = Field(alias="DivFY", default=None)
    dividend_annual: JQuantsDecimal = Field(alias="DivAnn", default=None)
    dividend_unit: str | None = Field(alias="DivUnit", default=None)
    dividend_total_annual: JQuantsDecimal = Field(alias="DivTotalAnn", default=None)
    payout_ratio_annual: JQuantsDecimal = Field(alias="PayoutRatioAnn", default=None)

    # === Current FY Forecast Dividends ===
    forecast_dividend_q1: JQuantsDecimal = Field(alias="FDiv1Q", default=None)
    forecast_dividend_q2: JQuantsDecimal = Field(alias="FDiv2Q", default=None)
    forecast_dividend_q3: JQuantsDecimal = Field(alias="FDiv3Q", default=None)
    forecast_dividend_fy: JQuantsDecimal = Field(alias="FDivFY", default=None)
    forecast_dividend_annual: JQuantsDecimal = Field(alias="FDivAnn", default=None)
    forecast_dividend_unit: str | None = Field(alias="FDivUnit", default=None)
    forecast_dividend_total_annual: JQuantsDecimal = Field(alias="FDivTotalAnn", default=None)
    forecast_payout_ratio_annual: JQuantsDecimal = Field(alias="FPayoutRatioAnn", default=None)

    # === Next FY Forecast Dividends ===
    next_forecast_dividend_q1: JQuantsDecimal = Field(alias="NxFDiv1Q", default=None)
    next_forecast_dividend_q2: JQuantsDecimal = Field(alias="NxFDiv2Q", default=None)
    next_forecast_dividend_q3: JQuantsDecimal = Field(alias="NxFDiv3Q", default=None)
    next_forecast_dividend_fy: JQuantsDecimal = Field(alias="NxFDivFY", default=None)
    next_forecast_dividend_annual: JQuantsDecimal = Field(alias="NxFDivAnn", default=None)
    next_forecast_dividend_unit: str | None = Field(alias="NxFDivUnit", default=None)
    next_forecast_payout_ratio_annual: JQuantsDecimal = Field(alias="NxFPayoutRatioAnn", default=None)

    # === Current FY Forecast (2Q Cumulative) ===
    forecast_sales_2q: JQuantsDecimal = Field(alias="FSales2Q", default=None)
    forecast_op_2q: JQuantsDecimal = Field(alias="FOP2Q", default=None)
    forecast_odp_2q: JQuantsDecimal = Field(alias="FOdP2Q", default=None)
    forecast_np_2q: JQuantsDecimal = Field(alias="FNP2Q", default=None)
    forecast_eps_2q: JQuantsDecimal = Field(alias="FEPS2Q", default=None)

    # === Next FY Forecast (2Q Cumulative) ===
    next_forecast_sales_2q: JQuantsDecimal = Field(alias="NxFSales2Q", default=None)
    next_forecast_op_2q: JQuantsDecimal = Field(alias="NxFOP2Q", default=None)
    next_forecast_odp_2q: JQuantsDecimal = Field(alias="NxFOdP2Q", default=None)
    next_forecast_np_2q: JQuantsDecimal = Field(alias="NxFNp2Q", default=None)
    next_forecast_eps_2q: JQuantsDecimal = Field(alias="NxFEPS2Q", default=None)

    # === Current FY Forecast (Full Year) ===
    forecast_sales: JQuantsDecimal = Field(alias="FSales", default=None)
    forecast_op: JQuantsDecimal = Field(alias="FOP", default=None)
    forecast_odp: JQuantsDecimal = Field(alias="FOdP", default=None)
    forecast_np: JQuantsDecimal = Field(alias="FNP", default=None)
    forecast_eps: JQuantsDecimal = Field(alias="FEPS", default=None)

    # === Next FY Forecast (Full Year) ===
    next_forecast_sales: JQuantsDecimal = Field(alias="NxFSales", default=None)
    next_forecast_op: JQuantsDecimal = Field(alias="NxFOP", default=None)
    next_forecast_odp: JQuantsDecimal = Field(alias="NxFOdP", default=None)
    next_forecast_np: JQuantsDecimal = Field(alias="NxFNp", default=None)
    next_forecast_eps: JQuantsDecimal = Field(alias="NxFEPS", default=None)

    # === Change Flags ===
    material_change_subsidiaries: str | None = Field(alias="MatChgSub", default=None)
    significant_change_in_scope: str | None = Field(alias="SigChgInC", default=None)
    change_by_accounting_standard_revision: str | None = Field(alias="ChgByASRev", default=None)
    change_not_accounting_standard_revision: str | None = Field(alias="ChgNoASRev", default=None)
    change_in_accounting_estimates: str | None = Field(alias="ChgAcEst", default=None)
    retrospective_restatement: str | None = Field(alias="RetroRst", default=None)

    # === Share Data ===
    shares_outstanding_fy: JQuantsDecimal = Field(alias="ShOutFY", default=None)
    treasury_shares_fy: JQuantsDecimal = Field(alias="TrShFY", default=None)
    average_shares: JQuantsDecimal = Field(alias="AvgSh", default=None)

    # === Non-Consolidated Actuals ===
    nc_sales: JQuantsDecimal = Field(alias="NCSales", default=None)
    nc_op: JQuantsDecimal = Field(alias="NCOP", default=None)
    nc_odp: JQuantsDecimal = Field(alias="NCOdP", default=None)
    nc_np: JQuantsDecimal = Field(alias="NCNP", default=None)
    nc_eps: JQuantsDecimal = Field(alias="NCEPS", default=None)
    nc_ta: JQuantsDecimal = Field(alias="NCTA", default=None)
    nc_eq: JQuantsDecimal = Field(alias="NCEq", default=None)
    nc_eq_ratio: JQuantsDecimal = Field(alias="NCEqAR", default=None)
    nc_bps: JQuantsDecimal = Field(alias="NCBPS", default=None)

    # === Non-Consolidated Current FY Forecast (2Q) ===
    forecast_nc_sales_2q: JQuantsDecimal = Field(alias="FNCSales2Q", default=None)
    forecast_nc_op_2q: JQuantsDecimal = Field(alias="FNCOP2Q", default=None)
    forecast_nc_odp_2q: JQuantsDecimal = Field(alias="FNCOdP2Q", default=None)
    forecast_nc_np_2q: JQuantsDecimal = Field(alias="FNCNP2Q", default=None)
    forecast_nc_eps_2q: JQuantsDecimal = Field(alias="FNCEPS2Q", default=None)

    # === Non-Consolidated Next FY Forecast (2Q) ===
    next_forecast_nc_sales_2q: JQuantsDecimal = Field(alias="NxFNCSales2Q", default=None)
    next_forecast_nc_op_2q: JQuantsDecimal = Field(alias="NxFNCOP2Q", default=None)
    next_forecast_nc_odp_2q: JQuantsDecimal = Field(alias="NxFNCOdP2Q", default=None)
    next_forecast_nc_np_2q: JQuantsDecimal = Field(alias="NxFNCNP2Q", default=None)
    next_forecast_nc_eps_2q: JQuantsDecimal = Field(alias="NxFNCEPS2Q", default=None)

    # === Non-Consolidated Current FY Forecast (Full Year) ===
    forecast_nc_sales: JQuantsDecimal = Field(alias="FNCSales", default=None)
    forecast_nc_op: JQuantsDecimal = Field(alias="FNCOP", default=None)
    forecast_nc_odp: JQuantsDecimal = Field(alias="FNCOdP", default=None)
    forecast_nc_np: JQuantsDecimal = Field(alias="FNCNP", default=None)
    forecast_nc_eps: JQuantsDecimal = Field(alias="FNCEPS", default=None)

    # === Non-Consolidated Next FY Forecast (Full Year) ===
    next_forecast_nc_sales: JQuantsDecimal = Field(alias="NxFNCSales", default=None)
    next_forecast_nc_op: JQuantsDecimal = Field(alias="NxFNCOP", default=None)
    next_forecast_nc_odp: JQuantsDecimal = Field(alias="NxFNCOdP", default=None)
    next_forecast_nc_np: JQuantsDecimal = Field(alias="NxFNCNP", default=None)
    next_forecast_nc_eps: JQuantsDecimal = Field(alias="NxFNCEPS", default=None)


class Dividend(BaseModel):
    """Dividend data."""

    code: str = Field(alias="Code")
    record_date: JQuantsDate = Field(alias="RecordDate")
    ex_dividend_date: JQuantsDateOptional = Field(alias="ExDividendDate", default=None)
    payment_date: JQuantsDateOptional = Field(alias="PaymentDate", default=None)
    dividend_per_share: JQuantsDecimalRequired = Field(alias="DividendPerShare")


class EarningsAnnouncement(BaseModel):
    """Earnings announcement calendar entry (V2 API abbreviated field names)."""

    code: str = Field(alias="Code")
    company_name: str = Field(alias="CoName")
    announcement_date: JQuantsDate = Field(alias="Date")
    fiscal_year: str | None = Field(alias="FY", default=None)
    fiscal_quarter: str | None = Field(alias="FQ", default=None)
    sector_name: str | None = Field(alias="SectorNm", default=None)
    section: str | None = Field(alias="Section", default=None)


class FinancialDetails(BaseModel):
    """Full financial statement data (BS/PL/CF).

    Provides detailed balance sheet, income statement, and cash flow data.
    """

    code: str = Field(alias="LocalCode")
    disclosed_date: JQuantsDate = Field(alias="DisclosedDate")
    type_of_document: str | None = Field(alias="TypeOfDocument", default=None)

    # Balance Sheet
    total_assets: JQuantsDecimal = Field(alias="TotalAssets", default=None)
    total_liabilities: JQuantsDecimal = Field(alias="TotalLiabilities", default=None)
    net_assets: JQuantsDecimal = Field(alias="NetAssets", default=None)
    current_assets: JQuantsDecimal = Field(alias="CurrentAssets", default=None)
    non_current_assets: JQuantsDecimal = Field(alias="NoncurrentAssets", default=None)
    current_liabilities: JQuantsDecimal = Field(alias="CurrentLiabilities", default=None)
    non_current_liabilities: JQuantsDecimal = Field(
        alias="NoncurrentLiabilities", default=None
    )

    # Income Statement
    net_sales: JQuantsDecimal = Field(alias="NetSales", default=None)
    cost_of_sales: JQuantsDecimal = Field(alias="CostOfSales", default=None)
    gross_profit: JQuantsDecimal = Field(alias="GrossProfit", default=None)
    operating_profit: JQuantsDecimal = Field(alias="OperatingProfit", default=None)
    ordinary_profit: JQuantsDecimal = Field(alias="OrdinaryProfit", default=None)
    profit_before_tax: JQuantsDecimal = Field(alias="ProfitBeforeTax", default=None)
    profit: JQuantsDecimal = Field(alias="Profit", default=None)

    # Cash Flow
    cf_operating: JQuantsDecimal = Field(
        alias="CashFlowsFromOperatingActivities", default=None
    )
    cf_investing: JQuantsDecimal = Field(
        alias="CashFlowsFromInvestingActivities", default=None
    )
    cf_financing: JQuantsDecimal = Field(
        alias="CashFlowsFromFinancingActivities", default=None
    )
    cash_end_of_period: JQuantsDecimal = Field(
        alias="CashAndCashEquivalents", default=None
    )
