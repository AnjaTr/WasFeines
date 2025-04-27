from typing import List, Annotated, Any
from contextlib import asynccontextmanager
import logging
import sys

from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.oauth1.client import OAuth1Client
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import TypeAdapter

from wasfeines.models import Recipe, User
from wasfeines.models.draft import DraftMedia, DraftRecipeResponseModel, DraftRecipeRequestModel
from wasfeines.models.message import MessageResponse
from wasfeines.settings import Settings
from wasfeines.storage.repository import S3StorageRepository
from wasfeines.llm.anthropic_recipe_service import AnthropicRecipeService

log = logging.getLogger(__name__)

api_v1_router = APIRouter()

async def valid_user_session(request: Request) -> User:
    if (user := request.session.get('user')) is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return TypeAdapter(User).validate_python(user)

ValidUser = Annotated[User, Depends(valid_user_session)]

@api_v1_router.get("/recipes")
async def get_recipes(request: Request, user: ValidUser) -> List[Recipe]:
    log.info(f"User: {user}")
    repo: S3StorageRepository = request.app.state.storage_repository
    return await repo.list_recipes()

@api_v1_router.get("/draftmedia")
async def get_draft(request: Request, user: ValidUser) -> List[DraftMedia]:
    repo: S3StorageRepository = request.app.state.storage_repository
    return await repo.get_draft_media(user.email)

@api_v1_router.get('/draftrecipe', response_model=DraftRecipeResponseModel)
async def get_draft_recipe(request: Request, user: ValidUser) -> DraftRecipeResponseModel:
    repo: S3StorageRepository = request.app.state.storage_repository
    draft_recipe = await repo.get_draft_recipe(user.email)
    if draft_recipe is None:
        draft_media = await repo.get_draft_media(user.email)
        return (await repo.put_draft_recipe(user_id=user.email, recipe=DraftRecipeRequestModel(
            name=None,
            user_content=None,
            user_tags=None,
            user_rating=None,
        ))).to_response_model(draft_media)
    draft_media = await repo.get_draft_media(user.email)
    return draft_recipe.to_response_model(draft_media)

@api_v1_router.post('/draftrecipe', response_model=DraftRecipeResponseModel)
async def post_draft_recipe(request: Request, user: ValidUser, recipe: DraftRecipeRequestModel) -> DraftRecipeResponseModel:
    repo: S3StorageRepository = request.app.state.storage_repository
    draft_recipe = await repo.put_draft_recipe(user_id=user.email, recipe=recipe)
    draft_media = await repo.get_draft_media(user.email)
    return draft_recipe.to_response_model(draft_media)

@api_v1_router.delete('/draftrecipe', response_model=MessageResponse, responses={
    404: { "model": MessageResponse, "description": "Draft recipe not found" },
})
async def delete_draft_recipe(request: Request, user: ValidUser) -> MessageResponse | JSONResponse:
    repo: S3StorageRepository = request.app.state.storage_repository
    draft_recipe = await repo.delete_draft_recipe(user_id=user.email)
    if draft_recipe is None:
        return JSONResponse(status_code=404, content={"detail": "Draft recipe not found"})
    return MessageResponse(detail="Draft recipe deleted successfully")

@api_v1_router.get('/login')
async def login(request: Request):
    client: Any = request.app.state.oauth.auth0
    return await client.authorize_redirect(request, request.app.state.settings.oidc_redirect_uri)

@api_v1_router.get('/whoami')
async def whoami(request: Request, user: ValidUser) -> User:
    return user

@api_v1_router.api_route('/auth', methods=['GET', 'POST'])
async def auth(request: Request):
    token = await request.app.state.oauth.auth0.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


def configure_logging(settings: Settings):
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

@asynccontextmanager
async def lifespan(app: FastAPI, settings: Settings):
    app.state.settings = settings
    app.state.storage_repository = S3StorageRepository(settings)
    app.state.oauth = OAuth()
    app.state.oauth.register(
            "auth0",
            client_id=settings.oidc_client_id,
            client_secret=settings.oidc_client_secret,
            client_kwargs={
                "scope": "openid profile email",
                "redirect_uri": settings.oidc_redirect_uri,
            },
            server_metadata_url=f'https://{settings.oidc_domain}/.well-known/openid-configuration'
    )
    app.state.llm_recipe_service = AnthropicRecipeService(
        settings, app.state.storage_repository
    )
    configure_logging(settings)
    yield
    print("Shutting down")

def create_app() -> FastAPI:
    settings = Settings.model_validate({})
    app = FastAPI(
        title="Wasfeines API",
        description="API for Wasfeines",
        version="0.1.0",
        lifespan=lambda app: lifespan(app, settings),
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.app_secret_key)
    app.include_router(api_v1_router, prefix="/api/v1")
    return app