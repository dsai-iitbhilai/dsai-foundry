import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    """Small OpenAI-compatible wrapper (Groq by default)."""

    def __init__(self, provider: str = "groq", model: str | None = None, temperature: float = 0.0, max_tokens: int = 256):
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found. Add it in .env")
            self.client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            self.model = model or "llama-3.3-70b-versatile"
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found. Add it in .env")
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
        else:
            raise ValueError("provider must be 'groq' or 'openai'")

        self.temperature = temperature
        self.max_tokens = max_tokens
        self.total_tokens_used = 0

    def generate(self, prompt: str, stop: list[str] | None = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop,
        )

        if response.usage:
            self.total_tokens_used += response.usage.total_tokens

        return (response.choices[0].message.content or "").strip()
