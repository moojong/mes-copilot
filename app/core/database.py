from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings


# 마스터 DB 엔진/세션
engine_master = create_engine(
    settings.database_url_master,
    future=True,
    pool_pre_ping=True,
)
SessionLocalMaster = sessionmaker(bind=engine_master, autocommit=False, autoflush=False, class_=Session)


# 센서 DB 엔진/세션
engine_sensor = create_engine(
    settings.database_url_sensor,
    future=True,
    pool_pre_ping=True,
)
SessionLocalSensor = sessionmaker(bind=engine_sensor, autocommit=False, autoflush=False, class_=Session)


def get_master_db() -> Generator[Session, None, None]:
    """마스터 DB 세션을 제공하는 의존성

    Yields:
        Generator[Session, None, None]: SQLAlchemy 세션
    """
    db = SessionLocalMaster()
    try:
        yield db
    finally:
        db.close()


def get_sensor_db() -> Generator[Session, None, None]:
    """센서 DB 세션을 제공하는 의존성

    Yields:
        Generator[Session, None, None]: SQLAlchemy 세션
    """
    db = SessionLocalSensor()
    try:
        yield db
    finally:
        db.close()
