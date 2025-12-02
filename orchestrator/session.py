import logging
from typing import Any

logger = logging.getLogger("brandflow.orchestrator")
logging.basicConfig(level=logging.INFO)

class InMemorySessionService:
    """
    Tracks state across long-running agent executions.
    Supports pause/resume for each pipeline stage.
    """

    def __init__(self):
        self.storage = {}

    def save(self, key: str, value: Any):
        logger.info(f"[Session] saving: {key}")
        self.storage[key] = value

    def get(self, key: str):
        return self.storage.get(key)

    def all(self):
        return self.storage

