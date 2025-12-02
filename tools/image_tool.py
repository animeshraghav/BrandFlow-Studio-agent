import google.generativeai as genai
import os
import logging as logger

class GoogleImageTool:
    """
    Tool that wraps Gemini's image generation capabilities.
    """

    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable")

        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def generate_image(self, prompt: str, n: int = 1, size: str = "1024x1024"):
        logger.info("[GoogleImageTool] generating %d image(s) with prompt=%s", n, prompt)

        images = []
        for _ in range(n):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "response_mime_type": "image/png",
                    }
                )
                # Return raw bytes
                # Check if we have parts
                if response.parts:
                    for part in response.parts:
                        if part.inline_data:
                            images.append(part.inline_data.data)
            except Exception as e:
                logger.error(f"[GoogleImageTool] Error generating image: {e}")
                pass

        return images