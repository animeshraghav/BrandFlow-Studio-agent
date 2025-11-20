

# Rebind names
LLMClient = globals()['LLMClient']
ToolClient = globals()['ToolClient']
BrandProfile = globals()['BrandProfile']
make_id = globals()['make_id']
logger = globals()['logger']


class BrandDesignAgent:
    """Brand Design Agent: creates a brand profile, palette, tagline and simple logo concepts.

    - Uses LLM for brand copy & dos/don'ts
    - Uses ToolClient.generate_image to create logo concept images (optional)
    """

    def __init__(self, llm: LLMClient, tools: ToolClient):
        self.llm = llm
        self.tools = tools

    def run(self, brief: Dict[str, Any], research: ResearchOutput) -> BrandProfile:
        company_name = brief.get("company_name") or brief.get("name") or "MyBrand"
        logger.info("[BrandDesignAgent] designing brand for: %s", company_name)

        prompt = (
            f"You are a senior brand strategist. Using the research summary: {research.summary}\n\n"
            f"Create a brand profile for the company named '{company_name}'. Provide:\n"
            "1) 1-sentence mission\n2) Tone (3 words)\n3) 5 dos and 5 donts\n4) Tagline (1 line)\n5) Color palette (3 hex codes)\n6) Font suggestions (2)\nReturn JSON only."
        )
        json_text = self.llm.generate(prompt, max_tokens=400)
        # NOTE: production code should parse JSON safely. Here we create a simple profile.

        # Simple heuristic parse: keep placeholders and use LLM text as mission
        mission = json_text.splitlines()[0] if json_text else f"{company_name} mission"

        profile = BrandProfile(
            id=make_id("brand"),
            name=company_name,
            mission=mission,
            tone=["friendly", "clear", "confident"],
            dos=["be concise", "use active voice", "provide examples", "focus on benefits", "use brand words"],
            donts=["use jargon", "be passive", "overpromise", "repeat", "use excessive adjectives"],
            tagline=brief.get("short_tagline") or "Your story, better.",
            palette=["#0f172a", "#06b6d4", "#f97316"],
            fonts=["Inter", "Merriweather"],
            logo_concepts=[{"id": make_id("logo"), "prompt": f"Logo idea for {company_name} - modern, minimal"}]
        )

        # Optionally call image generator for each logo concept
        for concept in profile.logo_concepts:
            prompt_img = concept["prompt"]
            imgs = self.tools.generate_image(prompt_img, n=2)
            # store placeholders (actual bytes would be stored in asset store)
            concept["images"] = ["<binary_image_placeholder>" for _ in imgs]

        logger.info("[BrandDesignAgent] created brand profile id=%s", profile.id)
        return profile
