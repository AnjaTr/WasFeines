from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DraftMedia:
    exists: bool
    get_url: str
    put_url: str
    delete_url: Optional[str] = None

@dataclass
class DraftRecipe:
    name: Optional[str]
    user_content: Optional[str]
    user_tags: Optional[List[str]]
    user_rating_anja: Optional[float]
    user_rating_georg: Optional[float]
    draft_media: List[DraftMedia]