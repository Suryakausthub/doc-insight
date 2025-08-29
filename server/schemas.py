from pydantic import BaseModel
from typing import List, Tuple, Optional

class Insight(BaseModel):
    id: str
    filename: str
    summary_type: str                 # "ai" | "fallback"
    summary: Optional[str] = None
    top_words: Optional[List[Tuple[str, int]]] = None

class HistoryItem(BaseModel):
    id: str
    filename: str
    uploaded_at: str
    summary_type: str
