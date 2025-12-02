from __future__ import annotations
import os
import logging
import google.generativeai as genai

logger = logging.getLogger("brandflow.tools.llm")


class GoogleLLMClient:
    """
    Google Gemini LLM Client
    Wraps google-generativeai SDK and matches the interface expected by LLMClient.
    """

    def __init__(self, model: str = "gemini-2.0-pro-exp"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable")

        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        logger.info("[GoogleLLMClient] generating with Gemini model=%s", self.model_name)
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        return response.text or ""
