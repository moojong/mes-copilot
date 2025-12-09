from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .master_base import MasterBase
import uuid


class WorkResult(MasterBase):
    """작업실적 테이블

    result_id (UUID)를 기본키로 사용합니다.
    work_order_id, equipment_id, defect_code_id는 각각 FK입니다.
    work_data (JSONB)에 상세 정보를 저장합니다.
    """

    __tablename__ = "work_results"

    result_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    work_order_id = Column(String(36), ForeignKey("work_orders.order_id"), nullable=False)
    equipment_id = Column(String(50), ForeignKey("equipment.equipment_id"), nullable=True)
    good_qty = Column(Integer, default=0)
    defect_qty = Column(Integer, default=0)
    defect_code_id = Column(String(20), ForeignKey("defect_codes.defect_code"), nullable=True)
    work_data = Column(JSONB, default={})
    work_date = Column(Date, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=False)

    # 관계 설정
    work_order = relationship("WorkOrder", backref="work_results")
    equipment = relationship("Equipment", backref="work_results")
    defect_code = relationship("DefectCode", backref="work_results")
