try:
    # pydantic v2.12+ moved BaseSettings to separate package `pydantic-settings`.
    from pydantic import BaseSettings  # type: ignore
except Exception:
    from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    """애플리케이션 설정 (환경 변수에서 로드).

    다음 환경 변수를 사용합니다:
    - DATABASE_URL_MASTER: 마스터 DB의 SQLAlchemy URL
    - DATABASE_URL_SENSOR: 센서 DB의 SQLAlchemy URL
    - FASTAPI_PORT: FastAPI가 바인드할 포트
    """

    database_url_master: str
    database_url_sensor: str
    fastapi_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
