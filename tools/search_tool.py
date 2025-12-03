import os
import logging
import google.generativeai as genai
import json

logger = logging.getLogger("brandflow.tools.search")

class GoogleSearchTool:
    """
    Search tool using Gemini "grounded" responses.
    This is not a full web crawler; it uses Gemini's retrieval augmentation.
    """

    def __init__(self, model: str = "gemini-2.0-pro-exp"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable")

        genai.configure(api_key=api_key)
        self.model_name = model
        # Enable Google Search tool
        # self.tools = [{'google_search': {}}]
        # Use explicit Tool object to avoid FunctionDeclaration error
        self.tools = [
            genai.protos.Tool(
                google_search_retrieval=genai.protos.GoogleSearchRetrieval()
            )
        ]
        self.model = genai.GenerativeModel(model, tools=self.tools)

    def search(self, query: str, top_k: int = 5):
        prompt = f"Search the web for: {query}. Return a list of {top_k} results with 'title' and 'url' and a brief 'snippet' for each. Return ONLY valid JSON list."

        logger.info("[GoogleSearchTool] executing search for query=%s", query)

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Clean up markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            return json.loads(text)
        except Exception as e:
            logger.warning(f"[GoogleSearchTool] Failed to search or parse results: {e}")
            return []
