import os, httpx, logging

logger = logging.getLogger("sarvam")

SARVAM_API_URL = (os.getenv("SARVAM_API_URL") or "").strip()
SARVAM_API_KEY = (os.getenv("SARVAM_API_KEY") or "").strip()
SUMMARY_MODEL  = (os.getenv("SUMMARY_MODEL") or "").strip()

PROMPT = (
    "Summarize this resume in 5-7 crisp bullets focusing on skills, impact, and tech stack:\n\n"
)

def _bearer_headers():
    return {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json",
    }

def _parse_any(data: dict) -> str:
    # OpenAI chat style
    if isinstance(data, dict) and isinstance(data.get("choices"), list) and data["choices"]:
        msg = (data["choices"][0].get("message") or {})
        content = (msg.get("content") or "").strip()
        if content:
            return content
        # legacy text completions
        text = (data["choices"][0].get("text") or "").strip()
        if text:
            return text

    # Common custom keys
    for key in ("summary", "output", "result", "data"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    raise RuntimeError(f"Unrecognized response shape: keys={list(data.keys())[:6]}")

async def summarize_with_sarvam(text: str, timeout_s: int = 25) -> str:
    if not SARVAM_API_KEY:
        raise RuntimeError("Sarvam not configured: missing SARVAM_API_KEY")
    if not SARVAM_API_URL:
        raise RuntimeError("Sarvam not configured: missing SARVAM_API_URL")

    # Try a few payload shapes against the same URL
    attempts = []

    # 1) OpenAI chat/completions shape
    payload_chat = {
        "model": SUMMARY_MODEL or "default",
        "messages": [
            {"role": "system", "content": "You are a concise resume summarizer."},
            {"role": "user", "content": PROMPT + text[:8000]},
        ],
        "temperature": 0,
    }
    attempts.append(("chat", payload_chat))

    # 2) Plain 'prompt' (legacy completions style)
    payload_prompt = {
        "model": SUMMARY_MODEL or "default",
        "prompt": PROMPT + text[:8000],
        "temperature": 0,
        "max_tokens": 400,
    }
    attempts.append(("prompt", payload_prompt))

    # 3) Plain 'input' (some providers use this)
    payload_input = {
        "model": SUMMARY_MODEL or "default",
        "input": PROMPT + text[:8000],
    }
    attempts.append(("input", payload_input))

    # 4) Minimal 'text'
    payload_text = {
        "text": PROMPT + text[:8000],
    }
    attempts.append(("text", payload_text))

    errors = []
    async with httpx.AsyncClient(timeout=timeout_s) as client:
        for kind, payload in attempts:
            try:
                r = await client.post(SARVAM_API_URL, json=payload, headers=_bearer_headers())
                if r.status_code >= 400:
                    # log the raw body to see provider’s hint
                    logger.warning("%s attempt got %s: %s", kind, r.status_code, r.text)
                    r.raise_for_status()
                data = r.json()
                return _parse_any(data)
            except Exception as e:
                errors.append((kind, str(e)))
                continue

    raise RuntimeError(f"All Sarvam attempts failed: {errors}")
