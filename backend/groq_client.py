import json
import os
import random
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_RETRIES = int(os.getenv("GROQ_MAX_RETRIES", "3"))
BACKOFF_BASE = float(os.getenv("GROQ_BACKOFF_BASE", "0.5"))
BACKOFF_CAP = float(os.getenv("GROQ_BACKOFF_CAP", "8"))


def _parse_error_message(raw_body):
    if not raw_body:
        return ""
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body
    if isinstance(payload, dict):
        error = payload.get("error") or {}
        if isinstance(error, dict):
            return error.get("message") or raw_body
    return raw_body


def _should_retry(status_code):
    return status_code in (429, 500, 502, 503, 504)


def chat_completion(messages):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        )
    }

    print(headers) 

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    print(payload)  

    data_bytes = json.dumps(payload).encode("utf-8")

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        request = Request(GROQ_API_URL, data=data_bytes, headers=headers, method="POST")
        try:
            with urlopen(request, timeout=30) as response:
                response_body = response.read().decode("utf-8")
                data = json.loads(response_body)
                break
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8") if exc.fp else ""
            message = _parse_error_message(error_body)           
            last_error = RuntimeError(f"Groq API error: {exc.code} {message}".strip())
            if not _should_retry(exc.code) or attempt >= MAX_RETRIES:
                raise last_error from exc
        except URLError as exc:
            last_error = RuntimeError(f"Groq API connection error: {exc.reason}")
            if attempt >= MAX_RETRIES:
                raise last_error from exc

        delay = min(BACKOFF_BASE * (2 ** attempt), BACKOFF_CAP)
        delay += random.uniform(0, 0.2)
        time.sleep(delay)
    else:
        raise last_error or RuntimeError("Groq API request failed")

    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message", {})
    return {"content": message.get("content", "")}
