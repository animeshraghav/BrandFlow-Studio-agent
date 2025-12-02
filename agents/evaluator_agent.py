from agents.common import Draft, BrandProfile, EvaluationReport, logger, LLMClient, ToolClient
from agents.research_agent import ResearchAgent
from agents.brand_design_agent import BrandDesignAgent
from agents.draft_agent import DraftAgent
from agents.editor_agent import EditorAgent
from agents.seo_agent import SEOAgent
from agents.visual_agent import VisualAgent

class EvaluatorAgent:
    """Evaluator Agent: computes automated scores for readability, brand consistency and SEO.

    This is intentionally light-weight and replaceable by stronger metrics.
    """

    def __init__(self):
        pass

    def readability(self, text: str) -> float:
        # naive proxy: shorter average sentence -> higher score (stub)
        sentences = [s for s in text.split('.') if s.strip()]
        avg_len = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        score = max(0.0, min(1.0, 1.0 - (avg_len - 20) / 60))
        return score

    def brand_consistency(self, text: str, brand: BrandProfile) -> float:
        # placeholder: check presence of brand tagline or mission words
        hit = 1 if brand.tagline.lower().split()[0] in text.lower() else 0
        return 0.6 + 0.4 * hit

    def evaluate_content(self, draft: Draft, brand: BrandProfile) -> EvaluationReport:
        r = self.readability(draft.content)
        b = self.brand_consistency(draft.content, brand)
        s = 0.75  # placeholder seo score
        overall = (r * 0.4) + (b * 0.3) + (s * 0.3)
        notes = ["automated evaluation (stub)"]
        report = EvaluationReport(readability_score=r, brand_consistency_score=b, seo_score=s, overall_score=overall, notes=notes)
        logger.info("[EvaluatorAgent] evaluated draft id=%s => overall=%.3f", draft.id, overall)
        return report


# End of agents bundle
# Each agent is intentionally SDK-agnostic and expects concrete implementations of LLMClient and ToolClient in production.

# Example usage snippet (if run as a module)
if __name__ == "__main__":
    # Instantiate stubs
    llm = LLMClient()
    tools = ToolClient()
    evaluator = EvaluatorAgent()

    # Quick demo flow
    research_agent = ResearchAgent(llm=llm, tools=tools)
    brand_agent = BrandDesignAgent(llm=llm, tools=tools)
    draft_agent = DraftAgent(llm=llm)
    editor_agent = EditorAgent(llm=llm, evaluator=evaluator)
    seo_agent = SEOAgent(llm=llm, tools=tools)
    visual_agent = VisualAgent(tools=tools)

    brief = {"company_name": "Acme Widgets", "industry": "small business marketing", "description": "A startup that sells helpful widgets"}
    research = research_agent.run(brief)
    brand = brand_agent.run(brief, research)
    draft = draft_agent.run_blog(brand_compact={"tone": brand.tone}, title="How Widgets Help Startups", keywords=research.keywords)
    edited = editor_agent.run(draft, brand)
    seo = seo_agent.run(edited, research.keywords)
    logos = visual_agent.run_logo_variants(brand)
    eval_report = evaluator.evaluate_content(edited, brand)

    print("Demo finished. Brand ID:", brand.id)
