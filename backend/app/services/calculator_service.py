"""Financial calculation service: EMI, moratorium, amortization, coverage.

Formula used:
    EMI = P * r * (1 + r)^n / [(1 + r)^n - 1]

where P is the financed principal after applying coverage %, r is the monthly
interest rate (annual % / 12 / 100) and n is the number of monthly instalments.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class EMIInput:
    project_cost: float
    interest_rate_annual: float          # percent, e.g. 7.0
    tenure_months: int
    coverage_percent: float = 100.0      # % of project cost financed by scheme
    moratorium_months: int = 0           # months before repayment starts
    subsidy_amount: float = 0.0          # up-front amount reduced from principal
    upfront_payment: float = 0.0         # user's own contribution (reduces principal)

    @property
    def financed(self) -> float:
        base = self.project_cost * (self.coverage_percent / 100.0)
        principal = base - self.subsidy_amount - self.upfront_payment
        return max(principal, 0.0)

    @property
    def monthly_rate(self) -> float:
        return self.interest_rate_annual / 100.0 / 12.0


@dataclass
class AmortizationRow:
    month: int
    opening_balance: float
    emi: float
    interest: float
    principal: float
    closing_balance: float


@dataclass
class EMISchedule:
    principal: float
    emi: float
    total_interest: float
    total_payment: float
    moratorium_interest: float = 0.0
    rows: list[AmortizationRow] = field(default_factory=list)


def _round2(value: float) -> float:
    return round(value + 1e-9, 2)


class CalculatorService:
    """Pure financial calculations with no DB dependencies — testable."""

    MIN_INTEREST_RATE = 0.0
    MAX_INTEREST_RATE = 100.0
    MIN_TENURE = 1
    MAX_TENURE = 360
    MIN_COVERAGE = 0.0
    MAX_COVERAGE = 100.0
    MIN_MORATORIUM = 0
    MAX_MORATORIUM = 60
    MIN_PROJECT_COST = 0.0

    @staticmethod
    def validate(data: EMIInput) -> None:
        if data.project_cost < CalculatorService.MIN_PROJECT_COST:
            raise ValueError("project_cost must be >= 0")
        if not (CalculatorService.MIN_INTEREST_RATE <= data.interest_rate_annual <= CalculatorService.MAX_INTEREST_RATE):
            raise ValueError("interest_rate_annual must be between 0 and 100")
        if not (CalculatorService.MIN_TENURE <= data.tenure_months <= CalculatorService.MAX_TENURE):
            raise ValueError("tenure_months must be between 1 and 360")
        if not (CalculatorService.MIN_COVERAGE <= data.coverage_percent <= CalculatorService.MAX_COVERAGE):
            raise ValueError("coverage_percent must be between 0 and 100")
        if not (CalculatorService.MIN_MORATORIUM <= data.moratorium_months <= CalculatorService.MAX_MORATORIUM):
            raise ValueError("moratorium_months must be between 0 and 60")

    @classmethod
    def compute_emi(cls, principal: float, annual_rate: float, tenure_months: int) -> float:
        """EMI given financed principal, annual % rate and tenure in months."""
        if principal <= 0:
            return 0.0
        if tenure_months <= 0:
            raise ValueError("tenure_months must be > 0")
        r = annual_rate / 100.0 / 12.0
        if r == 0:
            return _round2(principal / tenure_months)
        factor = (1 + r) ** tenure_months
        emi = principal * r * factor / (factor - 1)
        return _round2(emi)

    @classmethod
    def moratorium_interest(cls, principal: float, annual_rate: float, moratorium_months: int) -> float:
        """Simple interest accruing during the moratorium period (added later)."""
        if principal <= 0 or moratorium_months <= 0:
            return 0.0
        r = annual_rate / 100.0 / 12.0
        total = principal * r * moratorium_months
        return _round2(total)

    @classmethod
    def schedule(cls, input_data: EMIInput) -> EMISchedule:
        cls.validate(input_data)
        principal = input_data.financed
        moratorium_interest = cls.moratorium_interest(
            principal, input_data.interest_rate_annual, input_data.moratorium_months
        )
        # Principal to amortize includes accrued moratorium interest.
        amortized_principal = principal + moratorium_interest
        emi = cls.compute_emi(
            amortized_principal, input_data.interest_rate_annual, input_data.tenure_months
        )
        if emi == 0:
            return EMISchedule(
                principal=principal, emi=0.0, total_interest=0.0, total_payment=0.0,
                moratorium_interest=moratorium_interest, rows=[],
            )

        rows: list[AmortizationRow] = []
        balance = amortized_principal
        monthly_rate = input_data.monthly_rate
        total_interest = 0.0
        for month in range(1, input_data.tenure_months + 1):
            opening = balance
            interest = _round2(balance * monthly_rate)
            principal_part = _round2(emi - interest)
            if principal_part > balance:
                principal_part = balance
                emi = _round2(interest + principal_part)
            balance = _round2(balance - principal_part)
            rows.append(AmortizationRow(
                month=month,
                opening_balance=_round2(opening),
                emi=emi,
                interest=interest,
                principal=principal_part,
                closing_balance=balance,
            ))
            total_interest += interest

        total_interest = _round2(total_interest + moratorium_interest)
        total_payment = _round2(principal + total_interest)
        return EMISchedule(
            principal=_round2(principal),
            emi=emi,
            total_interest=total_interest,
            total_payment=total_payment,
            moratorium_interest=moratorium_interest,
            rows=rows,
        )

    @classmethod
    def summarize(cls, input_data: EMIInput, schedule: EMISchedule) -> dict:
        return {
            "project_cost": _round2(input_data.project_cost),
            "coverage_percent": input_data.coverage_percent,
            "financed_amount": _round2(schedule.principal),
            "subsidy_amount": _round2(input_data.subsidy_amount),
            "upfront_payment": _round2(input_data.upfront_payment),
            "moratorium_months": input_data.moratorium_months,
            "moratorium_interest": _round2(schedule.moratorium_interest),
            "tenure_months": input_data.tenure_months,
            "interest_rate": input_data.interest_rate_annual,
            "emi": schedule.emi,
            "total_interest": schedule.total_interest,
            "total_payment": schedule.total_payment,
            "effective_rate_note": (
                "Moratorium interest added to principal before repayment begins."
                if input_data.moratorium_months > 0 else None
            ),
        }