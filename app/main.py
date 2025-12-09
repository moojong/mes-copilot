from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from routers import root_router
from core.database import get_master_db, get_sensor_db


app = FastAPI(title="MES Copilot API")


@app.get("/", response_model=str)
def read_root() -> str:
    """루트 엔드포인트

    MES Copilot 서비스의 루트 엔드포인트입니다. GET 요청 시
    "MES Copilot" 문자열을 반환합니다.

    Returns:
        str: 항상 "MES Copilot" 문자열을 반환합니다.

    Raises:
        없음
    """
    return "MES Copilot"

# master-db 확인 엔드포인트
@app.get("/health/master-db")
def health_check_master_db(db: Session = Depends(get_master_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Master DB is healthy"}
    except Exception:
        raise HTTPException(status_code=500, detail="Master DB is unhealthy")

# sensor-db 확인 엔드포인트
@app.get("/health/sensor-db")
def health_check_sensor_db(db: Session = Depends(get_sensor_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Sensor DB is healthy"}
    except Exception:
        raise HTTPException(status_code=500, detail="Sensor DB is unhealthy")

app.include_router(root_router)
