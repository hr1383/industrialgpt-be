from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()