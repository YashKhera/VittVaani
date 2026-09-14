from typing import List

from pydantic import BaseModel


class UnderstandRequest(BaseModel):
    description: str = ""


class UnderstandResponse(BaseModel):
    sector: str | None = None
    tags: List[str] = []
    summary_en: str = ""
    summary_hi: str = ""
    provider: str = "builtin"


class ConfirmUnderstandingRequest(BaseModel):
    description: str | None = None
    sector: str | None = None
    tags: List[str] = []
    summary_en: str = ""
    summary_hi: str = ""