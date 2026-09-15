from typing import Any, Dict

from pydantic import BaseModel, Field


class ProgressPayload(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0


class ProgressResponse(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0


class BilingualText(BaseModel):
    en: str = ""
    hi: str = ""


class DynamicQuestionOption(BaseModel):
    value: str
    en: str = ""
    hi: str = ""


class DynamicQuestion(BaseModel):
    id: str
    type: str
    title: BilingualText
    help: BilingualText | None = None
    options: list[DynamicQuestionOption] = Field(default_factory=list)


class DynamicQuestionRequest(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)


class DynamicQuestionResponse(BaseModel):
    questions: list[DynamicQuestion] = Field(default_factory=list)
    source: str = "bank"
