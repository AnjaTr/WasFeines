from dataclasses import dataclass
from typing import List

@dataclass
class DraftMedia:
    name: str
    content_base64: str
    content_mime_type: str

@dataclass
class DraftRecipe:
    name: str
    content: str
    draft_media: List[DraftMedia]