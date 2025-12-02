from __future__ import annotations
import logging
from typing import Dict, Any
from agents.research_agent import ResearchAgent
from agents.brand_design_agent import BrandDesignAgent
from agents.draft_agent import DraftAgent
from agents.editor_agent import EditorAgent
from agents.seo_agent import SEOAgent
from agents.visual_agent import VisualAgent
from agents.evaluator_agent import EvaluatorAgent
from tools.google_llm import GoogleLLMClient
from tools.tool_client import GoogleToolClient

logger = logging.getLogger("brandflow.orchestrator")
logging.basicConfig(level=logging.INFO)


class PipelineOrchestrator:
    """
    Controls the full BrandFlow workflow:

        1. Research Phase
        2. Brand Design
        3. Draft Generation
        4. Editing Loop (with eval)
        5. SEO Enhancement
        6. Visual Asset Generation
        7. Final Packaging

    Supports session tracking and step-by-step execution.
    """

    def __init__(self, session, agents):
        self.session = session  # SessionService
        self.research = agents["research"]
        self.brand = agents["brand"]
        self.draft = agents["draft"]
        self.editor = agents["editor"]
        self.seo = agents["seo"]
        self.visual = agents["visual"]
        self.evaluator = agents["evaluator"]

    # ------------------------------------------------------------
    # Main pipeline
    # ------------------------------------------------------------

    def run_full(self, brief: Dict[str, Any], topic: str):
        logger.info("[Pipeline] starting full BrandFlow run")

        # STEP 1: Research
        research_out = self.research.run(brief)
        self.session.save("research", research_out)

        # STEP 2: Brand Design
        brand_profile = self.brand.run(brief, research_out)
        self.session.save("brand", brand_profile)

        # STEP 3: Draft Generation
        draft = self.draft.run_blog(
            brand_compact={"tone": brand_profile.tone},
            title=topic,
            keywords=research_out.keywords
        )
        self.session.save("draft_initial", draft)

        # STEP 4: Editor Loop
        edited = self.editor.run(draft, brand_profile)
        self.session.save("draft_edited", edited)

        # STEP 5: SEO
        seo_report = self.seo.run(edited, research_out.keywords)
        self.session.save("seo", seo_report)

        # STEP 6: Visuals
        logos = self.visual.run_logo_variants(brand_profile)
        thumb = self.visual.run_thumbnail(topic, brand_profile)
        self.session.save("logos", logos)
        self.session.save("thumbnail", thumb)

        # STEP 7: Evaluation
        evaluation = self.evaluator.evaluate_content(edited, brand_profile)
        self.session.save("evaluation", evaluation)

        logger.info("[Pipeline] completed BrandFlow generation")

        return {
            "research": research_out,
            "brand": brand_profile,
            "draft_initial": draft,
            "draft_edited": edited,
            "seo": seo_report,
            "logos": logos,
            "thumbnail": thumb,
            "evaluation": evaluation,
        }