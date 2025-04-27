import asyncio
from typing import Any, Dict, List
from abc import ABC, abstractmethod
from lxml import html
import json

import anthropic

from wasfeines.settings import Settings
from wasfeines.models.draft import DraftRecipe, DraftMedia
from wasfeines.models.recipe import Recipe
from wasfeines.storage.repository import StorageRepository

class LLMRecipeService(ABC):
    async def generate_recipe_html(self, draft_recipe: DraftRecipe, draft_media: List[DraftMedia]) -> tuple[dict, str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.generate_recipe_html_sync, draft_recipe, draft_media)

    @abstractmethod
    def generate_recipe_html_sync(self, draft_recipe: DraftRecipe, draft_media: List[DraftMedia]) -> tuple[dict, str]:
        pass

class AnthropicRecipeService(LLMRecipeService):
    def __init__(self, settings: Settings, storage_repository: StorageRepository):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.storage_respository = storage_repository

    def generate_recipe_html_sync(self, draft_recipe: DraftRecipe, draft_media: List[DraftMedia]) -> tuple[dict, str]:
        main_prompt = {
            "type": "text",
            "text": f"""
                You are an expert recipe generator. Your task is to create a complete, detailed recipe based on a provided user draft.

                Keep recipes concise and simple. Prefer vegeterian or vegan options, unless the draft is clearly meat-based. 
                Put a focus on healthy ingredients and high protein content. Pay also special attention to "User content" below if supplied,
                which may also override these instructions (except formatting).

                The draft must include at least one image, everything else is optional. If only an image is provided,
                try to fill in the gaps with reasonable assumptions. The output is a complete recipe in a specific HTML format.
                The output should be a single string, starting with a <summary> tag containing a JSON object with the recipe name.
                The rest of the HTML should be a sequence of <section> tags, each for a specified purpose.
                
                Example Output File START:
                    <summary>
                        {{
                            "name": "Vegan Peanut Protein Balls"
                        }}
                    </summary>
                    <section class="recipe--header">
                        <h1>Vegan Peanut Protein Balls</h1>
                        <h2>10-15min, Snack</h2>
                    </section>

                    <section class="recipe--summary">
                        <p>Quick snack for the week.</p>
                    </section>

                    <section class="recipe--ingredients">
                        <h2>Ingredients</h2>
                        <ul>
                            <li>90g Oats</li>
                            <li>65g Mixd Nuts</li>
                            <li>20g Mixed Seeds</li>
                            <li>2 scoops Protein Powder</li>
                            <li>125g Peanutbutter</li>
                            <li>2-3 tbs Milk Alternative</li>
                        </ul>
                    </section>

                    <section class="recipe--instructions">
                        <ol>
                            <li>Blend Oats, Nuts ans Seeds.</li>
                            <li>Add Protein Powder, Peanutbutter and milk alternative.</li>
                            <li>Mix till it forms a sticky dough. (May need to add more Mikl) </li>
                            <li>Form balls and keep them in the fridge.</li>
                        </ol>
                    </section>
                Example Output File END.

                The draft recipe is as follows (images are provided separately):

                Name: {draft_recipe.name}
                Created by: {draft_recipe.created_by}
                User content: {draft_recipe.user_content}
                User tags: {draft_recipe.user_tags}
                Ratings: {draft_recipe.ratings}
                """
        }
        images = [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": media.get_url
                }
            } for media in draft_media if media.exists
        ]
        prompt_content = [main_prompt] + images
        message = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=4096,
            messages=[
                {
                    "role": "user", "content": prompt_content
                },
            ]
        )
        final_response = ""
        for block in message.content:
            if block.type == "text":
                final_response += block.text
        summary_data = {}
        try:
            tree = html.fromstring(final_response)
            summary_text = tree.xpath('//summary/text()')[0]
            summary_data = json.loads(summary_text)
        except (IndexError, ValueError) as e:
            print(f"Error parsing summary: {e}")
            pass
        return summary_data, final_response