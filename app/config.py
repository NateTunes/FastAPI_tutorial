from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str
    DB_PASS: str
    DB_NAME: str
    DB_USERNAME: str
    DB_SECRET_KEY: str
    DB_ALGORITHM: str
    DB_ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
