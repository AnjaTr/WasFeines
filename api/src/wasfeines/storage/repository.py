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
    from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef


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
    def put_recipe_sync(self, recipe: DraftRecipe, media: List[DraftMedia], recipe_html: str) -> Recipe:
        raise NotImplementedError()

    @abstractmethod
    def delete_recipe_sync(self, id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_draft_media_sync(self, user_id: str) -> List[DraftMedia]:
        raise NotImplementedError()

    @abstractmethod
    def get_draft_recipe_sync(self, user_id: str) -> Optional[DraftRecipe]:
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

    async def put_recipe(self, recipe: DraftRecipe, media: List[DraftMedia], recipe_html: str) -> Recipe:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.put_recipe_sync, recipe, media, recipe_html)

    async def delete_recipe(self, id: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.delete_recipe_sync, id)

    async def get_draft_media(self, user_id: str) -> List[DraftMedia]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_draft_media_sync, user_id)

    async def get_draft_recipe(self, user_id: str) -> Optional[DraftRecipe]:
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

    def _load_item(self, key_html: str, objects: "ListObjectsV2OutputTypeDef") -> Recipe:
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
        if "Contents" not in objects:
            raise ValueError(f"Recipe {key_html} not found in S3")
        for obj_inner in objects["Contents"]:
            if "Key" not in obj_inner:
                continue
            key_inner = obj_inner["Key"]
            if key_inner.startswith(f"{key_noext}/"):
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
            if "Key" not in obj_inner:
                continue
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
        if "Contents" not in objects:
            return recipes
        for obj in objects["Contents"]:
            if "Key" not in obj:
                continue
            key = obj["Key"]
            if key.endswith(".html"):
                recipes.append(self._load_item(key, objects))
        return recipes

    def put_recipe_sync(self, recipe: DraftRecipe, media: List[DraftMedia], recipe_html: str) -> Recipe:
        id = f"{recipe.name}.html"
        html_key = Path(self.settings.s3_bucket_base_path) / id
        self.s3.put_object(
            Bucket=self.settings.s3_bucket,
            Key=str(html_key),
            Body=recipe_html,
            ContentType="text/html",
        )
        for media_item in media:
            if not media_item.exists:
                continue
            dest_media_key = Path(self.settings.s3_bucket_base_path) / f"{recipe.name}/{media_item.name}"
            self.s3.copy_object(
                Bucket=self.settings.s3_bucket,
                CopySource={
                    "Bucket": self.settings.s3_bucket,
                    "Key": media_item.key
                },
                Key=str(dest_media_key),
            )
        json_key = Path(self.settings.s3_bucket_base_path) / f"{recipe.name}.json"
        recipe_dict = asdict(recipe)
        self.s3.put_object(
            Bucket=self.settings.s3_bucket,
            Key=str(json_key),
            Body=json.dumps(recipe_dict, default=str),
            ContentType="application/json",
        )
        list_objects = self.s3.list_objects_v2(
            Bucket=self.settings.s3_bucket, Prefix=str(html_key)
        )
        return self._load_item(id, list_objects)
    
    def delete_recipe_sync(self, id: str) -> bool:
        html_key = f"{id}.html"
        json_key = f"{id}.json"
        folder_key = f"{id}/"
        resp = self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(html_key))
        if resp["ResponseMetadata"]["HTTPStatusCode"] != 204:
            return False
        self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(json_key))
        objects = self.s3.list_objects_v2(
            Bucket=self.settings.s3_bucket, Prefix=str(folder_key)
        )
        if "Contents" not in objects:
            return True
        for obj in objects["Contents"]:
            if "Key" not in obj:
                continue
            key = obj["Key"]
            if key == folder_key:
                continue
            self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(key))
        return True

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
            assert "Contents" in existing_objects
            for obj in existing_objects["Contents"]:
                if "Key" not in obj:
                    continue
                assert "LastModified" in obj
                key_inner = obj["Key"]
                get_url, put_url, delete_url = self._get_presigned_get_put_urls(key_inner)
                draft_media.append(
                    DraftMedia(
                        exists=True,
                        name=key_inner.split("/")[-1],
                        key=key_inner,
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
                    key=str(key),
                    name=uuid,
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
        draft_recipe = recipe.to_draft_recipe(created_by=user_id)
        json_dict = asdict(draft_recipe)
        self.s3.put_object(
            Bucket=self.settings.s3_bucket,
            Key=str(key),
            Body=json.dumps(json_dict, default=str),
            ContentType="application/json",
        )
        return draft_recipe

    def delete_draft_recipe_sync(self, user_id):
        key = Path(self.settings.s3_bucket_base_path) / self.settings.s3_draft_folder / f"{user_id}-draft.json"
        try:
            self.s3.delete_object(Bucket=self.settings.s3_bucket, Key=str(key))
            return True
        except self.s3.exceptions.NoSuchKey:
            return False