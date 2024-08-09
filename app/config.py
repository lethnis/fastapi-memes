from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
