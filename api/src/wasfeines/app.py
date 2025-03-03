from typing import List

from fastapi import FastAPI, Request

from wasfeines.models import Recipe, Ingredient

recipes = [
    Recipe(
        name="Spaghetti Carbonara", 
        description="Spaghetti Carbonara ist ein italienisches Nudelgericht aus Spaghetti, Speck, Eiern, Käse und Pfeffer.",
        ingredients=[
            Ingredient(name="Spaghetti", description="Spaghetti sind eine", amount=500, unit="g"),
            Ingredient(name="Eier", description="Eier sind", amount=2, unit="pcs"),
            Ingredient(name="Speck", description="Speck ist", amount=100, unit="g"),
        ]
    ),
    Recipe(
        name="Lasagne", 
        description="Lasagne ist ein Nudelauflauf aus Italien. Die klassische Lasagne alla bolognese wird mit Fleischsauce, Béchamelsauce und Parmesan zubereitet.",
        ingredients=[
            Ingredient(name="Lasagneplatten", description="Lasagneplatten sind", amount=250, unit="g"),
            Ingredient(name="Hackfleisch", description="Hackfleisch ist", amount=500, unit="g"),
            Ingredient(name="Tomaten", description="Tomaten sind", amount=400, unit="g"),
        ]
    ),
]

app = FastAPI()

@app.get("/api/v1/recipes")
async def get_recipes(request: Request) -> List[Recipe]:
    return recipes