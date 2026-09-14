from typing import Any, Dict

from pydantic import BaseModel, Field


class ProgressPayload(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0


class ProgressResponse(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0
