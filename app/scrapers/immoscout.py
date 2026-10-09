from __future__ import annotations

from typing import Any, Dict, List


class BaseScraper:
    source_name: str = "base"

    def __init__(self, preferences: Dict[str, Any] | None = None):
        self.preferences = preferences or {}

    def collect(self, query: str) -> List[Dict[str, Any]]:
        raise NotImplementedError
