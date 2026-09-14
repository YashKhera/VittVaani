from app.services.ai_service import ai_service
from app.services.auth_service import AuthService
from app.services.matching_service import AdvancedMatchingService, RecommendationService
from app.services.notification_service import notification_service
from app.services.profile_service import ProfileService
from app.services.scheme_service import SchemeService

__all__ = [
    "ai_service", "AuthService", "AdvancedMatchingService", "RecommendationService",
    "notification_service", "ProfileService", "SchemeService",
]