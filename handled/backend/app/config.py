from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    APP_BASE_URL: str = "http://localhost:3000"
    API_BASE_URL: str = "http://localhost:8000"
    MAGIC_LINK_SECRET: str
    SESSION_COOKIE_NAME: str = "handled_session"
    UPLOAD_DIR: str = "./uploads"
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
