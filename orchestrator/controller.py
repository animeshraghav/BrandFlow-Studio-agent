from agents import (
    ResearchAgent,
    BrandDesignAgent,
    DraftAgent,
    EditorAgent,
    SEOAgent,
    VisualAgent,
    EvaluatorAgent,
)

from tools import GoogleLLMClient, GoogleToolClient
from agents.common import logger as log
from .session import InMemorySessionService
from .pipeline import PipelineOrchestrator

class BrandFlowController:
    """
    Top-level controller that instantiates:

      - Session
      - Tools (Google)
      - Agents (multi-agent system)
      - Orchestrator instance
    """

    def __init__(self, llm_client_cls, tool_client_cls, agent_classes):
        self.session = InMemorySessionService()

        # Init clients
        llm = llm_client_cls()
        tools = tool_client_cls()
        evaluator = agent_classes["evaluator"]()

        # Init agents
        self.agents = {
            "research": agent_classes["research"](llm, tools),
            "brand": agent_classes["brand"](llm, tools),
            "draft": agent_classes["draft"](llm),
            "editor": agent_classes["editor"](llm, evaluator),
            "seo": agent_classes["seo"](llm, tools),
            "visual": agent_classes["visual"](tools),
            "evaluator": evaluator,
        }

        self.orchestrator = PipelineOrchestrator(self.session, self.agents)

    def run(self, brief, topic):
        log.info("Starting pipeline...")
        return self.orchestrator.run_full(brief, topic)
