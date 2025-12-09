from sqlalchemy import Column, String, Integer, Boolean
from .master_base import MasterBase


class Product(MasterBase):
    """제품 마스터 테이블

    product_id (제품코드)를 기본키로 사용합니다.
    """

    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=True)
    unit_price = Column(Integer, default=0)
    enabled = Column(Boolean, default=True)
