from typing import List
from contextlib import asynccontextmanager
import logging
import sys

from fastapi import FastAPI, Request, APIRouter

from wasfeines.models import Recipe
from wasfeines.settings import Settings
from wasfeines.storage.repository import S3StorageRepository

log = logging.getLogger(__name__)

api_v1_router = APIRouter()

@api_v1_router.get("/recipes")
async def get_recipes(request: Request) -> List[Recipe]:
    repo: S3StorageRepository = request.app.state.storage_repository
    return await repo.list_recipes()

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
    app.include_router(api_v1_router, prefix="/api/v1")
    return app