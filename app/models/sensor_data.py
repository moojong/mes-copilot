from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    text,
    event,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Connection
from datetime import date
from calendar import monthrange
from .sensor_base import SensorBase
import uuid


def _add_months(orig_date: date, months: int) -> date:
    """간단한 월 추가 유틸리티

    Args:
        orig_date: 기준 날짜
        months: 추가할 개월 수

    Returns:
        계산된 날짜
    """
    year = orig_date.year + (orig_date.month - 1 + months) // 12
    month = (orig_date.month - 1 + months) % 12 + 1
    day = min(orig_date.day, monthrange(year, month)[1])
    return date(year, month, day)


class SensorData(SensorBase):
    """센서 데이터 테이블 (월별 Range Partitioning 적용)

    - 부모 테이블: `sensor_data` (RANGE PARTITION on `timestamp`)
    - 파티션: `sensor_data_YYYY_MM` 형식으로 자동 생성
    - 일일 10만 건 이상 적재 가능하도록 파티셔닝으로 성능 최적화
    """

    __tablename__ = "sensor_data"

    # PostgreSQL partitioning 지시: RANGE 기반 월별 파티션
    __table_args__ = (
        {"postgresql_partition_by": "RANGE (timestamp)"},
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    equipment_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    values = Column(JSONB, nullable=False)
    is_anomaly = Column(Boolean, default=False)


def _create_monthly_partitions(target, connection: Connection, **kw):
    """`sensor_data` 테이블 생성 후 다음 12개월치 파티션을 생성합니다.

    Args:
        target: SQLAlchemy Table 객체
        connection: 활성 DB 연결
        **kw: 추가 파라미터 (미사용)

    참고:
        - 이 함수는 `after_create` 이벤트로 등록되며, MetaData.create_all()
          또는 Table.create() 실행 시 자동으로 호출됩니다.
        - 파티션 범위는 해당 월 1일 00:00 ~ 다음 월 1일 00:00 입니다.
    """
    # 기준: 이번 달 1일
    today = date.today().replace(day=1)
    for i in range(0, 12):
        start = _add_months(today, i)
        end = _add_months(today, i + 1)
        part_name = f"sensor_data_{start.year}_{start.month:02d}"

        # 파티션 생성 SQL (IF NOT EXISTS 추가하여 중복 생성 방지)
        sql = f"""
        CREATE TABLE IF NOT EXISTS {part_name}
        PARTITION OF sensor_data
        FOR VALUES FROM ('{start.isoformat()} 00:00:00+00:00') TO ('{end.isoformat()} 00:00:00+00:00');
        """
        connection.execute(text(sql))


# 테이블 생성 후 파티션 자동 생성
event.listen(SensorData.__table__, "after_create", _create_monthly_partitions)
