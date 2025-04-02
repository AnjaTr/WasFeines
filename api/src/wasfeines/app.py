from typing import List, Annotated
from contextlib import asynccontextmanager
from dataclasses import dataclass
import logging
import sys

from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.oauth1.client import OAuth1Client
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from pydantic import TypeAdapter

from wasfeines.models import Recipe, User
from wasfeines.models.draft import DraftMedia
from wasfeines.settings import Settings
from wasfeines.storage.repository import S3StorageRepository

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

@api_v1_router.get('/login')
async def login(request: Request):
    client: OAuth1Client = request.app.state.oauth.auth0
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
    configure_logging(settings)
    yield
    print("Shutting down")

def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="Wasfeines API",
        description="API for Wasfeines",
        version="0.1.0",
        lifespan=lambda app: lifespan(app, settings),
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.app_secret_key)
    app.include_router(api_v1_router, prefix="/api/v1")
    return app