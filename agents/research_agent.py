from dataclasses import asdict
from typing import Iterable

# local import for a single-file doc; in real repo use: from agents.common import LLMClient, ToolClient, ResearchOutput, CompetitorSummary, logger

# Rebind names (for single-file readability)
LLMClient = globals()['LLMClient']
ToolClient = globals()['ToolClient']
ResearchOutput = globals()['ResearchOutput']
CompetitorSummary = globals()['CompetitorSummary']
logger = globals()['logger']


class ResearchAgent:
    """Research Agent: gathers competitor context, keywords and topical references.

    - Uses ToolClient.search for quick web evidence
    - Uses LLM to synthesize a concise research summary
    """

    def __init__(self, llm: LLMClient, tools: ToolClient):
        self.llm = llm
        self.tools = tools

    def run(self, brief: Dict[str, Any], max_competitors: int = 3) -> ResearchOutput:
        query = brief.get("industry") or brief.get("topic") or brief.get("description", "")
        logger.info("[ResearchAgent] running research for: %s", query)

        # 1) quick search
        search_results = self.tools.search(query, top_k=10)
        # For simplicity make competitor stubs from search results
        competitors = []
        for r in (search_results[:max_competitors] or []):
            name = r.get("title", "unknown")[:60]
            competitors.append(CompetitorSummary(name=name, top_headlines=[name], tone=None, urls=[r.get("url")]))

        # 2) extract keywords with LLM
        prompt_kw = (
            f"Extract the top 8 SEO keywords and short search-intent labels from the following brief:\n{brief}\nReturn a JSON list of keywords."
        )
        kw_text = self.llm.generate(prompt_kw, max_tokens=200)
        # naive parsing: split by newlines
        keywords = [k.strip() for k in kw_text.splitlines() if k.strip()][:8]

        # 3) generate research summary
        prompt_summary = (
            f"Synthesize a concise research summary for the brief below. Include 3 quick insights and recommended content angles.\n\nBRIEF:\n{brief}\n\nUse bullet points."
        )
        summary = self.llm.generate(prompt_summary, max_tokens=400)

        research = ResearchOutput(competitors=competitors, keywords=keywords, top_refs=[], summary=summary)
        logger.info("[ResearchAgent] completed research: %s", {"keywords": keywords})
        return research