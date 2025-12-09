from sqlalchemy import Column, String, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB
from .master_base import MasterBase


class Equipment(MasterBase):
    """설비 마스터 테이블

    equipment_id (설비코드)를 기본키로 사용합니다.
    attributes (JSONB)에 GIN 인덱스를 적용합니다.
    """

    __tablename__ = "equipment"

    equipment_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    equipment_type = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    attributes = Column(JSONB, default={})
    enabled = Column(Boolean, default=True)

    # GIN 인덱스 for JSONB 쿼리 성능
    __table_args__ = (
        Index("idx_equipment_attributes_gin", "attributes", postgresql_using="gin"),
    )
