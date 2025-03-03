from dataclasses import dataclass
from typing import List, Literal

@dataclass
class Ingredient:
    name: str
    description: str
    amount: float
    unit: Literal["g", "ml", "pcs", "tsp", "tbsp"]


@dataclass
class Recipe:
    name: str
    description: str
    ingredients: List[Ingredient]
    images: List[str] = None