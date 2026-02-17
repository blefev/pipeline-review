from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://pipeline:pipeline@localhost:5432/pipeline"
    elasticsearch_url: str = "http://localhost:9200"
    read_only: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()
