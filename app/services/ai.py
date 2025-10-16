from typing import Optional

from openai import OpenAI

from app.core.config import settings


class AIService:
    def __init__(self, api_key: Optional[str] = None) -> None:
        key = api_key or settings.openai_api_key
        self._client = OpenAI(api_key=key) if key else None

    def generate_message(self, prompt: str) -> str:
        if not self._client:
            # Offline/dev fallback
            return f"[DEV RESPONSE] {prompt[:120]}"

        # Simple example with responses API (OpenAI v1 client)
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content or ""

