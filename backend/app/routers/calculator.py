from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.scheme import Scheme
from app.models.user import User
from app.schemas.calculator import (
    AmortizationRowOut,
    CalculatorRequest,
    CalculatorResponse,
    SchemeCalcItem,
    SchemeCalculatorRequest,
    SchemeCalculatorResponse,
)
from app.services.calculator_service import CalculatorService, EMIInput

router = APIRouter(prefix="/calculator", tags=["calculator"])


def _scheme_rate(scheme: Scheme) -> float:
    """Pick the concessional floor rate when present, else default 7.0%."""
    if scheme.interest_rate_min is not None:
        return float(scheme.interest_rate_min)
    if scheme.interest_rate_max is not None:
        return float(scheme.interest_rate_max)
    return 7.0


def _scheme_moratorium(scheme: Scheme) -> int:
    if scheme.moratorium_min_months is not None:
        return int(scheme.moratorium_min_months)
    return int(scheme.moratorium_max_months or 0)


def _scheme_coverage(scheme: Scheme, fallback: float) -> float:
    if scheme.max_coverage_pct is not None:
        return float(scheme.max_coverage_pct)
    return fallback


@router.get("/defaults", response_model=dict)
def defaults(_: User = Depends(get_current_user)):
    return {
        "default_interest_rate": 7.0,
        "max_coverage_percent": 90.0,
        "moratorium_range_months": [0, 60],
        "tenure_range_months": [6, 120],
    }


@router.post("", response_model=CalculatorResponse)
def calculate(payload: CalculatorRequest, _: User = Depends(get_current_user)):
    data = EMIInput(
        project_cost=payload.project_cost,
        interest_rate_annual=payload.interest_rate_annual,
        tenure_months=payload.tenure_months,
        coverage_percent=payload.coverage_percent,
        moratorium_months=payload.moratorium_months,
        subsidy_amount=payload.subsidy_amount,
        upfront_payment=payload.upfront_payment,
    )
    schedule = CalculatorService.schedule(data)
    summary = CalculatorService.summarize(data, schedule)

    return CalculatorResponse(
        **summary,
        amortization=[
            AmortizationRowOut(
                month=r.month,
                opening_balance=r.opening_balance,
                emi=r.emi,
                interest=r.interest,
                principal=r.principal,
                closing_balance=r.closing_balance,
            )
            for r in schedule.rows
        ],
    )


@router.get("/schemes")
def scheme_defaults(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Compare-list schemes, personalized to the caller's eligibility.

    When the user has a profile, items carry ``eligible`` + ``match_score``
    computed with the same hard-eligibility rules as /api/recommendations
    (gender/category/state/project-type/income filters), so e.g. a male user
    never sees Mahila Samridhi Yojana pre-listed for comparison.
    Without a profile every scheme is returned with eligible=False and
    personalized=False so the UI can prompt profile completion.
    """
    from app.models.profile import EntrepreneurProfile
    from app.services.matching_service import RecommendationService

    schemes = db.query(Scheme).filter(Scheme.loan_category.isnot(None)).all()

    def _item(s: Scheme, eligible: bool, match_score: float | None) -> dict:
        return {
            "scheme_id": s.id,
            "scheme_name": s.name,
            "interest_rate": _scheme_rate(s),
            "moratorium_months": _scheme_moratorium(s),
            "coverage_percent": float(s.max_coverage_pct or 90.0),
            "tenure_max_months": s.tenure_max_months,
            "loan_min": s.loan_min,
            "loan_max": s.loan_max,
            "loan_category": s.loan_category,
            "eligible": eligible,
            "match_score": match_score,
        }

    profile = db.query(EntrepreneurProfile).filter(
        EntrepreneurProfile.user_id == current_user.id
    ).first()
    if profile is None:
        return {
            "personalized": False,
            "eligible_count": 0,
            "total": len(schemes),
            "items": [_item(s, False, None) for s in schemes],
        }

    result = RecommendationService(db).get_recommendations(
        profile=profile, min_score=40, max_results=50
    )
    rec = {r["scheme_id"]: r for r in result["recommendations"]}
    items = [_item(s, s.id in rec, rec[s.id]["match_score"] if s.id in rec else None)
             for s in schemes]
    # Eligible first (best match first), then the rest alphabetically.
    items.sort(key=lambda i: (
        0 if i["eligible"] else 1,
        -(i["match_score"] or 0),
        (i["scheme_name"] or "").lower(),
    ))
    return {
        "personalized": True,
        "eligible_count": sum(1 for i in items if i["eligible"]),
        "total": len(items),
        "items": items,
    }


@router.post("/schemes", response_model=SchemeCalculatorResponse)
def calculate_schemes(
    payload: SchemeCalculatorRequest,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items: list[SchemeCalcItem] = []
    for scheme_id in payload.scheme_ids:
        scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
        if scheme is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheme {scheme_id} not found",
            )
        rate = _scheme_rate(scheme)
        moratorium = _scheme_moratorium(scheme)
        coverage = _scheme_coverage(scheme, payload.default_coverage_percent)
        data = EMIInput(
            project_cost=payload.project_cost,
            interest_rate_annual=rate,
            tenure_months=payload.tenure_months,
            coverage_percent=coverage,
            moratorium_months=moratorium,
            subsidy_amount=0.0,
            upfront_payment=0.0,
        )
        sched = CalculatorService.schedule(data)
        items.append(SchemeCalcItem(
            scheme_id=scheme.id,
            scheme_name=scheme.name,
            interest_rate=rate,
            moratorium_months=moratorium,
            coverage_percent=coverage,
            financed_amount=sched.principal,
            emi=sched.emi,
            total_interest=sched.total_interest,
            total_payment=sched.total_payment,
        ))
    items.sort(key=lambda i: i.emi)
    return SchemeCalculatorResponse(project_cost=payload.project_cost, tenure_months=payload.tenure_months, items=items)