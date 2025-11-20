LLMClient = globals()['LLMClient']
SEOReport = globals()['SEOReport']
logger = globals()['logger']


class SEOAgent:
    """SEO Agent: optimize titles, meta descriptions, headings and compute a simple SEO score.
    """

    def __init__(self, llm: LLMClient, tools: ToolClient):
        self.llm = llm
        self.tools = tools

    def run(self, draft: Draft, keywords: List[str]) -> SEOReport:
        logger.info("[SEOAgent] optimizing draft id=%s", draft.id)
        prompt = (
            f"Given this article content:\n{draft.content}\n\nProvide an SEO-optimized title, a meta description (max 160 chars), and 3 suggested headings."
        )
        res = self.llm.generate(prompt, max_tokens=300)
        # Very naive parsing for the stub
        title = draft.title + " | BrandFlow"
        meta = (res.splitlines()[0][:160]) if res else ""
        score = 0.75  # placeholder
        suggestions = ["Use target keyword in h2", "Add internal link to cornerstone article"]
        report = SEOReport(title=title, meta_description=meta, seo_score=score, suggestions=suggestions)
        logger.info("[SEOAgent] seo_score=%.2f for draft id=%s", score, draft.id)
        return report