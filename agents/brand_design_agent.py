from typing import Dict, Any
from utils.logger import log
from dataclasses import dataclass
import json

from models.brand_profile import BrandProfile
from models.research_output import ResearchOutput
from utils.ids import make_id


class BrandDesignAgent:
    """
    Creates brand identity elements including:
    - Mission statement
    - Tone & brand guidelines
    - Tagline
    - Palette & Fonts
    - Logo concepts (via ImageGeneratorTool)
    """

    def __init__(self, llm, tools):
        self.llm = llm            # GoogleLLMClient
        self.tools = tools        # GoogleToolClient (contains .images)

    def run(self, brief: Dict[str, Any], research: ResearchOutput) -> BrandProfile:

        company_name = (
            brief.get("company_name")
            or brief.get("name")
            or brief.get("brand_name")
            or "MyBrand"
        )

        log(f"[BrandDesignAgent] Designing brand identity for: {company_name}")

        # LLM PROMPT
        prompt = f"""
        You are a senior brand strategist.

        Based on this research:
        {research.summary}

        Create a brand identity for "{company_name}".

        Return ONLY valid JSON:
        {{
            "mission": "...",
            "tone": ["...", "...", "..."],
            "dos": ["...", "..."],
            "donts": ["...", "..."],
            "tagline": "...",
            "palette": ["#xxxxxx", "#xxxxxx", "#xxxxxx"],
            "fonts": ["Font A", "Font B"]
        }}
        """

        response_text = self.llm.run(prompt)

        # SAFE JSON PARSE
        try:
            data = json.loads(response_text)
        except Exception:
            log("[BrandDesignAgent] WARNING: JSON parse failed. Using fallback defaults.")
            data = {}

        # CREATE BRAND PROFILE OBJECT
        profile = BrandProfile(
            id=make_id("brand"),
            name=company_name,
            mission=data.get("mission", f"{company_name} creates meaningful impact."),
            tone=data.get("tone", ["friendly", "clear", "confident"]),
            dos=data.get("dos", ["be concise", "be helpful", "stay consistent"]),
            donts=data.get("donts", ["avoid jargon", "avoid filler", "avoid ambiguity"]),
            tagline=data.get("tagline", brief.get("tagline") or "Your story, better."),
            palette=data.get("palette", ["#0F172A", "#06B6D4", "#F97316"]),
            fonts=data.get("fonts", ["Inter", "Merriweather"]),
            logo_concepts=[]
        )

        # LOGO CONCEPT GENERATION
        base_prompt = f"Modern minimal vector logo for '{company_name}'"

        for i in range(2):
            concept_prompt = f"{base_prompt}, variation {i+1}"

            log(f"[BrandDesignAgent] Generating image: {concept_prompt}")

            try:
                img_bytes = self.tools.images.generate(concept_prompt)
            except Exception as e:
                log(f"[BrandDesignAgent] ERROR generating image: {e}")
                img_bytes = None

            profile.logo_concepts.append({
                "id": make_id("logo"),
                "prompt": concept_prompt,
                "image": img_bytes
            })

        log(f"[BrandDesignAgent] Completed profile: {profile.id}")
        return profile
