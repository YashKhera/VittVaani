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


def is_live_model(model: str) -> bool:
    """Models that only run on the real-time Live API (WebSocket).

    Covers the Live and native-audio / audio-dialog preview models, e.g.
    gemini-2.5-flash-preview-native-audio-dialog, gemini-3.1-flash-live-preview.
    These are for real-time voice agents and are NOT callable over the REST
    generateContent/interactions endpoints.
    """
    if not model:
        return False
    m = model.lower()
    return (
        "native-audio" in m
        or "audio-dialog" in m
        or m.endswith("live")
        or "-live" in m
        or m.startswith("live")
    )


def _call_live(prompt: str, max_tokens: int) -> str:
    """One-shot TEXT request over the Live API (bidiGenerateContent).

    Returns "" on any failure so callers can fall back gracefully.
    Requires `websockets`; the model must be provisioned for the account and
    support TEXT modality.
    """
    import asyncio
    import json
    import urllib.parse

    try:
        import websockets
    except ImportError:
        return ""

    url = (
        "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta."
        "GenerativeService.BidiGenerateContent?key="
        + urllib.parse.quote(settings.GEMINI_API_KEY)
    )

    async def run() -> str:
        header = {"x-goog-api-key": settings.GEMINI_API_KEY}
        async with websockets.connect(url, additional_headers=header) as ws:
            setup = {
                "setup": {
                    "model": f"models/{settings.GEMINI_MODEL}",
                    "generation_config": {
                        "response_modalities": ["TEXT"],
                        "temperature": 0.2,
                        "max_output_tokens": max_tokens,
                    },
                }
            }
            await ws.send(json.dumps(setup))
            await asyncio.wait_for(ws.recv(), timeout=120)
            await ws.send(json.dumps({
                "client_content": {
                    "turns": [{"role": "user", "parts": [{"text": prompt}]}],
                    "turn_complete": True,
                }
            }))
            chunks = []
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=120)
                data = json.loads(raw)
                sc = data.get("serverContent") or {}
                for part in sc.get("modelTurn", {}).get("parts", []):
                    if "text" in part:
                        chunks.append(part["text"])
                if sc.get("turnComplete"):
                    break
            return "".join(chunks)

    try:
        return asyncio.run(run())
    except Exception:
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
    if is_live_model(settings.GEMINI_MODEL):
        return _call_live(prompt, max_tokens)
    if is_agent_model(settings.GEMINI_MODEL):
        return _call_interactions(prompt, max_tokens)
    return _call_generate_content(prompt, max_tokens)