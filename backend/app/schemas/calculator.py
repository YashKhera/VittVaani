from typing import List, Optional

from pydantic import BaseModel, Field


class CalculatorRequest(BaseModel):
    project_cost: float = Field(..., gt=0, description="Total project cost in INR")
    interest_rate_annual: float = Field(..., ge=0, le=100, description="Annual interest rate (percent)")
    tenure_months: int = Field(..., ge=1, le=360, description="Repayment tenure in months")
    coverage_percent: float = Field(100.0, ge=0, le=100, description="% of project cost financed")
    moratorium_months: int = Field(0, ge=0, le=60, description="Moratorium months before repayment")
    subsidy_amount: float = Field(0.0, ge=0, description="Up-front subsidy applied to principal")
    upfront_payment: float = Field(0.0, ge=0, description="User's own contribution reducing principal")


class SchemeCalculatorRequest(BaseModel):
    scheme_ids: List[int] = Field(..., min_length=1, max_length=10)
    project_cost: float = Field(..., gt=0)
    tenure_months: int = Field(..., ge=1, le=360)
    default_coverage_percent: float = Field(100.0, ge=0, le=100)


class AmortizationRowOut(BaseModel):
    month: int
    opening_balance: float
    emi: float
    interest: float
    principal: float
    closing_balance: float


class CalculatorResponse(BaseModel):
    project_cost: float
    coverage_percent: float
    financed_amount: float
    subsidy_amount: float
    upfront_payment: float
    moratorium_months: int
    moratorium_interest: float
    tenure_months: int
    interest_rate: float
    emi: float
    total_interest: float
    total_payment: float
    effective_rate_note: Optional[str] = None
    amortization: List[AmortizationRowOut] = []


class SchemeCalcItem(BaseModel):
    scheme_id: int
    scheme_name: str
    interest_rate: float
    moratorium_months: int
    coverage_percent: float
    financed_amount: float
    emi: float
    total_interest: float
    total_payment: float


class SchemeCalculatorResponse(BaseModel):
    project_cost: float
    tenure_months: int
    items: List[SchemeCalcItem]