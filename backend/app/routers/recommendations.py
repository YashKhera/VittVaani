from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.profile import EntrepreneurProfile
from app.models.user import User
from app.schemas.recommendation import (
    MatchBreakdown, RecommendationItem, RecommendationRequest, RecommendationResponse,
)
from app.services.ai_service import ai_service
from app.services.matching_service import RecommendationService
from app.services.profile_service import ProfileService
from app.schemas.scheme import SchemeListItem

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

MAX_AI_EXPLANATIONS = 5
AI_EXPLANATION_WORKERS = 4


def _serialize(item: dict, language: str, explanation: str) -> RecommendationItem:
    scheme = item["scheme"]

    return RecommendationItem(
        scheme_id=scheme.id,
        scheme_name=scheme.name,
        match_score=item["match_score"],
        match_level=item["match_level"],
        matched_criteria=item["matched_criteria"],
        match_breakdown=MatchBreakdown(
            sector_match=item["match_breakdown"]["sector_match"],
            support_match=item["match_breakdown"]["support_match"],
            location_match=item["match_breakdown"]["location_match"],
            stage_match=item["match_breakdown"]["stage_match"],
            entrepreneur_type_match=item["match_breakdown"]["entrepreneur_type_match"],
            description_match=item["match_breakdown"].get("description_match", 0),
            targeted_match=item["match_breakdown"].get("targeted_match", 0),
            tier_match=item["match_breakdown"].get("tier_match", 0),
            total_score=item["match_score"],
        ),
        possible_gap=item["possible_gap"],
        explanation=explanation,
        funding_range=item["funding_range"],
        processing_time=item["processing_time"],
        scheme=SchemeListItem.model_validate(scheme),
    )


@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    payload: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.user_id == current_user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please complete your profile first")
    result = RecommendationService(db).get_recommendations(
        profile=profile,
        min_score=payload.min_score or 40,
        max_results=payload.max_results or 15,
        language=payload.language or "en",
        override_sector=payload.sector,
        override_state=payload.state,
        override_stage=payload.business_stage,
        override_revenue=payload.annual_revenue,
    )

    items = []
    recommended = result["recommendations"]
    language = payload.language or "en"
    if ai_service.enabled:
        with ThreadPoolExecutor(max_workers=AI_EXPLANATION_WORKERS) as pool:
            futures = {}
            for idx, item in enumerate(recommended[:MAX_AI_EXPLANATIONS]):
                future = pool.submit(
                    ai_service.generate_explanation,
                    profile,
                    item["scheme"],
                    item["matched_criteria"],
                    language,
                )
                futures[future] = idx
            explanations = {idx: "" for idx in range(len(recommended))}
            for future in futures:
                idx = futures[future]
                try:
                    explanations[idx] = future.result() or ""
                except Exception:
                    explanations[idx] = ""
        for idx, item in enumerate(recommended):
            items.append((idx, _serialize(item, language, explanations[idx])))
    else:
        for idx, item in enumerate(recommended):
            explanation = item.get("explanation") or ""
            if not explanation:
                explanation = ai_service.generate_explanation(
                    profile, item["scheme"], item["matched_criteria"], language
                )
            items.append((idx, _serialize(item, language, explanation)))
    items = [serialized for _, serialized in sorted(items)]

    return RecommendationResponse(
        recommendations=items,
        total_schemes=result["total_schemes"],
        profile_summary=result["profile_summary"],
    )