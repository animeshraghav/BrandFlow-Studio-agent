LLMClient = globals()['LLMClient']
Draft = globals()['Draft']
EvaluationReport = globals()['EvaluationReport']
logger = globals()['logger']


class EditorAgent:
    """Editor Agent: refines drafts to adhere to brand voice, readability and constraints.

    It can run loop iterations and return a changelog.
    """

    def __init__(self, llm: LLMClient, evaluator: "EvaluatorAgent"):
        self.llm = llm
        self.evaluator = evaluator

    def run(self, draft: Draft, brand_profile: BrandProfile, max_iters: int = 2, threshold: float = 0.7) -> Draft:
        logger.info("[EditorAgent] editing draft id=%s", draft.id)
        current = draft
        for i in range(max_iters):
            prompt = (
                f"You are an editor that must make the draft follow the brand profile and dos/donts.\n"
                f"Brand mission: {brand_profile.mission}\nDos: {brand_profile.dos}\nDonts: {brand_profile.donts}\n"
                f"Draft begin:\n{current.content}\nEnd draft.\nReturn the edited markdown and a short changelog."
            )
            res = self.llm.generate(prompt, max_tokens=800)
            # naive split: last line considered changelog in this stub
            edited = res
            current = Draft(id=current.id, slug=current.slug, title=current.title, content=edited, metadata=current.metadata)

            # Evaluate
            report = self.evaluator.evaluate_content(current, brand_profile)
            logger.info("[EditorAgent] iteration %d score=%.3f", i + 1, report.overall_score)
            if report.overall_score >= threshold:
                break

        return current