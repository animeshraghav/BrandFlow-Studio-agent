from typing import List, Dict, Any
from agents.common import LLMClient, Draft, make_id, logger

class DraftAgent:
    """Draft Agent: generates first-pass content drafts.

    Supports parallel drafting for multiple artifact types (blog, linkedin, twitter).
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def create_outline(self, topic: str, keywords: List[str]) -> str:
        prompt = f"Create an outline of 4-6 sections for a blog titled '{topic}' targeting keywords {keywords}."
        return self.llm.generate(prompt, max_tokens=200)

    def run_blog(self, brand_compact: Dict[str, Any], title: str, keywords: List[str]) -> Draft:
        logger.info("[DraftAgent] generating blog draft: %s", title)
        outline = self.create_outline(title, keywords)
        prompt = (
            f"You are a writer. Brand compact: {brand_compact}\nWrite a blog post titled '{title}'.\nUse outline:\n{outline}\nTarget keywords: {keywords}\nReturn markdown."
        )
        content = self.llm.generate(prompt, max_tokens=1200)
        draft = Draft(id=make_id("draft"), slug=title.lower().replace(" ", "-"), title=title, content=content, metadata={"outline": outline})
        logger.info("[DraftAgent] created draft id=%s", draft.id)
        return draft

    def run_social(self, brand_compact: Dict[str, Any], topic: str) -> List[Draft]:
        logger.info("[DraftAgent] generating social posts for: %s", topic)
        prompts = [
            f"Write a short LinkedIn post about {topic} in this tone: {brand_compact.get('tone')}. Include CTA.",
            f"Write three tweet-sized posts about {topic} in this tone: {brand_compact.get('tone')}.",
        ]
        drafts = []
        for p in prompts:
            content = self.llm.generate(p, max_tokens=200)
            drafts.append(Draft(id=make_id("draft"), slug=make_id("social"), title=topic, content=content, metadata={}))
        return drafts
