# reading_history.py
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, cast

from tarotai.core.types import Reading, SpreadPosition


class ReadingHistoryManager:
    def __init__(self, history_file: Path = Path("data/readings.json")):
        self.history_file = history_file
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps({"readings": [], "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }}, indent=2))

    def add_reading(self, reading: Reading) -> None:
        """Add a new reading to history."""
        data = self._load_history()
        reading_dict = reading.dict()
        reading_dict['timestamp'] = datetime.now().isoformat()
        data["readings"].append(reading_dict)
        self._save_history(data)

    def get_readings_for_card(self, card_name: str) -> List[Reading]:
        """Retrieve all readings containing a specific card."""
        data = self._load_history()
        return [
            Reading(**r) for r in data["readings"]
            if any(c.name == card_name for c in Reading(**r).cards)
        ]

    def get_card_statistics(self, card_name: str) -> Dict[str, Any]:
        """Get usage statistics for a specific card."""
        readings = self.get_readings_for_card(card_name)
        return {
            "total_appearances": len(readings),
            "positions": self._analyze_positions(readings, card_name),
            "average_resonance": self._calculate_average_resonance(readings),
            "common_contexts": self._analyze_contexts(readings)
        }

    def _load_history(self) -> Dict[str, Any]:
        """Load reading history from file."""
        return json.loads(self.history_file.read_text())

    def _save_history(self, data: Dict[str, Any]) -> None:
        """Save reading history to file."""
        self.history_file.write_text(json.dumps(data, indent=2))

    def _analyze_positions(self, readings: List[Reading], card_name: str) -> Dict[str, int]:
        """Analyze in which positions the card appears most frequently."""
        position_counts: Dict[str, int] = {}
        for reading in readings:
            for card, position in zip(reading.cards, reading.positions):
                if card.name == card_name:
                    pos_name = cast(SpreadPosition, position).name
                    position_counts[pos_name] = position_counts.get(pos_name, 0) + 1
        return position_counts

    def _calculate_average_resonance(self, readings: List[Reading]) -> float:
        """Calculate average resonance score for readings."""
        scores = [r.resonance_score for r in readings if r.resonance_score is not None]
        return sum(scores) / len(scores) if scores else 0.0

    def _analyze_contexts(self, readings: List[Reading]) -> Dict[str, int]:
        """Analyze common question contexts."""
        context_counts: Dict[str, int] = {}
        for reading in readings:
            context = reading.question
            context_counts[context] = context_counts.get(context, 0) + 1
        return context_counts
