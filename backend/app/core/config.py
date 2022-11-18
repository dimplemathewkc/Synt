from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # hiring api details
    API_KEY: str
    API_SECRET: str
    API_URL: str

    CACHE_ACTIVE: bool = True

    # redis details
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
