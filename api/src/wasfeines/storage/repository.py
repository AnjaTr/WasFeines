from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
import asyncio
from pathlib import Path
import json
from uuid import uuid4

import boto3
from botocore.config import Config
if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client

from wasfeines.models.recipe import Recipe, Media
from wasfeines.models.draft import DraftMedia
from wasfeines.models.draft import DraftRecipe
from wasfeines.settings import Settings


class StorageRepository(ABC):
    @abstractmethod
    def list_recipes_sync(self) -> List[Recipe]:
        raise NotImplementedError()

    @abstractmethod
    def put_recipe_sync(self, recipe: DraftRecipe) -> Recipe:
        raise NotImplementedError()

    @abstractmethod
    def delete_recipe_sync(self, id: str) -> Recipe:
        raise NotImplementedError()

    @abstractmethod
    def get_draft_media_sync(self) -> List[DraftRecipe]:
        raise NotImplementedError()

    async def list_recipes(self) -> List[Recipe]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.list_recipes_sync)

    async def put_recipe(self, recipe: DraftRecipe) -> Recipe:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.put_recipe_sync, recipe)

    async def delete_recipe(self, id: str) -> Recipe:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.delete_recipe_sync, id)

    async def get_draft_media(self) -> List[DraftRecipe]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_draft_media_sync)


def is_media(key: str) -> bool:
    return (
        key.endswith(".jpg")
        or key.endswith(".jpeg")
        or key.endswith(".png")
        or key.endswith(".gif")
        or key.endswith(".webp")
    )


class S3StorageRepository(StorageRepository):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.s3: S3Client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=Config(
                response_checksum_validation="when_required"
            ),
        )

    def _load_item(self, key_html: str, objects: List) -> Recipe:
        """
        Given a recipe key, for example "recipe_Peanut_Protein_Balls.html", return the full recipe object

        * Loading the associated recipe_Peanut_Protein_Balls.json, if it exists
        * Loading all media files associated with the recipe
        """
        key_presigned = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.s3_bucket, "Key": key_html},
            ExpiresIn=3600,
        )
        key_noext = key_html[:-5]
        media = []
        for obj_inner in objects["Contents"]:
            key_inner = obj_inner["Key"]
            if key_inner.startswith(key_noext) and is_media(key_inner):
                key_inner_presigned = self.s3.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": self.settings.s3_bucket,
                        "Key": key_inner,
                    },
                    ExpiresIn=3600,
                )
                media.append(
                    Media(name=key_inner, content_url=key_inner_presigned)
                )
        summary = None
        for obj_inner in objects["Contents"]:
            key_inner = obj_inner["Key"]
            if key_inner == f"{key_noext}.json":
                contents = self.s3.get_object(
                    Bucket=self.settings.s3_bucket, Key=key_inner
                )["Body"].read()
                summary = json.loads(contents)

        return Recipe(
            name=key_noext,
            content_url=key_presigned,
            media=media,
            summary=summary,
        )

    def list_recipes_sync(self) -> List[Recipe]:
        objects = self.s3.list_objects_v2(
            Bucket=self.settings.s3_bucket, Prefix=self.settings.s3_bucket_base_path
        )
        recipes = []
        for obj in objects["Contents"]:
            key = obj["Key"]
            if key.endswith(".html"):
                recipes.append(self._load_item(key, objects))
        return recipes

    def put_recipe_sync(self, recipe: DraftRecipe) -> Recipe:
        key = Path(self.settings.s3_bucket_base_path) / f"{recipe.name}.html"
        self.s3.put_object(
            Bucket=self.settings.s3_bucket,
            Key=str(key),
            Body=recipe.content,
            ContentType="text/html",
        )
        return Recipe(
            name=recipe.name,
            content_url=self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.settings.s3_bucket, "Key": str(key)},
                ExpiresIn=3600,
            ),
            media=[],
        )
    
    def delete_recipe_sync(self, id: str) -> Recipe:
        key = Path(self.settings.s3_bucket_base_path) / f"{id}.html"
        self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(key))
        return Recipe(
            name=id,
            content_url="",
            media=[],
        )

    def get_draft_media_sync(self) -> DraftMedia:
        media_uuid = str(uuid4())
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{media_uuid}"
        media = DraftMedia(
            get_url=self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.settings.s3_bucket, "Key": str(key)},
                ExpiresIn=3600,
            ),
            put_url=self.s3.generate_presigned_url(
                "put_object",
                Params={"Bucket": self.settings.s3_bucket, "Key": str(key)},
                ExpiresIn=3600,
            ),
        )
        return media
