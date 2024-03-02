from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int
    database_url: str
    cors_allowed_origins: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)