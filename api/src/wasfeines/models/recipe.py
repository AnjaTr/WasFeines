from dataclasses import dataclass
from typing import List, Literal

@dataclass
class Media:
    name: str
    content_url: str

@dataclass
class Recipe:
    name: str
    content_url: str
    media: List[Media]