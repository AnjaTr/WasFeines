from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Media:
    name: str
    content_url: str

@dataclass
class Recipe:
    name: str
    content_url: str
    media: List[Media]
    summary: Optional[Dict[str, str | List[str] | float | int]]