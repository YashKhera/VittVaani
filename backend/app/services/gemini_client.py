import json
import urllib.error
import urllib.request

from app.config import settings

_INTERACTIONS_API = "https://generativelanguage.googleapis.com/v1beta/interactions"
_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "sector": {"type": "string", "nullable": True},
        "tags": {"type": "array", "items": {"type": "string"}},
        "summary_en": {"type": "string"},
        "summary_hi": {"type": "string"},
    },
    "required": ["sector", "tags", "summary_en", "summary_hi"],
}


def is_agent_model(model: str) -> bool:
    return bool(model) and "antigravity" in model.lower()


def _call_generate_content(prompt: str, max_tokens: int) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    )
    for use_json_mode in (True, False):
        generation_config = {"maxOutputTokens": max_tokens}
        if use_json_mode:
            generation_config["responseMimeType"] = "application/json"
        body = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 400 and use_json_mode:
                continue
            return ""
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError):
            return ""
    return ""


def _call_interactions(prompt: str, max_tokens: int) -> str:
    body = json.dumps({
        "agent": settings.GEMINI_MODEL,
        "input": prompt,
        "environment": "remote",
        "response_format": {"type": "object", "json_schema": _JSON_SCHEMA},
    }).encode("utf-8")
    req = urllib.request.Request(
        _INTERACTIONS_API,
        data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": settings.GEMINI_API_KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return ""
    if data.get("status") == "completed":
        if data.get("output_text"):
            return data["output_text"]
        steps = data.get("steps") or []
        for step in reversed(steps):
            if step.get("type") == "model_output":
                content = step.get("content") or []
                if content and content[0].get("text"):
                    return content[0]["text"]
    return ""


def call_gemini_text(prompt: str, max_tokens: int = 2000) -> str:
    if not settings.GEMINI_API_KEY:
        return ""
    if is_agent_model(settings.GEMINI_MODEL):
        return _call_interactions(prompt, max_tokens)
    return _call_generate_content(prompt, max_tokens)