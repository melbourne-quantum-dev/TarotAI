from pydantic import BaseModel
from typing import List, Dict, Any

class ReadingHistory(BaseModel):
    readings: List[Dict[str, Any]]
