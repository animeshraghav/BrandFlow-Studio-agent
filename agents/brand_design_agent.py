from typing import Dict, Any
import json
from agents.common import logger as log, BrandProfile, ResearchOutput, make_id

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

        log.info(f"[BrandDesignAgent] Designing brand identity for: {company_name}")

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

        response_text = self.llm.generate(prompt)

        # SAFE JSON PARSE
        try:
            # Clean up markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            data = json.loads(response_text)
        except Exception:
            log.warning("[BrandDesignAgent] WARNING: JSON parse failed. Using fallback defaults.")
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

            log.info(f"[BrandDesignAgent] Generating image: {concept_prompt}")

            try:
                img_bytes = self.tools.generate_image(concept_prompt)
            except Exception as e:
                log.error(f"[BrandDesignAgent] ERROR generating image: {e}")
                img_bytes = None

            # img_bytes is a list of bytes
            profile.logo_concepts.append({
                "id": make_id("logo"),
                "prompt": concept_prompt,
                "image": img_bytes[0] if img_bytes else None
            })

        log.info(f"[BrandDesignAgent] Completed profile: {profile.id}")
        return profile
