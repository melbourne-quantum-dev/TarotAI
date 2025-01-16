# src/tarotai/extensions/enrichment/analyzers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from tarotai.core.types import Reading

class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, readings: List[Reading], **kwargs) -> Dict[str, Any]:
        """Base analysis method to be implemented by specific analyzers."""
        pass

    def _validate_readings(self, readings: List[Reading]) -> None:
        """Basic validation of readings data."""
        if not readings:
            raise ValueError("No readings provided for analysis")