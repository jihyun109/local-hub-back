from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "LocalHub"
    API_V1_PREFIX: str = "/api"

    DATABASE_URL: str = "sqlite:///./localhub.db"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]


settings = Settings()
