"""
Minimal local stub for the `openai` package.

Provides an `OpenAI` client compatible with the usage in `first_llm_app.py`,
forwarding chat completion requests to an OpenAI-compatible HTTP API such as
Ollama running at `OLLAMA_HOST`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List
from urllib import request as _urlrequest
from urllib.error import HTTPError


@dataclass
class _Message:
    role: str
    content: str


@dataclass
class _Choice:
    message: _Message


class _Response:
    def __init__(self, choices: List[_Choice]) -> None:
        self.choices = choices


class _ChatCompletionsClient:
    def __init__(self, base_url: str) -> None:
        base = base_url.rstrip("/")
        # Primary: OpenAI-compatible endpoint (if available).
        self._primary_endpoint = base + "/v1/chat/completions"
        # Fallback: Ollama's native chat endpoint.
        self._fallback_endpoint = base + "/api/chat"

    def create(self, model: str, messages: List[Dict[str, Any]]) -> Any:
        """
        Send a chat completion request to an OpenAI-compatible endpoint.

        Returns a dict shaped similarly to the official OpenAI response so that
        `response.choices[0].message.content` works as expected.
        """
        payload = {"model": model, "messages": messages}
        data = json.dumps(payload).encode("utf-8")

        def _call(endpoint: str) -> Any:
            req = _urlrequest.Request(
                endpoint,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with _urlrequest.urlopen(req) as resp:  # type: ignore[call-arg]
                return resp.read().decode("utf-8")

        try:
            body = _call(self._primary_endpoint)
        except HTTPError as e:
            # If the OpenAI-style route is missing, fall back to Ollama's `/api/chat`.
            if e.code == 404:
                body = _call(self._fallback_endpoint)
            else:
                raise

        parsed = json.loads(body)

        # If the backend already returns an OpenAI-shaped response, adapt it.
        if isinstance(parsed, dict) and "choices" in parsed:
            raw_choices = parsed["choices"]
            choices: List[_Choice] = []
            for ch in raw_choices:
                msg = ch.get("message", {})
                choices.append(
                    _Choice(
                        message=_Message(
                            role=msg.get("role", "assistant"),
                            content=msg.get("content", ""),
                        )
                    )
                )
            return _Response(choices=choices)

        # Otherwise, wrap the backend result into a minimal OpenAI-like shape.
        content = parsed.get("message", parsed) if isinstance(parsed, dict) else parsed
        return _Response(
            choices=[_Choice(message=_Message(role="assistant", content=content))]
        )


class _ChatClient:
    def __init__(self, base_url: str) -> None:
        self.completions = _ChatCompletionsClient(base_url)


class OpenAI:
    """
    Minimal stand-in for `openai.OpenAI` with only the pieces your script uses.
    """

    def __init__(self, base_url: str) -> None:
        self.chat = _ChatClient(base_url)

