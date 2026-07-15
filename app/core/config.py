from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "LocalHub"
    API_V1_PREFIX: str = "/api"

    DATABASE_URL: str = "sqlite:///./localhub.db"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5-mini"
    CHAT_MAX_HISTORY: int = 20          # 저장할 최대 메시지(user+assistant) 개수
    CHAT_SYSTEM_PROMPT: str = "당신은 친절한 관광 안내 챗봇입니다."

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
