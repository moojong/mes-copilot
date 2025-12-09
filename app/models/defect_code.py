from sqlalchemy import Column, String
from .master_base import MasterBase


class DefectCode(MasterBase):
    """불량코드 마스터 테이블

    defect_code (불량코드)를 기본키로 사용합니다.
    """

    __tablename__ = "defect_codes"

    defect_code = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
