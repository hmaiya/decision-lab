"""
openrouter.py: one small client for every agent and for the Decision Lab runner.

- jev(state, questions)      -> TypeSafe Jev via OpenRouter's Decisions route
- chat(model, messages)      -> any frontier model via OpenRouter chat completions

The key comes from OPENROUTER_API_KEY, or from a key file
(OPENROUTER_KEY_FILE, or ~/.config/openrouter/key). It is never printed.
"""
import json
import os
import time
import urllib.error
import urllib.request

KEY_FILES = [
    os.environ.get("OPENROUTER_KEY_FILE", ""),
    os.path.expanduser("~/.config/openrouter/key"),
]
JEV_URL = "https://openrouter.ai/api/alpha/decisions"
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_key():
    # Step 1: an environment variable wins.
    if os.environ.get("OPENROUTER_API_KEY", "").strip():
        return os.environ["OPENROUTER_API_KEY"].strip()
    # Step 2: otherwise, the first non-empty key file.
    for path in KEY_FILES:
        if path and os.path.isfile(path):
            key = open(path).read().strip()
            if key:
                return key
    raise RuntimeError("No OpenRouter key. Set OPENROUTER_API_KEY or write it to ~/.config/openrouter/key")


def _post(url, body, timeout):
    # Step 3: POST JSON, time it, and hide the key from any error text.
    key = load_key()
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "X-Title": "Decision Lab",
    })
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "ms": (time.perf_counter() - started) * 1000, "data": data}
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace").replace(key, "[key hidden]")
        return {"ok": False, "ms": (time.perf_counter() - started) * 1000, "status": e.code, "error": text}
    except Exception as e:
        return {"ok": False, "ms": (time.perf_counter() - started) * 1000, "status": None,
                "error": f"{type(e).__name__}: {e}".replace(key, "[key hidden]")}


def jev(state, questions, model="typesafe/jev-1.13", timeout=30):
    """Ask Jev typed questions. Returns {ok, ms, data:{answers, usage, model}}."""
    return _post(JEV_URL, {"model": model, "state": state, "questions": questions}, timeout)


def chat(model, messages, max_tokens=50, timeout=90, **extra):
    """Call a chat model. usage.cost is OpenRouter's billed cost in USD."""
    body = {"model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": 0, "usage": {"include": True}}
    body.update(extra)
    return _post(CHAT_URL, body, timeout)
