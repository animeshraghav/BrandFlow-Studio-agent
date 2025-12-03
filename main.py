from dotenv import load_dotenv
load_dotenv()

from orchestrator.controller import BrandFlowController
from tools.google_llm import GoogleLLMClient
from tools.tool_client import GoogleToolClient
from agents import *


def main():
    brief = {
        "industry": "technology consulting","audience": "startup founders",
        }
    topic = "How AI Agents Will Transform Startups in 2025"
    
    agent_classes = {
        "research": ResearchAgent,
        "brand": BrandDesignAgent,
        "draft": DraftAgent,
        "editor": EditorAgent,
        "seo": SEOAgent,
        "visual": VisualAgent,
        "evaluator": EvaluatorAgent,
    }


    controller = BrandFlowController(GoogleLLMClient, GoogleToolClient, agent_classes)
    result = controller.run(brief, topic)
    print("--- BrandFlow Output ---")
    for k, v in result.items():
        print(f"{k.upper()}:", v, "")


if __name__ == "__main__":
    main()