from dataclasses import dataclass
from typing import List, Optional

from wasfeines.models.rating import Rating, RatingRequestModel

@dataclass
class DraftMedia:
    exists: bool
    get_url: str
    put_url: str
    delete_url: Optional[str] = None
    create_timestamp: Optional[float] = None

@dataclass
class DraftRecipeResponseModel:
    name: str
    user_content: Optional[str]
    user_tags: Optional[List[str]]
    ratings: Optional[List[Rating]]
    draft_media: List[DraftMedia]

@dataclass
class DraftRecipe:
    name: str
    created_by: str
    user_content: Optional[str]
    user_tags: Optional[List[str]]
    ratings: Optional[List[Rating]]

    def to_response_model(self, draft_media: List[DraftMedia]) -> DraftRecipeResponseModel:
        return DraftRecipeResponseModel(
            name=self.name,
            user_content=self.user_content,
            user_tags=self.user_tags,
            ratings=self.ratings,
            draft_media=draft_media
        )

@dataclass
class DraftRecipeRequestModel:
    name: Optional[str]
    user_content: Optional[str]
    user_tags: Optional[List[str]]
    user_rating: Optional[RatingRequestModel]

    def to_draft_recipe(
            self, 
            created_by: str,
        ) -> DraftRecipe:
        return DraftRecipe(
            name=self.name,
            created_by=created_by,
            user_content=self.user_content,
            user_tags=self.user_tags,
            ratings=[self.user_rating.to_rating(created_by=created_by)] if self.user_rating else None
        )