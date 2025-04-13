from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Rating:
    created_by: str
    created_date: datetime
    rating: float
    comment: Optional[str]

@dataclass
class RatingRequestModel:
    rating: float
    comment: Optional[str]

    def to_rating(self, created_by: str) -> Rating:
        return Rating(
            created_by=created_by,
            created_date=datetime.now(),
            rating=self.rating,
            comment=self.comment
        )