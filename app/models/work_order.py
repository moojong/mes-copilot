from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, text, Enum
from sqlalchemy.orm import relationship
from .master_base import MasterBase
import enum
import uuid


class WorkOrderStatus(str, enum.Enum):
    """작업지시 상태 열거형"""
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class WorkOrder(MasterBase):
    """작업지시 테이블

    order_id (UUID)를 기본키로 사용합니다.
    product_id는 products 테이블의 FK입니다.
    """

    __tablename__ = "work_orders"

    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    order_qty = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(WorkOrderStatus, native_enum=False), default=WorkOrderStatus.PLANNED)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)

    # 관계 설정
    product = relationship("Product", backref="work_orders")
