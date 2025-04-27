from pydantic import (
    Field,
)

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    s3_bucket: str = Field(alias='S3_BUCKET')
    s3_access_key: str = Field(alias='S3_ACCESS_KEY')
    s3_secret_key: str = Field(alias='S3_SECRET_ACCESS_KEY')
    s3_region: str = Field(alias='S3_REGION')
    s3_endpoint_url: str = Field(alias='S3_ENDPOINT_URL')
    s3_bucket_base_path: str = Field(alias='S3_BUCKET_BASE_PATH')
    s3_draft_folder: str = Field(alias='S3_DRAFT_FOLDER', default='drafts')
    debug: bool = Field(alias='DEBUG', default=False)
    oidc_client_id: str = Field(alias='OIDC_CLIENT_ID')
    oidc_client_secret: str = Field(alias='OIDC_CLIENT_SECRET')
    oidc_domain: str = Field(alias='OIDC_DOMAIN')
    oidc_redirect_uri: str = Field(alias='OIDC_REDIRECT_URI')
    app_secret_key: str = Field(alias='APP_SECRET_KEY')
    max_num_draft_media: int = Field(alias='MAX_NUM_DRAFT_MEDIA', default=10, description="Number of draft media items to send to client on request")
    anthropic_api_key: str = Field(alias='ANTHROPIC_API_KEY')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')