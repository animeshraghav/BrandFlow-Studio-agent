# Common utilities and stubs used by agents
# File: agents/common.py
from __future__ import annotations
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import uuid
import time

logger = logging.getLogger("brandflow.agents")
logging.basicConfig(level=logging.INFO)


class LLMClient:
    """Minimal LLM client interface (wrap your favorite LLM SDK here).

    Implement `.generate(prompt, **kwargs)` to call the LLM and return a string.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        # Replace this with actual SDK call, e.g., OpenAI, Anthropic, Vertex, etc.
        logger.info("[LLMClient] generate called (stub). Model=%s", self.model)
        return f"[LLM_RESPONSE_PLACEHOLDER]\nPrompt received:\n{prompt[:400]}"


class ToolClient:
    """Minimal interface for external tools: search, image generation, code exec, etc.

    You can extend this class to call actual APIs.
    """

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info("[ToolClient] search stub for: %s", query)
        return []

    def generate_image(self, prompt: str, n: int = 1, size: str = "1024x1024") -> List[bytes]:
        logger.info("[ToolClient] generate_image stub for: %s", prompt)
        return []

    def run_code(self, code: str) -> str:
        logger.info("[ToolClient] run_code stub")
        return "# code exec result (stub)"


# Domain dataclasses
@dataclass
class CompetitorSummary:
    name: str
    top_headlines: List[str]
    tone: Optional[str] = None
    urls: List[str] = None


@dataclass
class ResearchOutput:
    competitors: List[CompetitorSummary]
    keywords: List[str]
    top_refs: List[str]
    summary: str


@dataclass
class BrandProfile:
    id: str
    name: str
    mission: str
    tone: List[str]
    dos: List[str]
    donts: List[str]
    tagline: str
    palette: List[str]
    fonts: List[str]
    logo_concepts: List[Dict[str, str]]


@dataclass
class Draft:
    id: str
    slug: str
    title: str
    content: str
    metadata: Dict[str, Any]


@dataclass
class SEOReport:
    title: str
    meta_description: str
    seo_score: float
    suggestions: List[str]


@dataclass
class EvaluationReport:
    readability_score: float
    brand_consistency_score: float
    seo_score: float
    overall_score: float
    notes: List[str]


# Utilities

def make_id(prefix: str = "item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"