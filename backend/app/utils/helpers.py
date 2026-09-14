from fastapi import HTTPException, status


def require_profile(profile):
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your profile first",
        )
    return profile


def normalize_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def humanize_key(key: str) -> str:
    return key.replace("_", " ").title()