from typing import List, Annotated

from fastapi.testclient import TestClient
import pytest

from wasfeines.llm.anthropic_recipe_service import AnthropicRecipeService, LLMRecipeService
from wasfeines.storage.repository import StorageRepository
from wasfeines.models.draft import DraftRecipe

@pytest.mark.asyncio
async def test_anthropic_recipe_service(app):
    with TestClient(app) as client:
        repo: StorageRepository = app.state.storage_repository
        draft_media = await repo.get_draft_media("g.j.grab@gmail.com")
        draft_recipe = await repo.get_draft_recipe("g.j.grab@gmail.com")
        assert draft_recipe is not None
        recipe_service: LLMRecipeService = app.state.llm_recipe_service
        summary_dict, html = recipe_service.generate_recipe_html_sync(draft_recipe, draft_media)
        assert html is not None
        if not draft_recipe.name:
            draft_recipe.name = summary_dict["name"]
        recipe = await repo.put_recipe(
            recipe=draft_recipe,
            media=draft_media,
            recipe_html=html,
        )
        assert recipe is not None
        import ipdb; ipdb.set_trace()
        await repo.delete_recipe(recipe.name)