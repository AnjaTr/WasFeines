from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Optional
import asyncio
from pathlib import Path
import json
from uuid import uuid4
from dataclasses import asdict
import logging

from pydantic import TypeAdapter
import boto3
from botocore.config import Config
if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client

from wasfeines.models.recipe import Recipe, Media
from wasfeines.models.draft import DraftMedia
from wasfeines.models.draft import DraftRecipe, DraftRecipeRequestModel
from wasfeines.settings import Settings

log = logging.getLogger(__name__)

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
    def get_draft_media_sync(self) -> List[DraftMedia]:
        raise NotImplementedError()

    @abstractmethod
    def get_draft_recipe_sync(self, user_id: str) -> DraftRecipe:
        raise NotImplementedError()

    @abstractmethod
    def put_draft_recipe_sync(self, user_id: str, recipe: DraftRecipeRequestModel) -> DraftRecipe:
        raise NotImplementedError()

    @abstractmethod
    def delete_draft_recipe_sync(self, user_id: str) -> bool:
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

    async def get_draft_media(self, user_id: str) -> List[DraftMedia]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_draft_media_sync, user_id)

    async def get_draft_recipe(self, user_id: str) -> DraftRecipe:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_draft_recipe_sync, user_id)

    async def put_draft_recipe(self, user_id: str, recipe: DraftRecipeRequestModel) -> DraftRecipe:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.put_draft_recipe_sync, user_id, recipe)

    async def delete_draft_recipe(self, user_id: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.delete_draft_recipe_sync, user_id)



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

    def _get_presigned_get_put_urls(self, key: str) -> tuple[str, str, str]:
        get_url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.s3_bucket, "Key": key},
            ExpiresIn=3600,
        )
        put_url = self.s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.settings.s3_bucket, "Key": key},
            ExpiresIn=3600,
        )
        delete_url = self.s3.generate_presigned_url(
            "delete_object",
            Params={"Bucket": self.settings.s3_bucket, "Key": key},
            ExpiresIn=3600,
        )
        return get_url, put_url, delete_url

    def get_draft_media_sync(self, user_id: str) -> List[DraftMedia]:
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}"
        existing_objects = self.s3.list_objects_v2(
            Bucket=self.settings.s3_bucket, Prefix=f"{key}/"
        )
        draft_media = []
        if existing_objects["KeyCount"] > 0:
            for obj in existing_objects["Contents"]:
                key_inner = obj["Key"]
                get_url, put_url, delete_url = self._get_presigned_get_put_urls(key_inner)
                draft_media.append(
                    DraftMedia(
                        exists=True,
                        get_url=get_url,
                        put_url=put_url,
                        delete_url=delete_url,
                        create_timestamp=obj["LastModified"].timestamp(),
                    )
                )
        for i in range(self.settings.max_num_draft_media - len(draft_media)):
            uuid = str(uuid4())
            key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}/{uuid}"
            get_url, put_url, _ = self._get_presigned_get_put_urls(str(key))
            draft_media.append(
                DraftMedia(
                    exists=False,
                    get_url=get_url,
                    put_url=put_url,
                )
            )
        return draft_media

    def get_draft_recipe_sync(self, user_id: str) -> Optional[DraftRecipe]:
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}-draft.json"
        try:
            existing_object = self.s3.get_object(
                Bucket=self.settings.s3_bucket, Key=str(key)
            )
        except self.s3.exceptions.NoSuchKey:
            return None
        contents = existing_object["Body"].read()
        draft_recipe = TypeAdapter(DraftRecipe).validate_json(contents)
        return draft_recipe

    def put_draft_recipe_sync(self, user_id: str, recipe: DraftRecipeRequestModel) -> DraftRecipe:
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}-draft.json"
        json_dict = asdict(recipe.to_draft_recipe(created_by=user_id))
        self.s3.put_object(
            Bucket=self.settings.s3_bucket,
            Key=str(key),
            Body=json.dumps(json_dict, default=str),
            ContentType="application/json",
        )
        return self.get_draft_recipe_sync(user_id)

    def delete_draft_recipe_sync(self, user_id):
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}-draft.json"
        try:
            self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(key))
            return True
        except self.s3.exceptions.NoSuchKey:
            return False